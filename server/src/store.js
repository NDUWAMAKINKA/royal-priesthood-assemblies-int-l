import { randomUUID } from 'node:crypto';

/**
 * Placeholder persistence. In production swap this for Postgres/Redis so the
 * store survives restarts and can be shared across instances. The interface is
 * deliberately small: idempotency guards and payment state only.
 */
const payments = new Map();
const idempotency = new Map();

const IDEMPOTENCY_TTL_MS = 15 * 60 * 1000;

function sweep() {
  const cutoff = Date.now() - IDEMPOTENCY_TTL_MS;
  for (const [key, entry] of idempotency) {
    if (entry.createdAt < cutoff) idempotency.delete(key);
  }
}

export function newReference(prefix = 'RPAI') {
  // Uppercase alphanumeric, easy for a donor to read out over the phone.
  const rand = randomUUID().replace(/-/g, '').slice(0, 16).toUpperCase();
  return `${prefix}_${rand}`;
}

export function beginIdempotent(key, response) {
  sweep();
  if (!key) return false;
  const existing = idempotency.get(key);
  if (existing) {
    Object.assign(response, existing.response);
    return true;
  }
  return false;
}

export function rememberIdempotent(key, response) {
  if (key) idempotency.set(key, { createdAt: Date.now(), response });
}

export function savePayment(payment) {
  payments.set(payment.reference, { ...payment, updatedAt: new Date().toISOString() });
  return payments.get(payment.reference);
}

export function updatePayment(reference, patch) {
  const current = payments.get(reference);
  if (!current) return null;
  const next = { ...current, ...patch, updatedAt: new Date().toISOString() };
  payments.set(reference, next);
  return next;
}

export function getPayment(reference) {
  return payments.get(reference) ?? null;
}

export function listPayments() {
  return [...payments.values()];
}