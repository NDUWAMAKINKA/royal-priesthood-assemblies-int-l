# Video conference and library

This adds two public pages and a small admin screen:

| Page | Address | What it does |
|---|---|---|
| Video Conference | `video-conference.html` | Embeds the Jitsi room and emails the room link to anyone who asks |
| Library | `library.html` | Searchable messages, worship recordings, videos and study links |
| Pastor's desk | `https://<api-host>/admin` | Lets the pastor set the room and see registrations without editing code |

The library is plain HTML and works without the API. The video conference page
uses the existing Render API, Supabase database and email delivery.

---

## The meeting platform: Jitsi Meet

Jitsi is the main room because it is genuinely free, needs no account, and can
be embedded inside the church page.

- **No account** for the pastor or the congregation.
- **No app** — it runs in the browser on a phone or computer.
- **More than 5 people** — 5–20 people is well within its normal range.
- **No per-meeting time limit** on the free public service.
- **No Host button** — the room opens when the first person joins. The pastor
  can join first to welcome people and keep order, but the meeting does not
  depend on the pastor starting it.
- **Screen sharing, chat, mute and a waiting/prejoin screen** are built in.

The free public service is `meet.jit.si`. Its terms provide the service **as
is**, with no uptime guarantee, and limit free use to **25 unique devices per
calendar month**. For a church with roughly 5–20 regular online attendees this
is normally enough. If the church grows past that, the options are a paid Jitsi
service, self-hosting, or moving to Daily.co's free minutes.

FreeConferenceCall is kept as an **optional backup link** for a very large
service or if Jitsi is ever unavailable. It is not required for normal use.

---

## One-time setup

### 1. Deploy the code

Push to `main` with the normal command:

```bash
deploy.bat
# or
python scripts/deploy.py -m "feat: Jitsi video conference and library"
```

Render runs `npm run db:migrate` before starting the API. That applies:

- `server/sql/002_conference.sql`
- `server/sql/003_jitsi.sql` — adds the Jitsi room column and gives the existing
  settings row a random room name such as `RPAI-Online-4F8A21C9`

### 2. Set the admin password

In Render → `rpai-give-api` → Environment:

| Variable | Value |
|---|---|
| `CONFERENCE_ADMIN_PASSWORD` | A long, unique passphrase for the pastor |
| `CONFERENCE_ADMIN_SECRET` | A separate random string used to sign the 8-hour login token |
| `CONFERENCE_ADMIN_TOKEN_HOURS` | `8` (optional) |

Generate the secret with:

