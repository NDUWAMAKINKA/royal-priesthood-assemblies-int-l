import { config, toSubunits } from './config.js';

class PaystackError extends Error {
  constructor(message, { status = 502, code = 'paystack_error', response } = {}) {
    super(message);
    this.name = 'PaystackError';
    this.status = status;
    this.code = code;
    this.response = response;
  }
}

/**
 * Single place that talks to Paystack, so the secret key is never scattered
 * across the codebase and can never reach a response body.
 */
async function paystackRequest(path, { method = 'GET', body } = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), config.paystack.timeoutMs);

  try {
    const res = await fetch(`${config.paystack.baseUrl}${path}`, {
      method,
      headers: {
        Authorization: `Bearer ${config.paystack.secretKey}`,
        'Content-Type': 'application/json',
      },
      body: body ? JSON.stringify(body) : undefined,
      signal: controller.signal,
    });

    const payload = await res.json().catch(() => ({}));

    if (!res.ok) {
      throw new PaystackError(
        payload.message || 'The payment provider rejected the request',
        {
          status: res.status === 401 ? 500 : 502,
          code: 'upstream_error',
          response: payload,
        }
      );
    }
    return payload;
  } catch (err) {
    if (err instanceof PaystackError) throw err;
    if (err.name === 'AbortError') {
      throw new PaystackError('The payment provider did not respond in time', {
        status: 504,
        code: 'upstream_timeout',
      });
    }
    throw new PaystackError('Could not reach the payment provider', {
      status: 502,
      code: 'upstream_unreachable',
    });
  } finally {
    clearTimeout(timer);
  }
}

/**
 * Initiate a mobile money charge.
 *
 * IMPORTANT: this does not complete the payment. Paystack returns an
 * authorization_url and the customer must open it on their device to enter
 * their PIN. There is no silent STK push from this endpoint.
 */
export async function initializeMobileMoneyCharge({
  email,
  amount,
  currency,
  phone,
  provider,
  reference,
}) {
  const payload = {
    email,
    amount: toSubunits(amount, currency),
    currency,
    reference,
    channels: ['mobile_money'],
    mobile_money: { phone, provider },
    metadata: { source: 'rpai-give-page' },
  };

  const result = await paystackRequest('/charge', { method: 'POST', body: payload });

  return {
    reference: result.data?.reference ?? reference,
    authorizationUrl: result.data?.authorization_url ?? null,
    accessCode: result.data?.access_code ?? null,
    status: result.data?.status ?? 'pending',
    raw: result.data,
  };
}

/**
 * Authoritative confirmation source, used by the webhook and as a safety net
 * when a webhook is missed.
 */
export async function verifyCharge(reference) {
  const result = await paystackRequest(
    `/charge/verify/${encodeURIComponent(reference)}`
  );
  return result.data ?? null;
}

/**
 * Reports what the live account is actually enabled for. Use this to confirm
 * the currency before taking real money rather than trusting documentation.
 */
export async function getCapabilities() {
  const [banks, countries] = await Promise.all([
    paystackRequest('/bank').catch(() => null),
    paystackRequest('/country').catch(() => null),
  ]);

  const zambia = countries?.data?.find((c) => c.country === 'Zambia') ?? null;

  return {
    apiBase: config.paystack.baseUrl,
    mode: config.paystack.secretKey.startsWith('sk_live') ? 'live' : 'test',
    configuredCurrency: config.paystack.currency,
    // Paystack exposes supported settlement currencies per bank, not as a flat
    // list, so this is the reliable way to see whether ZMW is enabled.
    currenciesByBank: (banks?.data ?? []).map((b) => ({
      bank: b.name,
      currency: b.currency,
      supported: b.active,
      countries: b.country,
    })),
    zambia: zambia
      ? { supported: zambia.is_supported, currency: zambia.currency }
      : null,
  };
}