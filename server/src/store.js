import { createHash, randomUUID } from 'node:crypto';

import { query } from './db.js';

/**
 * Postgres persistence for payment attempts, idempotency keys and webhook
 * audit events. The API is still deliberately small: this module is the only
 * place that reads or writes those tables.
 */
const IDEMPOTENCY_TTL_MS = 15 * 60 * 1000;

/** Input field -> database column. Only these names are ever interpolated. */
const PAYMENT_COLUMNS = {
  method: 'method',
  provider: 'provider',
  email: 'email',
  amount: 'amount',
  currency: 'currency',
  status: 'status',
  authorizationUrl: 'authorization_url',
  providerReference: 'provider_reference',
  paidAt: 'paid_at',
  channel: 'channel',
  providerResponse: 'provider_response',
};

function encodeValue(columnKey, value) {
  if (columnKey === 'providerResponse') {
    return value === null || value === undefined ? null : JSON.stringify(value);
  }
  return value;
}

function mapPayment(row) {
  if (!row) return null;
  return {
    reference: row.reference,
    method: row.method,
    provider: row.provider ?? undefined,
    email: row.email ?? undefined,
    amount: Number(row.amount),
    currency: row.currency,
    status: row.status,
    authorizationUrl: row.authorization_url ?? undefined,
    providerReference: row.provider_reference ?? undefined,
    paidAt: row.paid_at ? new Date(row.paid_at).toISOString() : undefined,
    channel: row.channel ?? undefined,
    providerResponse: row.provider_response ?? undefined,
    createdAt: row.created_at ? new Date(row.created_at).toISOString() : undefined,
    updatedAt: row.updated_at ? new Date(row.updated_at).toISOString() : undefined,
  };
}

export function newReference(prefix = 'RPAI') {
  // Uppercase alphanumeric, easy for a donor to read out over the phone.
  const rand = randomUUID().replace(/-/g, '').slice(0, 16).toUpperCase();
  return `${prefix}_${rand}`;
}

export async function beginIdempotent(key, response) {
  if (!key) return false;

  const { rows } = await query(
    'select response from public.idempotency_keys where key = $1 and expires_at > now()',
    [key]
  );
  if (!rows.length) return false;

  Object.assign(response, rows[0].response || {});
  return true;
}

export async function rememberIdempotent(key, response) {
  if (!key) return;

  const expiresAt = new Date(Date.now() + IDEMPOTENCY_TTL_MS).toISOString();
  await query(
    `insert into public.idempotency_keys (key, response, expires_at)
     values ($1, $2::jsonb, $3)
     on conflict (key) do update
       set response = excluded.response,
           expires_at = excluded.expires_at`,
    [key, JSON.stringify(response || {}), expiresAt]
  );

  // Housekeeping on the same path; the table stays small without a cron job.
  await query('delete from public.idempotency_keys where expires_at < now()');
}

export async function savePayment(payment) {
  if (!payment?.reference) throw new Error('savePayment needs a reference');

  const input = { status: 'pending', currency: 'ZMW', ...payment };
  const keys = Object.keys(PAYMENT_COLUMNS).filter(
    (key) => input[key] !== undefined
  );
  const columns = ['reference', ...keys.map((key) => PAYMENT_COLUMNS[key])];
  const values = [input.reference, ...keys.map((key) => encodeValue(key, input[key]))];
  const placeholders = values.map((_, index) => `$${index + 1}`);
  const updates = keys
    .map((key) => `${PAYMENT_COLUMNS[key]} = excluded.${PAYMENT_COLUMNS[key]}`)
    .join(', ');

  const { rows } = await query(
    `insert into public.payments (${columns.join(', ')})
     values (${placeholders.join(', ')})
     on conflict (reference) do update set ${updates}
     returning *`,
    values
  );
  return mapPayment(rows[0]);
}

export async function updatePayment(reference, patch) {
  if (!reference) return null;

  const keys = Object.keys(PAYMENT_COLUMNS).filter(
    (key) => patch && patch[key] !== undefined
  );
  if (!keys.length) return getPayment(reference);

  const assignments = keys.map(
    (key, index) => `${PAYMENT_COLUMNS[key]} = $${index + 2}`
  );
  const values = [reference, ...keys.map((key) => encodeValue(key, patch[key]))];

  const { rows } = await query(
    `update public.payments
     set ${assignments.join(', ')}
     where reference = $1
     returning *`,
    values
  );
  return mapPayment(rows[0]);
}

export async function getPayment(reference) {
  const { rows } = await query(
    'select * from public.payments where reference = $1',
    [reference]
  );
  return mapPayment(rows[0]);
}

export async function listPayments() {
  const { rows } = await query(
    'select * from public.payments order by created_at desc limit 500'
  );
  return rows.map(mapPayment);
}

export async function saveWebhookEvent({
  provider = 'paystack',
  eventId = null,
  eventType = null,
  reference = null,
  payload,
  signatureValid = false,
}) {
  const serialized = JSON.stringify(payload ?? {});
  const payloadHash = createHash('sha256').update(serialized).digest('hex');

  const { rows } = await query(
    `insert into public.webhook_events
       (provider, event_id, event_type, reference, payload_hash, payload, signature_valid)
     values ($1, $2, $3, $4, $5, $6::jsonb, $7)
     on conflict (provider, payload_hash) do nothing
     returning id`,
    [
      provider,
      eventId === null || eventId === undefined ? null : String(eventId),
      eventType,
      reference,
      payloadHash,
      serialized,
      signatureValid,
    ]
  );

  return rows[0]?.id ?? null;
}

export async function markWebhookProcessed(id) {
  if (!id) return;
  await query(
    "update public.webhook_events set processed_at = now(), status = 'processed' where id = $1",
    [id]
  );
}
