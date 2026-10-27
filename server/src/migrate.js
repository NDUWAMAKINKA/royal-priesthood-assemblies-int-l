import 'dotenv/config';
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { closeDb, pool } from './db.js';

const here = path.dirname(fileURLToPath(import.meta.url));
const sqlDir = path.join(here, '..', 'sql');

try {
  const files = (await readdir(sqlDir))
    .filter((name) => name.endsWith('.sql'))
    .sort();

  if (!files.length) {
    console.log('[db] no SQL migrations found');
  }

  for (const file of files) {
    const sql = await readFile(path.join(sqlDir, file), 'utf8');
    console.log(`[db] applying ${file}`);
    await pool.query(sql);
  }
  console.log('[db] migrations complete');
} catch (err) {
  console.error('[db] migration failed:', err.message);
  process.exitCode = 1;
} finally {
  await closeDb().catch(() => {});
}
