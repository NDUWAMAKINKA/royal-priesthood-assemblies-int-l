# Render + Supabase deployment

## One command deploys both services

The website and the giving API are built from the same branch, so a single
push ships both: GitHub Pages republishes the site, and Render rebuilds the
API. `deploy.py` wraps that push and then waits until both really are serving
the new commit.

```bash
# Windows
deploy.bat

# Linux / macOS / Render shell
./deploy.sh

# Any platform, directly
python scripts/deploy.py
```

Typical use:

```bash
# Commit everything in the working tree with a message, push, wait, verify
python scripts/deploy.py -m "content: Sunday bulletin"

# Changes already committed - just push and verify
python scripts/deploy.py
```

What it does, in order:

1. Refuses to run on the wrong branch, behind `origin`, or with uncommitted
   changes that have no message.
2. Commits and pushes `main` (only when there is something to push).
3. Waits for the site build of that exact commit to finish successfully -
   Render's `/deploy-info.json` stamp when the site is served by Render, or
   the GitHub Pages workflow run - and for `/api/health` to report the same
   commit.
4. Exits `0` on success, `1` when a deploy finishes unsuccessfully or times
   out, and `2` for a preflight problem.

The frontend check is a real proof, not a page fetch:
`scripts/build-static.mjs` writes `dist/deploy-info.json` with the commit
Render built, GitHub Pages reports the commit it published, and
`server/src/index.js` returns `RENDER_GIT_COMMIT` from `/api/health`.

`deploy.py` uses the Render stamp whenever that site exists, and falls back to
the GitHub Pages build for the same commit. Set `SITE_URL` in `.env.deploy` if
the static site URL changes.

If the API has no live server yet, the command reports it and still succeeds -
the site is what visitors see. Pass `--require-backend` to make a missing API
a failure.

### Rebuild without a new commit

Grab each service's Deploy Hook in Render, put them in `.env.deploy` (see
`.env.deploy.example`), then:

```bash
python scripts/deploy.py --redeploy all
python scripts/deploy.py --redeploy frontend
python scripts/deploy.py --redeploy backend
```

### Useful flags

| Flag | Meaning |
|---|---|
| `-m, --message` | Commit pending changes with this message |
| `--branch` | Branch to deploy (default `main`) |
| `--frontend` | `auto`, `pages` or `stamp` - how the site is verified |
| `--require-backend` | Fail unless the API is live too |
| `--timeout` | Seconds to wait for the deploy (default `900`) |
| `--poll` | Seconds between checks (default `20`) |
| `--no-wait` | Push and exit without verifying |
| `--dry-run` | Show what would happen, change nothing |

Set `GITHUB_TOKEN` in `.env.deploy` if the anonymous GitHub API limit (60
requests per hour) is too low. A read-only token with no scopes is enough.

The first deploy still needs the one-time setup below.

---

This repository now contains two Render services in `render.yaml`:

| Service | Type | What it serves |
|---|---|---|
| `rpai-church-site` | Static site | The church website from the repository root |
| `rpai-give-api` | Node web service | The giving API in `server/` |

The giving API stores payments, idempotency keys and webhook audit events in
Supabase Postgres. None of the public pages read the database directly.

## 1. Supabase

The `public` schema has been created with:

- `payments`
- `idempotency_keys`
- `webhook_events`

Row-level security is enabled. The Node API connects with the database owner
through the Supabase session pooler. The browser-safe publishable key is not
used by the API and cannot read these tables.

To re-apply the schema:

```bash
cd server
npm install
npm run db:migrate
```

The connection string lives in `server/.env` locally and is **not committed**.
In Render, set it as `DATABASE_URL` in the `rpai-give-api` service.

## 2. Render Blueprint

Open:

<https://render.com/deploy?repo=https://github.com/NDUWAMAKINKA/royal-priesthood-assemblies-int-l>

Render reads `render.yaml` and asks for the values marked `sync: false`.

### Required API environment variables

| Variable | Value |
|---|---|
| `DATABASE_URL` | The Supabase session-pooler URL, ending in `?sslmode=require` |
| `DATABASE_SSL` | `true` |
| `PAYSTACK_SECRET_KEY` | The Paystack secret key for the church account |
| `PAYSTACK_WEBHOOK_SECRET` | The Paystack webhook secret, if configured separately |
| `PAYSTACK_CURRENCY` | `ZMW` |
| `PAYSTACK_CURRENCY_EXPONENT` | `0` or `2`, confirmed with Paystack before live payments |
| `ALLOWED_ORIGIN` | Comma-separated frontend origins |
| `PUBLIC_SITE_URL` | The final static-site URL |

Optional bank-transfer values are intentionally not in the Blueprint yet. The
API returns `available: false` and keeps the public page at **To be confirmed**
until verified details are added.

## 3. After the first deploy

1. Open `https://royal-priesthood-assemblies-int-l.onrender.com/api/health`.
   It should return `{"ok":true,"db":"ok","commit":"...","currency":"ZMW"}`.
2. If Render gives the static site a different URL, update `ALLOWED_ORIGIN` on
   the API to include it. The service currently answers CORS only for the
   origins in that variable, so a new frontend origin is blocked until it is
   added.
3. In Paystack, set the webhook URL to
   `https://royal-priesthood-assemblies-int-l.onrender.com/api/webhook`.
4. Open `https://royal-priesthood-assemblies-int-l-1.onrender.com/` and
   confirm the church pages load.
5. The Give page still shows the verified static details. It does not silently
   start charging anyone. A payment form must be added and reviewed before the
   API is used by donors.

## 4. Frontend API base

The payment controller in `server/public/js__give.js` defaults to:

```text
https://royal-priesthood-assemblies-int-l.onrender.com
```

A page can override it before the script loads:

```html
<script>
  window.RPAI_API_BASE = 'https://your-api-host.example';
</script>
```

The public church pages do not currently load the payment controller, so the
existing **To be confirmed** payment section is unchanged.

## 5. Security notes

- Never commit `server/.env`.
- Never put the Supabase `service_role`/secret key in HTML or JavaScript.
- The publishable key is browser-safe but is not needed by this API.
- Rotate the Supabase database password after it has been shared in chat, then
  update `DATABASE_URL` in Render and `server/.env`.
