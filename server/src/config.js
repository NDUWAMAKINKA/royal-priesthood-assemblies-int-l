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
 * ZMW and XOF are whole-unit currencies (exponent 0) - there is no "kobo"
 * equivalent, so a charge of 50 ZMW must be sent as "50", never "5000".
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

export const config = {
  env: process.env.NODE_ENV || 'development',
  port: Number(process.env.PORT || 3000),

  paystack: {
    secretKey: required('PAYSTACK_SECRET_KEY'),
    // The API base is api.paystack.co. paystack.co is the dashboard website.
    baseUrl: 'https://api.paystack.co',
    currency: (process.env.PAYSTACK_CURRENCY || 'ZMW').toUpperCase(),
    timeoutMs: 20_000,
  },

  allowedOrigin: process.env.ALLOWED_ORIGIN || 'http://127.0.0.1:8123',
  publicSiteUrl: process.env.PUBLIC_SITE_URL || 'http://127.0.0.1:8123',
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

if (config.paystack.secretKey.startsWith('sk_live') && config.env === 'production') {
  // Not an error, just a loud reminder that live keys are now in play.
  console.warn('[config] Using a LIVE Paystack key. Test carefully.');
}

export function toSubunits(amount, currency = config.paystack.currency) {
  const exponent = SUBUNIT_EXPONENTS[currency];
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
  const exponent = SUBUNIT_EXPONENTS[currency] ?? 2;
  return Number(subunits) / 10 ** exponent;
}