import crypto from 'node:crypto';
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';

import { config } from './config.js';
import { closeDb, query } from './db.js';
import { chargeSchema } from './validation.js';
import {
  initializeMobileMoneyCharge,
  verifyCharge,
  getCapabilities,
} from './paystack.js';
import { buildBankTransferInstructions, recordBankTransferIntent } from './bank.js';
import {
  beginIdempotent,
  rememberIdempotent,
  newReference,
  savePayment,
  updatePayment,
  getPayment,
  saveWebhookEvent,
  markWebhookProcessed,
} from './store.js';

const app = express();

app.disable('x-powered-by');
app.set('trust proxy', 1);
app.use(helmet());

// CORS is scoped to the one site that is allowed to call this API.
app.use(
  cors({
    origin: config.allowedOrigins,
    methods: ['GET', 'POST'],
    allowedHeaders: ['Content-Type', 'Idempotency-Key'],
  })
);

/**
 * The webhook needs the EXACT raw bytes to recompute the HMAC. Express parses
 * JSON before any route runs, so we capture the raw body in verify() instead
 * of mounting a second body parser.
 */
app.use(
  express.json({
    limit: '64kb',
    verify: (req, res, buf) => {
      req.rawBody = buf;
    },
  })
);

// A coarse limiter. Put a real one (Redis) in front in production.
const hits = new Map();
app.use('/api', (req, res, next) => {
  const key = req.ip || 'unknown';
  const now = Date.now();
  const window = 60_000;
  const max = 20;
  const entry = hits.get(key);
  if (!entry || now - entry.start > window) {
    hits.set(key, { start: now, count: 1 });
    return next();
  }
  entry.count += 1;
  if (entry.count > max) {
    return res.status(429).json({ error: 'Too many requests, please slow down' });
  }
  return next();
});

// ---------------------------------------------------------------------------
// POST /api/charge
// ---------------------------------------------------------------------------
app.post('/api/charge', async (req, res, next) => {
  try {
    const parsed = chargeSchema.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({
        error: 'validation_failed',
        details: parsed.error.issues.map((i) => ({
          field: i.path.join('.'),
          message: i.message,
        })),
      });
    }

    const input = parsed.data;

    // Bank transfer never touches Paystack; hand back the printable details.
    if (input.method === 'bank_transfer') {
      const instructions = buildBankTransferInstructions();
      if (!instructions.available) {
        return res.status(409).json({
          error: 'bank_transfer_unavailable',
          warning: instructions.warning,
        });
      }
      const reference = input.reference || newReference('BANK');
      const record = await recordBankTransferIntent({
        email: input.email,
        amount: input.amount,
        currency: input.currency,
        reference,
      });
      return res.json({ ...record, instructions });
    }

    // Guard against double taps creating two charges.
    const idemKey = req.get('Idempotency-Key');
    const replay = {};
    if (await beginIdempotent(idemKey, replay)) {
      return res.json({ ...replay, replayed: true });
    }

    const reference = newReference('RPAI');

    const charge = await initializeMobileMoneyCharge({
      email: input.email,
      amount: input.amount,
      currency: input.currency,
      phone: input.mobile_money.phone,
      provider: input.mobile_money.provider,
      reference,
    });

    await savePayment({
      reference: charge.reference,
      method: 'mobile_money',
      provider: input.mobile_money.provider,
      email: input.email,
      amount: input.amount,
      currency: input.currency,
      status: charge.status,
      authorizationUrl: charge.authorizationUrl,
      providerReference: charge.accessCode,
    });

    const payload = {
      reference: charge.reference,
      status: charge.status,
      authorizationUrl: charge.authorizationUrl,
      /**
       * The customer must open this to enter their PIN. There is no way to
       * keep them on the church's page for this step.
       */
      next: 'authorise',
      message:
        'Open the secure payment page to enter your mobile money PIN, then return here.',
    };
    await rememberIdempotent(idemKey, payload);
    return res.json(payload);
  } catch (err) {
    return next(err);
  }
});

// ---------------------------------------------------------------------------
// GET /api/bank-transfer  (fallback card contents)
// ---------------------------------------------------------------------------
app.get('/api/bank-transfer', (_req, res) => {
  res.json(buildBankTransferInstructions());
});

// ---------------------------------------------------------------------------
// GET /api/capabilities  (confirm currency support against your own account)
// ---------------------------------------------------------------------------
app.get('/api/capabilities', async (_req, res, next) => {
  try {
    res.json(await getCapabilities());
  } catch (err) {
    next(err);
  }
});