```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

The pastor's page is:

```text
https://royal-priesthood-assemblies-int-l.onrender.com/admin
```

### 3. Choose an email transport

The Jitsi room itself needs no account. Email is only used to send the room
link to people who request it. Registration stays closed until email works.

#### Option A — Resend (recommended on Render)

1. Create a free account at <https://resend.com>.
2. Add and verify the church's sending domain (DNS records are shown in
   Resend).
3. Create an API key.
4. Set these Render variables:

```text
RESEND_API_KEY=re_...
MAIL_FROM=Royal Priesthood Assemblies International <meeting@your-verified-domain.org>
MAIL_REPLY_TO=royalpriesthoodassembliesintl@gmail.com
```

#### Option B — Gmail SMTP

1. Turn on 2-Step Verification for the church Google account.
2. Google Account → Security → App passwords → create one for "Mail".
3. Set these Render variables:

```text
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_SECURE=true
SMTP_USER=royalpriesthoodassembliesintl@gmail.com
SMTP_PASS=the 16-character app password
MAIL_FROM=Royal Priesthood Assemblies International <royalpriesthoodassembliesintl@gmail.com>
MAIL_REPLY_TO=royalpriesthoodassembliesintl@gmail.com
```

If port `465` is blocked, use `SMTP_PORT=587` and `SMTP_SECURE=false`.

### 4. Set the room

1. Open the admin page and sign in.
2. Under **Meeting details**, check the **Jitsi room name**. It starts as a
   random name such as `RPAI-Online-4F8A21C9`. Use **Generate** if you want a
   different one.
3. Add the title, host and time.
4. Leave **Allow people to request the link by email** ticked.
5. Save.
6. Send a test email from the **Help** tab.

The room is now live. No FreeConferenceCall account is needed.

---

## What the pastor does each week

1. Open the admin page on a phone or computer.
2. Sign in with the admin password.
3. Update the time, title or room name if needed.
4. Save.
5. Share the Video Conference page with the church (WhatsApp, Facebook, the
   announcement card, or the home page button).
6. At meeting time, open the Video Conference page and press **Join the
   meeting**. Join first if possible to welcome people. If the pastor is late,
   the room still starts for everyone else.

People who ask for the link are emailed automatically. The pastor can see who
registered, resend a link, remove a test entry, and export the list as CSV.

No one except the pastor (or someone with the admin password) can see the
registration list.

---

## Public page behaviour

The Video Conference page reads `GET /api/conference` and shows:

- the meeting title, host and schedule,
- the dial-in and access code only when the pastor fills the backup fields,
- a gold **Join the meeting** button,
- an embedded Jitsi room when the button is pressed,
- a backup FreeConferenceCall link when one is set,
- a registration form that posts to `POST /api/conference/register`.

The form:

- checks the email address,
- requires consent,
- has a hidden honeypot field for bots,
- limits one connection to five requests in ten minutes,
- stores the request in `conference_registrations`,
- emails the Jitsi room link,
- returns a friendly message either way.

When email is not configured, or the room is missing, the registration form
stays closed and the page says so. It does not collect addresses it cannot
reply to.

The Jitsi room is embedded with the official External API:

```html
<script src="https://meet.jit.si/external_api.js"></script>
```

The page loads that script only after the visitor presses **Join the meeting**,
so the rest of the page stays fast.

---

## Library

`library.html` contains six cards with real resources:

- a message from Apostle Dr. Mighty Zunga (`audio-message-5d1ec3.mp3`),
- three worship recordings,
- the service video on YouTube,
- the Sunday live stream on Facebook,
- the daily devotional,
- the online meeting page.

The search box and category buttons filter the cards in the browser. Every
audio player has `preload="none"`, so the large files are not downloaded until
someone presses play. There is also a download link beside each recording.

### Adding another item

The library is deliberately static, like the rest of the site, so adding an item
does not depend on the database being awake. To add one:

1. Put the audio or image file in the project root (or use an existing URL).
2. Copy one `<article class="rpai-library-card" ...>` block in `library.html`.
3. Give it a unique `data-category` (`messages`, `worship`, `video`, `devotion`
   or `meetings`) and a `data-search` string with the words people might type.
4. Change the title, description and media source.
5. Update the number in `Showing all 6 resources` if you add or remove a card.

Do not add a card without a working `src` or `href`. The point of the page is
that nothing on it is a placeholder.

---

## Troubleshooting

| Symptom | Check |
|---|---|
| Admin page says "not configured" | `CONFERENCE_ADMIN_PASSWORD` is missing on Render |
| Wrong password every time | The password was changed on Render; sign in again |
| Registration form is closed | Jitsi room missing, email not configured, or registration switched off |
| Test email fails | Provider key, verified domain, SMTP app password, and Render logs |
| Jitsi room does not load inside the page | Press **open it in a new tab**; allow camera/microphone; try Chrome or Firefox |
| Mobile camera does not work in the embedded room | Use the "open it in a new tab" link; some phone browsers restrict camera in iframes |
| Room asks for a name and camera | That is the Jitsi prejoin screen; enter a name and press Join |
| CORS error on the public page | Add the exact site origin to `ALLOWED_ORIGIN` on the API |
| Admin page loads without styling | The API is serving an old build; redeploy `rpai-give-api` |
| Public page says "Meeting details unavailable" | The API is asleep or unreachable; wait for Render to wake, then refresh |

Render free services sleep after inactivity. The first request can take a
minute. The rest of the site keeps working because it is static.

---

## Security notes

- The admin password is never stored in the browser. The browser holds a signed
  token that expires after eight hours.
- Passwords are compared in constant time.
- Login attempts are limited to ten per fifteen minutes per address.
- The registration list is protected by the admin token and row-level security.
- Meeting settings and registrations are never exposed by the public API.
- The Jitsi room name is random by default. It is not a password, but a random
  name makes it harder for a stranger to wander in. Use **Generate** if you
  need a new one.
- The backup FreeConferenceCall link is optional and only appears when set.
- Never commit `server/.env`, `RESEND_API_KEY`, `SMTP_PASS` or
  `CONFERENCE_ADMIN_PASSWORD`.
