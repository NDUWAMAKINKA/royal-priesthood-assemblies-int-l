# ROYAL PRIESTHOOD ASSEMBLIES INTERNATIONAL

Welcome to our official website! Here you can find information about our ministries, contact details, and more.

## About
ROYAL PRIESTHOOD ASSEMBLIES INTERNATIONAL, Lusaka, Zambia

## Contact
- Phone/WhatsApp: +260 767 716 936
- Email: royalpriesthoodassembliesintl@gmail.com

## What is on the site

| Page | Purpose |
|---|---|
| `index.html` | Home, service times, live service and online meeting links |
| `about.html` | Church story, founder, mission and values |
| `ministry.html` | Ministries and fellowships |
| `gallery.html` | Photos, video and worship audio |
| `library.html` | Searchable messages, worship recordings, videos, devotionals and meeting links |
| `daily-devotional.html` | Daily reading |
| `announcements.html` | Current notice from `announcement.json` |
| `branches-transport.html` | Branches, home cells and Sunday transport |
| `video-conference.html` | Embedded Jitsi meeting room and automatic email link requests |
| `give.html` | Zambian bank and mobile-money details |
| `contact.html` | Prayer request, connect card, map and contact details |

The online meeting is managed from the API host at
<https://royal-priesthood-assemblies-int-l.onrender.com/admin>. The pastor can
change the Jitsi room and schedule, review registrations and test email
delivery without editing any code. FreeConferenceCall is kept as an optional
backup link. See `VIDEO-CONFERENCE-SETUP.md` for the one-time setup and the
weekly routine.

---

This site is powered by [GitHub Pages](https://pages.github.com/) and uses the minimal Jekyll theme.

## Deployment

One command deploys the website and the giving API together, then verifies
both are live:

```bash
deploy.bat                                    # Windows
./deploy.sh                                   # Linux / macOS
python scripts/deploy.py -m "what changed"    # any platform
```

- The church website is served by Render at
  <https://royal-priesthood-assemblies-int-l-1.onrender.com> and mirrored on
  GitHub Pages.
- The giving API runs on Render at
  <https://royal-priesthood-assemblies-int-l.onrender.com> and stores payments
  in Supabase Postgres.
- Both deploy from `main` on every commit, so the frontend and backend never
  drift apart.

See `DEPLOY-RENDER.md` for the Blueprint, environment variables and the
flags `deploy.py` accepts.
