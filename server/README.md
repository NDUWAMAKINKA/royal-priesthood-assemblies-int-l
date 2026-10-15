# RPAI Giving API

Payment backend for the Give page. **This does not run on GitHub Pages** —
GitHub Pages hosts static files only. Deploy this folder to a host that runs
Node (Railway, Render, Fly.io, Railway, Cloud Run, or your own VPS).

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

- **Minor units** are ISO 4217 driven. ZMW exponent 0, so `50` ZMW is sent as
  `"50"`, never `"5000"`.
- **Phone normalisation** accepts `0971234567` or `+260971234567`.
- **HMAC-SHA512 webhook verification** with constant-time compare, using the
  raw request body.
- **Idempotency** via `Idempotency-Key` so a double tap cannot create two
  charges.
- **Strict account-name validation** — the bank card refuses to render if any
  field is still a placeholder.
- **Rate limiting** and a strict CORS allow-list.

---

## 7. Before production

1. Replace `store.js` with Postgres or Redis — the in-memory store loses
   payment state on restart.
2. Put a real rate limiter (Redis) in front; the in-memory one is per-instance.
3. Add your confirmation email in the webhook handler, queued not inline.
4. Set `PAYSTACK_WEBHOOK_SECRET` to the secret key's companion value from the
   dashboard.
5. Never deploy `.env`. Add `server/.env` and `server/node_modules` to
   `.gitignore`.
6. Do not use this module for anything else without review — it holds the key
   to real money.