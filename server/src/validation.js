import { z } from 'zod';
import { config } from './config.js';

/**
 * Zambian mobile numbers are 10 digits starting 07/09, or already in
 * +260 form. Paystack expects an international or local format; we normalise
 * to +260 so both user input styles work.
 */
export const phoneSchema = z
  .string()
  .trim()
  .transform((raw) => raw.replace(/[\s()-]/g, ''))
  .refine((v) => /^\+260\d{9}$/.test(v) || /^0\d{9}$/.test(v), {
    message: 'Enter a valid Zambian mobile number, e.g. 0971234567 or +260971234567',
  })
  .transform((v) => (v.startsWith('0') ? `+260${v.slice(1)}` : v));

export const chargeSchema = z.object({
  email: z.string().trim().email('Enter a valid email address').max(254),
  amount: z.coerce
    .number()
    .positive('Amount must be greater than zero')
    .max(5_000_000, 'Amount is above the permitted maximum'),
  currency: z.string().trim().toUpperCase().default(config.paystack.currency),

  method: z.enum(['mobile_money', 'bank_transfer'], {
    errorMap: () => ({ message: 'Choose either mobile_money or bank_transfer' }),
  }),

  // Required only for mobile money; stripped for bank transfer.
  mobile_money: z
    .object({
      phone: phoneSchema,
      provider: z.enum(['mtn', 'airtel'], {
        errorMap: () => ({ message: 'Provider must be "mtn" or "airtel"' }),
      }),
    })
    .optional(),

  /**
   * Bank transfers are paid by the customer out of band. We record the intent
   * so the church has a reference to match against the bank statement, but we
   * never submit anything to Paystack.
   */
  reference: z.string().trim().max(64).optional(),
})
.superRefine((data, ctx) => {
  if (data.method === 'mobile_money' && !data.mobile_money) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      path: ['mobile_money'],
      message: 'A phone number and provider are required for mobile money',
    });
  }
  if (data.method === 'bank_transfer' && data.mobile_money) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      path: ['mobile_money'],
      message: 'Do not send mobile money details for a bank transfer',
    });
  }
});

/**
 * The bank card is only safe to render when the account name is an exact,
 * non-empty string. A truncated or placeholder name is how donors end up with
 * returned transfers, so we refuse to render rather than show it half-filled.
 */
export function bankDetailsArePublishable(bank) {
  const placeholders = new Set([
    '',
    'to be confirmed',
    'tbc',
    'pending',
    'n/a',
    'none',
  ]);
  const ok = (v) => typeof v === 'string' && !placeholders.has(v.trim().toLowerCase());
  return ok(bank.name) && ok(bank.accountName) && ok(bank.accountNumber);
}