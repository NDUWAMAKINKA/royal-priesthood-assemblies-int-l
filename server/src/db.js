import 'dotenv/config';
import pg from 'pg';

const { Pool } = pg;

const rawConnectionString = process.env.DATABASE_URL || '';
if (!rawConnectionString) {
  throw new Error('Missing required environment variable: DATABASE_URL');
}

/**
 * Supabase's pooler presents a certificate chain that Node does not always
 * trust by default. TLS is still required; only certificate verification is
 * relaxed for the managed pooler. Set DATABASE_SSL=false only for a local
 * Postgres that does not use TLS.
 *
 * The `sslmode` query parameter is removed because node-postgres v8 treats
 * `sslmode=require` as verify-full (and Supabase's chain then fails). The
 * connection is still encrypted by the ssl option below.
 */
const sslEnabled =
  String(process.env.DATABASE_SSL || 'true').toLowerCase() !== 'false';

let connectionString = rawConnectionString;
try {
  const parsed = new URL(rawConnectionString);
  parsed.searchParams.delete('sslmode');
  parsed.searchParams.delete('sslrootcert');
  parsed.searchParams.delete('sslcert');
  parsed.searchParams.delete('sslkey');
  connectionString = parsed.toString();
} catch {
  // Leave a non-URL DSN untouched; pg can still parse it.
}

export const pool = new Pool({
  connectionString,
  ssl: sslEnabled ? { rejectUnauthorized: false } : undefined,
  max: Number(process.env.PG_POOL_MAX || 10),
  idleTimeoutMillis: 30_000,
  connectionTimeoutMillis: 15_000,
});

pool.on('error', (err) => {
  // A failed idle client must not take the process down. The next query will
  // open a fresh connection.
  console.error('[db] idle client error:', err.message);
});

export function query(text, params) {
  return pool.query(text, params);
}

export async function withTransaction(fn) {
  const client = await pool.connect();
  try {
    await client.query('begin');
    const result = await fn(client);
    await client.query('commit');
    return result;
  } catch (err) {
    await client.query('rollback').catch(() => {});
    throw err;
  } finally {
    client.release();
  }
}

export function closeDb() {
  return pool.end();
}