// ---------------------------------------------------------------------------
// POST /api/webhook  (authoritative confirmation)
// ---------------------------------------------------------------------------
app.post('/api/webhook', async (req, res) => {
  // Paystack retries on non-2xx, so validate before acknowledging.
  const signature = req.get('x-paystack-signature');
  const secret = process.env.PAYSTACK_WEBHOOK_SECRET || config.paystack.secretKey;

  if (!signature || !req.rawBody) {
    return res.status(400).send('missing signature');
  }

  const expected = crypto
    .createHmac('sha512', secret)
    .update(req.rawBody)
    .digest('hex');

  const a = Buffer.from(expected);
  const b = Buffer.from(signature);
  const valid = a.length === b.length && crypto.timingSafeEqual(a, b);
  if (!valid) {
    return res.status(401).send('invalid signature');
  }

  const event = req.body;
  const webhookRowId = await saveWebhookEvent({
    eventId: event?.data?.id,
    eventType: event?.event,
    reference: event?.data?.reference,
    payload: event,
    signatureValid: true,
  }).catch((err) => {
    // The audit copy is important but must not cause Paystack to retry a
    // payment already confirmed by a valid signature.
    console.error('[webhook] could not record event:', err.message);
    return null;
  });

  if (event?.event === 'charge.success') {
    const data = event.data ?? {};
    const reference = data.reference;
    const amount = data.amount;
    const status = data.status;

    // The webhook is the only trustworthy confirmation of payment.
    await updatePayment(reference, {
      status,
      paidAt: data.paid_at ?? new Date().toISOString(),
      channel: data.channel,
      providerResponse: {
        amount,
        currency: data.currency,
        fees: data.fees,
        authorisationCode: data.authorization_code,
        paid: data.paid,
      },
    });

    // TODO: enqueue the thank-you email / receipt here, not inline.
    console.log(`[webhook] charge.success ${reference} ${status}`);
  }

  if (event?.event === 'charge.failed') {
    await updatePayment(event.data?.reference, { status: 'failed' });
  }

  await markWebhookProcessed(webhookRowId).catch((err) => {
    console.error('[webhook] could not mark event processed:', err.message);
  });

  // Always acknowledge fast; do heavy work asynchronously.
  return res.sendStatus(200);
});

// ---------------------------------------------------------------------------
// GET /api/payments/:reference  (client polling fallback)
// ---------------------------------------------------------------------------
app.get('/api/payments/:reference', async (req, res, next) => {
  try {
    const local = await getPayment(req.params.reference);

    // If still pending, ask Paystack directly rather than trusting local state.
    if (local && local.status === 'pending') {
      const verified = await verifyCharge(req.params.reference).catch(() => null);
      if (verified) {
        await updatePayment(req.params.reference, {
          status: verified.status,
          paidAt: verified.paid_at,
          channel: verified.channel,
        });
      }
    }

    const fresh = (await getPayment(req.params.reference)) ?? local;
    if (!fresh) return res.status(404).json({ error: 'not_found' });

    return res.json({
      reference: fresh.reference,
      status: fresh.status,
      amount: fresh.amount,
      currency: fresh.currency,
      method: fresh.method,
    });
  } catch (err) {
    return next(err);
  }
});

// ---------------------------------------------------------------------------
app.get('/api/health', async (_req, res) => {
  try {
    await query('select 1');
    return res.json({
      ok: true,
      db: 'ok',
      currency: config.paystack.currency,
    });
  } catch (err) {
    console.error('[health] database check failed:', err.message);
    return res.status(503).json({
      ok: false,
      db: 'unavailable',
      currency: config.paystack.currency,
    });
  }
});

app.use((err, _req, res, _next) => {
  console.error('[error]', err);
  res.status(err.status || 500).json({
    error: err.code || 'internal_error',
    // Never echo upstream bodies; they can contain account details.
    message: err.message || 'Something went wrong',
  });
});

const server = app.listen(config.port, () => {
  console.log(`RPAI giving API listening on :${config.port}`);
  console.log(`Allowed origins: ${config.allowedOrigins.join(', ')}`);
  console.log(`Currency: ${config.paystack.currency}`);
});

let shuttingDown = false;
async function shutdown(signal) {
  if (shuttingDown) return;
  shuttingDown = true;
  console.log(`[shutdown] ${signal}`);
  server.close(async () => {
    await closeDb().catch(() => {});
    process.exit(0);
  });
  // Do not let a stuck connection keep a Render instance alive forever.
  setTimeout(() => process.exit(1), 10_000).unref();
}

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));

export default app;