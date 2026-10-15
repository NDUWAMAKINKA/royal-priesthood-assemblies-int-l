import { config } from './config.js';
import { bankDetailsArePublishable } from './validation.js';

const WARNING =
  'The account name must match exactly or banks will reject or return the transfer.';

/**
 * Bank transfer is a fallback path. Nothing is charged through the API; the
 * donor is shown the exact details and pays from their own banking app, then
 * the church matches the transfer against its statement using the reference.
 */
export function buildBankTransferInstructions() {
  if (!bankDetailsArePublishable(config.bank)) {
    return {
      available: false,
      warning:
        'Bank transfer details are not published yet. Please use mobile money or contact the church.',
      partialFields: Object.entries(config.bank)
        .filter(([, v]) => !v || v.toLowerCase() === 'to be confirmed')
        .map(([k]) => k),
    };
  }

  return {
    available: true,
    warning: WARNING,
    bank: {
      name: config.bank.name,
      accountName: config.bank.accountName,
      accountNumber: config.bank.accountNumber,
      swift: config.bank.swift,
      branch: config.bank.branch,
      address: config.bank.address,
    },
  };
}

/**
 * A donor choosing bank transfer still leaves us something to reconcile. We log
 * the intent server-side and return the reference the donor should quote.
 */
export function recordBankTransferIntent({ email, amount, reference }) {
  return {
    method: 'bank_transfer',
    reference,
    email,
    amount,
    status: 'awaiting_transfer',
    recordedAt: new Date().toISOString(),
    next: 'Donor pays from their banking app, then quotes the reference when contacting the church.',
  };
}