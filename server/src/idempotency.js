import crypto from 'node:crypto';

/**
 * Canonical JSON and request fingerprints for idempotency.
 *
 * Two requests are the same only when the method, path and canonical body are
 * the same. Reusing a key with a different amount must fail, not silently
 * return the first response.
 */

export function stableStringify(value) {
  if (value === null || typeof value !== 'object') {
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) {
    return `[${value.map((item) => stableStringify(item)).join(',')}]`;
  }
  const keys = Object.keys(value).sort();
  return `{${keys
    .map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`)
    .join(',')}}`;
}

export function requestFingerprint({ method, path, body }) {
  const canonical = stableStringify({
    method: String(method || '').toUpperCase(),
    path: String(path || ''),
    body: body ?? null,
  });
  return crypto.createHash('sha256').update(canonical).digest('hex');
}

export function isValidIdempotencyKey(key) {
  return (
    typeof key === 'string' &&
    key.length >= 8 &&
    key.length <= 128 &&
    /^[A-Za-z0-9._:-]+$/.test(key)
  );
}
