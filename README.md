# ROYAL PRIESTHOOD ASSEMBLIES INTERNATIONAL

Welcome to our official website! Here you can find information about our ministries, contact details, and more.

## About
ROYAL PRIESTHOOD ASSEMBLIES INTERNATIONAL, Lusaka, Zambia

## Contact
- Phone/WhatsApp: +260 767 716 936
- Email: royalpriesthoodassembliesintl@gmail.com

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

- The church website is published to GitHub Pages from `main`.
- The giving API in `server/` runs on Render as `rpai-give-api` and stores
  payments in Supabase Postgres.
- Both deploy from `main` on every commit, so the frontend and backend never
  drift apart. A Render static site (`rpai-church-site`) is also defined in
  `render.yaml` and deploys on the same commit.

See `DEPLOY-RENDER.md` for the Blueprint, environment variables and the
flags `deploy.py` accepts.
