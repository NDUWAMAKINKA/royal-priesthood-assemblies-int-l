# RPAI Giving API

Payment backend for the Give page. **This does not run on GitHub Pages** —
GitHub Pages hosts static files only. Deploy this folder to a host that runs
Node (Render, Railway, Fly.io, Cloud Run, or your own VPS).

Production deployment is prepared for **Render + Supabase Postgres**. See
`../DEPLOY-RENDER.md` for the Blueprint, environment variables and webhook URL.

## Why it cannot live in the site folder

The Give page is static HTML. A payment endpoint needs a running server that
can hold `PAYSTACK_SECRET_KEY` in memory. If that key were in the HTML, every
visitor could read it from View Source.

So: **site on GitHub Pages, API anywhere that runs Node.** The browser calls
the API directly; the API calls Paystack.

---

## 1. Run it locally

```bash
cd server
npm install
cp .env.example .env      # then fill in your secret key
npm run dev
```

## 2. Confirm ZMW is actually enabled on your account

```bash
curl http://127.0.0.1:3000/api/capabilities
```

Read the `zambia.supported` field. If it is `false`, Paystack cannot charge
ZMW and none of this will work until you contact Paystack support or switch
settlement currency.

---

## 3. Register the webhook

Dashboard → Settings → API Keys & Webhooks, set the URL to:

```
https://your-api-host/api/webhook
```

Subscribe to `charge.success` and `charge.failed`.

---

## 4. Flow

```
Browser                     API                        Paystack
   |  POST /api/charge        |                            |
   |------------------------->|  POST /charge              |
   |                          |--------------------------->|
   |  { authorization_url }   |  { authorization_url }    |
   |<-------------------------|                            |
   |                                                          |
   |  donor opens authorization_url, enters PIN               |
   |--------------------------------------------------------->|
   |                             |  charge.success webhook    |
   |                             |<---------------------------|
   |  GET /api/payments/:ref     |                            |
   |------------------------->->|  (webhook already recorded)|
```

The **webhook is the authoritative confirmation**. Client polling is only a
convenience for the donor's screen, and it re-verifies against Paystack rather
than trusting local state.

---

## 5. Endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/charge` | Start a mobile money charge, or record a bank transfer intent |
| POST | `/api/webhook` | Paystack events (HMAC verified) |
| GET | `/api/payments/:reference` | Status for the donor's screen |
| GET | `/api/bank-transfer` | Bank details for the fallback card |
| GET | `/api/capabilities` | Live check of enabled currencies/countries |
| GET | `/api/health` | Liveness |

---

## 6. What the code handles for you

- **Minor units** use `PAYSTACK_CURRENCY_EXPONENT`, confirmed for the live
  provider account. Set `0` or `2`; a wrong value changes the charge by 100x.
- **Phone normalisation** accepts `0971234567` or `+260971234567`.
- **HMAC-SHA512 webhook verification** with constant-time compare, using the
  raw request body.
- **Idempotency** via `Idempotency-Key` so a double tap cannot create two
  charges.
- **Strict account-name validation** — the bank card refuses to render if any
  field is still a placeholder.
- **Rate limiting** and a strict CORS allow-list.

---

## 7. Production storage

The payment store now uses Supabase Postgres. The schema is in
`server/sql/001_init.sql` and is applied with:

```bash
npm run db:migrate
```

The Render start command runs the migration before the API starts. Payments,
idempotency responses and webhook audit events survive restarts and are shared
by every API instance.

## 8. Before production

1. Put a real rate limiter (Redis) in front; the in-memory one is per-instance.
2. Add your confirmation email in the webhook handler, queued not inline.
3. Set `PAYSTACK_WEBHOOK_SECRET` to the secret key's companion value from the
   dashboard.
4. Confirm `PAYSTACK_CURRENCY_EXPONENT` with Paystack before taking live money.
5. Never deploy `.env`; `server/.env` is gitignored.
6. Do not use this module for anything else without review — it holds the key
   to real money.