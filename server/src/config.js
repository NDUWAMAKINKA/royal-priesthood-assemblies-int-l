import 'dotenv/config';

function required(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

/**
 * Minor-unit exponents, taken from ISO 4217.
 *
 * The configured currency's exponent can be overridden with
 * PAYSTACK_CURRENCY_EXPONENT because the provider's interpretation must be
 * confirmed against the live account. Getting this wrong changes the charge by
 * a factor of 100.
 */
export const SUBUNIT_EXPONENTS = {
  ZMW: 0,
  XOF: 0,
  NGN: 2,
  ZAR: 2,
  GHS: 2,
  KES: 2,
  EGP: 2,
  RWF: 0,
};

const configuredCurrency = (process.env.PAYSTACK_CURRENCY || 'ZMW').toUpperCase();
const exponentRaw = process.env.PAYSTACK_CURRENCY_EXPONENT;
const currencyExponent =
  exponentRaw === undefined || exponentRaw === '' ? 0 : Number(exponentRaw);

if (![0, 2].includes(currencyExponent)) {
  throw new Error(
    'PAYSTACK_CURRENCY_EXPONENT must be 0 or 2, confirmed against your provider account'
  );
}
if (exponentRaw === undefined || exponentRaw === '') {
  console.warn(
    '[config] PAYSTACK_CURRENCY_EXPONENT is not set; using 0. Confirm this with Paystack before taking live payments.'
  );
}

function parseOrigins(value) {
  return String(value || '')
    .split(',')
    .map((origin) => origin.trim())
    .filter(Boolean)
    .map((origin) => (origin.startsWith('http') ? origin : `https://${origin}`));
}

const publicSiteUrl =
  process.env.PUBLIC_SITE_URL ||
  'https://royal-priesthood-assemblies-int-l-1.onrender.com';

const allowedOrigins = parseOrigins(
  process.env.ALLOWED_ORIGIN ||
    [
      'http://127.0.0.1:8123',
      'http://localhost:8123',
      'https://nduwamakinka.github.io',
      'https://royal-priesthood-assemblies-int-l-1.onrender.com',
      'https://rpai-church-site.onrender.com',
    ].join(',')
);

// Whatever site is declared as the public one must always be able to call the
// API, even if ALLOWED_ORIGIN was set earlier and not updated since the move.
if (publicSiteUrl && !allowedOrigins.includes(publicSiteUrl)) {
  allowedOrigins.push(publicSiteUrl);
}

const minAmount = Number(process.env.PAYSTACK_MIN_AMOUNT || 1);
const maxAmount = Number(process.env.PAYSTACK_MAX_AMOUNT || 1_000_000);
const operators = (process.env.PAYSTACK_OPERATORS || 'mtn,airtel')
  .split(',')
  .map((operator) => operator.trim().toLowerCase())
  .filter(Boolean);

if (!Number.isFinite(minAmount) || minAmount <= 0) {
  throw new Error('PAYSTACK_MIN_AMOUNT must be a positive number');
}
if (!Number.isFinite(maxAmount) || maxAmount < minAmount) {
  throw new Error('PAYSTACK_MAX_AMOUNT must be a number at least the minimum');
}
if (!operators.length) {
  throw new Error('PAYSTACK_OPERATORS must contain at least one provider');
}

export const config = {
  env: process.env.NODE_ENV || 'development',
  port: Number(process.env.PORT || 3000),

  // Render injects the deployed commit at build time. scripts/deploy.py reads
  // it from /api/health to prove the instance matches what was pushed.
  deployedCommit:
    process.env.RENDER_GIT_COMMIT || process.env.GIT_COMMIT || 'unknown',

  paystack: {
    secretKey: required('PAYSTACK_SECRET_KEY'),
    // The API base is api.paystack.co. paystack.co is the dashboard website.
    baseUrl: 'https://api.paystack.co',
    currency: configuredCurrency,
    currencyExponent,
    minAmount,
    maxAmount,
    operators,
    timeoutMs: 20_000,
  },

  allowedOrigins,
  // Kept for callers that only need the primary origin (for example logs).
  allowedOrigin: allowedOrigins[0] || 'http://127.0.0.1:8123',
  publicSiteUrl,
  allowedCountries: (process.env.ALLOWED_COUNTRIES || 'ZM')
    .split(',')
    .map((c) => c.trim().toUpperCase())
    .filter(Boolean),

  bank: {
    name: process.env.BANK_NAME || '',
    accountName: process.env.BANK_ACCOUNT_NAME || '',
    accountNumber: process.env.BANK_ACCOUNT_NUMBER || '',
    swift: process.env.BANK_SWIFT || '',
    branch: process.env.BANK_BRANCH || '',
    address: process.env.BANK_ADDRESS || '',
  },
};

if (
  config.paystack.secretKey.startsWith('sk_live') &&
  config.env === 'production'
) {
  // Not an error, just a loud reminder that live keys are now in play.
  console.warn('[config] Using a LIVE Paystack key. Test carefully.');
}

function exponentFor(currency) {
  if (currency === config.paystack.currency) {
    return config.paystack.currencyExponent;
  }
  return SUBUNIT_EXPONENTS[currency];
}

export function toSubunits(amount, currency = config.paystack.currency) {
  const exponent = exponentFor(currency);
  if (exponent === undefined) {
    throw new Error(`Unknown currency "${currency}" - add it to SUBUNIT_EXPONENTS`);
  }
  const value = Math.round(Number(amount) * 10 ** exponent);
  if (!Number.isFinite(value) || value <= 0) {
    throw new Error('Amount must be a positive number');
  }
  return String(value);
}

export function fromSubunits(subunits, currency = config.paystack.currency) {
  const exponent = exponentFor(currency) ?? 2;
  return Number(subunits) / 10 ** exponent;
}
