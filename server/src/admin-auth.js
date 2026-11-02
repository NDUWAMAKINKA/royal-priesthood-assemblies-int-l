import crypto from 'node:crypto';

import { config } from './config.js';

/**
 * Password login for /admin.
 *
 * The password is never stored in, or sent back to, the browser. A successful
 * login returns a signed, expiring token. The token is held in sessionStorage
 * and sent as a Bearer header. That keeps the admin routes stateless (no
 * session table) without weakening the password check.
 */

const TOKEN_TTL_MS =
  Math.max(1, Number(config.conference.adminTokenHours) || 8) * 60 * 60 * 1000;

export function adminConfigured() {
  return Boolean(
    config.conference.adminPassword && config.conference.adminSecret
  );
}

function digest(value) {
  return crypto.createHash('sha256').update(String(value)).digest();
}

export function passwordMatches(input) {
  if (!adminConfigured()) return false;
  const expected = digest(config.conference.adminPassword);
  const actual = digest(input);
  return (
    expected.length === actual.length &&
    crypto.timingSafeEqual(expected, actual)
  );
}

export function issueAdminToken() {
  const expiresAt = Date.now() + TOKEN_TTL_MS;
  const payload = `${expiresAt}.${crypto.randomBytes(16).toString('hex')}`;
  const encoded = Buffer.from(payload, 'utf8').toString('base64url');
  const signature = crypto
    .createHmac('sha256', config.conference.adminSecret)
    .update(payload)
    .digest('base64url');

  return {
    token: `${encoded}.${signature}`,
    expiresAt: new Date(expiresAt).toISOString(),
    expiresInSeconds: Math.floor(TOKEN_TTL_MS / 1000),
  };
}

export function verifyAdminToken(token) {
  if (!adminConfigured() || typeof token !== 'string') return null;

  const parts = token.split('.');
  if (parts.length !== 2) return null;

  let payload;
  try {
    payload = Buffer.from(parts[0], 'base64url').toString('utf8');
  } catch {
    return null;
  }

  const expected = crypto
    .createHmac('sha256', config.conference.adminSecret)
    .update(payload)
    .digest();
  let actual;
  try {
    actual = Buffer.from(parts[1], 'base64url');
  } catch {
    return null;
  }

  if (
    actual.length !== expected.length ||
    !crypto.timingSafeEqual(actual, expected)
  ) {
    return null;
  }

  const expiresAt = Number(payload.split('.')[0]);
  if (!Number.isFinite(expiresAt) || expiresAt <= Date.now()) return null;

  return { expiresAt };
}

export function requireAdmin(req, res, next) {
  if (!adminConfigured()) {
    return res.status(503).json({
      error: 'admin_not_configured',
      message:
        'The admin page is not configured yet. Set CONFERENCE_ADMIN_PASSWORD on the server.',
    });
  }

  const header = req.get('authorization') || '';
  const token = header.startsWith('Bearer ') ? header.slice(7).trim() : '';
  const session = verifyAdminToken(token);

  if (!session) {
    return res.status(401).json({
      error: 'unauthorized',
      message: 'Please sign in again.',
    });
  }

  req.adminSession = session;
  return next();
}
