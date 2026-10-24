/**
 * Canonical payment status and transition rules.
 *
 * The provider's raw status is retained for audit, but the platform uses one
 * small vocabulary so a late failure cannot overwrite a success and a late
 * success can still be honoured.
 */

export const PENDING = 'pending';
export const SUCCESS = 'success';
export const FAILED = 'failed';
export const REVERSED = 'reversed';
export const REFUNDED = 'refunded';
export const CANCELLED = 'cancelled';
export const EXPIRED = 'expired';
export const DISPUTED = 'disputed';
export const AWAITING_TRANSFER = 'awaiting_transfer';

const TERMINAL = new Set([SUCCESS, FAILED, REVERSED, REFUNDED, CANCELLED, EXPIRED]);

const ALLOWED = {
  [PENDING]: new Set([PENDING, SUCCESS, FAILED, CANCELLED, EXPIRED, REVERSED]),
  [AWAITING_TRANSFER]: new Set([
    AWAITING_TRANSFER,
    SUCCESS,
    FAILED,
    CANCELLED,
    EXPIRED,
  ]),
  [SUCCESS]: new Set([SUCCESS, REFUNDED, REVERSED, DISPUTED]),
  [FAILED]: new Set([FAILED, SUCCESS]),
  [REVERSED]: new Set([REVERSED]),
  [REFUNDED]: new Set([REFUNDED, DISPUTED]),
  [CANCELLED]: new Set([CANCELLED, SUCCESS]),
  [EXPIRED]: new Set([EXPIRED, SUCCESS, FAILED]),
  [DISPUTED]: new Set([DISPUTED, SUCCESS, REFUNDED, FAILED]),
};

export function normalizeStatus(raw) {
  const value = String(raw ?? '').trim().toLowerCase();
  switch (value) {
    case 'success':
    case 'successful':
    case 'completed':
    case 'paid':
      return SUCCESS;
    case 'failed':
    case 'failure':
    case 'declined':
      return FAILED;
    case 'reversed':
    case 'reversal':
      return REVERSED;
    case 'refunded':
    case 'refund':
      return REFUNDED;
    case 'cancelled':
    case 'canceled':
    case 'abandoned':
      return CANCELLED;
    case 'expired':
    case 'timed_out':
      return EXPIRED;
    case 'disputed':
    case 'chargeback':
      return DISPUTED;
    case 'awaiting_transfer':
      return AWAITING_TRANSFER;
    case 'pending':
    case 'ongoing':
    case 'processing':
    case 'queued':
    case 'send_pin':
    case 'send_otp':
    case 'send_phone':
    case 'send_birthday':
      return PENDING;
    default:
      return PENDING;
  }
}

export function isTerminal(status) {
  return TERMINAL.has(normalizeStatus(status));
}

/**
 * Decide whether a status change is allowed.
 *
 * Late success is deliberately allowed from failed/cancelled/expired because
 * the provider may confirm a debit after a timeout. Success can never be
 * overwritten by a failure or by "pending".
 */
export function decideTransition(currentRaw, nextRaw) {
  const current = normalizeStatus(currentRaw);
  const next = normalizeStatus(nextRaw);

  if (current === next) {
    return { allowed: true, changed: false, lateSuccess: false, current, next };
  }

  const allowed = ALLOWED[current]?.has(next) ?? false;
  if (!allowed) {
    return {
      allowed: false,
      changed: false,
      lateSuccess: false,
      current,
      next,
      reason: `illegal_transition_${current}_to_${next}`,
    };
  }

  const lateSuccess =
    next === SUCCESS && [FAILED, CANCELLED, EXPIRED].includes(current);

  return { allowed: true, changed: true, lateSuccess, current, next };
}
