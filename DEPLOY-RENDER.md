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
3. Waits for the GitHub Pages workflow run for that exact commit to finish
   successfully, and for `/api/health` on the API to report the same commit.
4. Exits `0` on success, `1` when a deploy finishes unsuccessfully or times
   out, and `2` for a preflight problem.

The frontend check is a real proof, not a page fetch: GitHub Pages reports the
commit it built, and `server/src/index.js` returns `RENDER_GIT_COMMIT` from
`/api/health`.

If the website ever moves from GitHub Pages to the Render static site, set
`SITE_URL` in `.env.deploy`. `scripts/build-static.mjs` then writes
`dist/deploy-info.json` with the built commit, and `deploy.py` checks that
file instead.

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

1. Open `https://rpai-give-api.onrender.com/api/health`. It should return
   `{"ok":true,"db":"ok",...}`.
2. If Render gives the static site a different URL, update `ALLOWED_ORIGIN` on
   the API to include it.
3. In Paystack, set the webhook URL to
   `https://rpai-give-api.onrender.com/api/webhook`.
4. Open the static site and confirm the church pages load from Render.
5. The Give page still shows the verified static details. It does not silently
   start charging anyone. A payment form must be added and reviewed before the
   API is used by donors.

## 4. Frontend API base

The payment controller in `server/public/js__give.js` defaults to:

```text
https://rpai-give-api.onrender.com
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
