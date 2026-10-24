/**
 * Money helpers.
 *
 * The important rule: never infer a currency's minor-unit exponent from the
 * currency code alone. ISO 4217 says ZMW has two decimal places, but some
 * payment providers treat it as whole units. The exponent must be confirmed
 * against the provider contract and set explicitly in configuration.
 */

export const ISO_EXPONENTS = Object.freeze({
  ZMW: 2,
  XOF: 0,
  NGN: 2,
  ZAR: 2,
  GHS: 2,
  KES: 2,
  EGP: 2,
  RWF: 0,
  USD: 2,
  EUR: 2,
  GBP: 2,
});

export function currencyCode(value) {
  const code = String(value || '').trim().toUpperCase();
  if (!code) throw new Error('Currency is required');
  return code;
}

export function isoExponent(currency) {
  const code = currencyCode(currency);
  if (!(code in ISO_EXPONENTS)) {
    throw new Error(`Unsupported currency "${code}"`);
  }
  return ISO_EXPONENTS[code];
}

/**
 * Parse an explicitly configured exponent.
 * Returns null when the value is missing, so the caller can decide whether
 * that is a startup error or a test default.
 */
export function parseExponent(value) {
  if (value === undefined || value === null || String(value).trim() === '') {
    return null;
  }
  const exponent = Number(value);
  if (!Number.isInteger(exponent) || exponent < 0 || exponent > 4) {
    throw new Error('Currency exponent must be an integer between 0 and 4');
  }
  return exponent;
}

export function resolveExponent(currency, configured) {
  const explicit = parseExponent(configured);
  return explicit === null ? isoExponent(currency) : explicit;
}

/**
 * Convert a major-unit amount (for example 250.50 ZMW) to integer minor units.
 * The exponent is passed explicitly; there is no hidden global default.
 */
export function toMinorUnits(amount, currency, exponent) {
  const code = currencyCode(currency);
  const exp = resolveExponent(code, exponent);
  const numeric =
    typeof amount === 'string'
      ? Number(amount.replace(/[,\s]/g, ''))
      : Number(amount);

  if (!Number.isFinite(numeric) || numeric <= 0) {
    throw new Error('Amount must be a positive number');
  }

  const factor = 10 ** exp;
  const minor = Math.round((numeric + Number.EPSILON) * factor);

  if (!Number.isSafeInteger(minor) || minor <= 0) {
    throw new Error('Amount is outside the supported range');
  }
  return minor;
}

export function fromMinorUnits(minor, currency, exponent) {
  const code = currencyCode(currency);
  const exp = resolveExponent(code, exponent);
  const value = Number(minor);
  if (!Number.isSafeInteger(value)) {
    throw new Error('Minor units must be a safe integer');
  }
  return value / 10 ** exp;
}

export function formatMinorUnits(minor, currency, exponent) {
  const code = currencyCode(currency);
  const exp = resolveExponent(code, exponent);
  return fromMinorUnits(minor, code, exp).toFixed(exp);
}
