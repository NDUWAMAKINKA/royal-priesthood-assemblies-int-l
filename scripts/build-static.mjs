import { cp, mkdir, readdir, rm } from 'node:fs/promises';
import path from 'node:path';

/**
 * Copy only the public website files into dist/ for Render's static site.
 * The repository root also contains the API, docs and (locally) the admin
 * bot. None of those belong in the published site.
 */
const root = process.cwd();
const out = path.join(root, 'dist');

const skippedDirectories = new Set([
  '.git',
  '.github',
  '.vscode',
  'admin-bot',
  'dist',
  'docs',
  'node_modules',
  'scripts',
  'server',
]);

const skippedFiles = new Set([
  '_config.yml',
  'check_html.py',
  'rename-manifest.txt',
  'render.yaml',
]);

function isWebsiteFile(name) {
  if (skippedFiles.has(name)) return false;
  if (name.endsWith('.md')) return false;
  if (name.endsWith('.py')) return false;
  if (name.endsWith('.before-markers')) return false;
  if (name.endsWith('.mp4')) return false;
  if (name.startsWith('WhatsApp ')) return false;
  if (name.startsWith('.') && name !== '.nojekyll') return false;
  return true;
}

await rm(out, { recursive: true, force: true });
await mkdir(out, { recursive: true });

let copied = 0;
for (const entry of await readdir(root, { withFileTypes: true })) {
  if (entry.isDirectory() && skippedDirectories.has(entry.name)) continue;
  if (entry.isFile() && !isWebsiteFile(entry.name)) continue;

  await cp(path.join(root, entry.name), path.join(out, entry.name), {
    recursive: true,
  });
  copied += 1;
}

console.log(`[static] copied ${copied} entries to dist/`);
