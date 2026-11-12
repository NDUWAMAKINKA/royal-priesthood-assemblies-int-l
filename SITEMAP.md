# SITEMAP & LINK STRUCTURE
### Royal Priesthood Assemblies International

This document lists the pages, navigation and major features of the rebuilt RPAI site.
The source of truth for the shared layout and page bodies is `scripts/build-site.py`.

Updated: 2026-11-12

---

## SITE STRUCTURE AT A GLANCE

```
royal priesthood/
├── index.html .................. Home
├── about.html .................. Our Story
├── senior-pastor.html .......... Senior Pastor
├── testimonies.html ............ Testimonies
├── ministry.html ............... Ministries
├── gallery.html ................ Media Gallery
├── impact.html ................. Our Impact
├── branches-transport.html ..... Visit Us
├── give.html ................... Give
├── daily-devotional.html ....... Daily Devotional
├── announcements.html ......... Announcements
├── contact.html ................ Contact Us
├── attend.html ................. I Am Attending (social card maker)
├── privacy.html ................ Privacy
├── terms.html .................. Terms of Use
└── library.html ................ Legacy redirect to Home
```

## PRIMARY NAVIGATION

Header (desktop): Home, Our Story, Senior Pastor, Testimonies, Ministries, Media Gallery, More ▾
CTA button: I Am Attending → attend.html

Mobile: burger menu with the same links, plus the I Am Attending CTA.

## FOOTER

Explore: Home, Our Story, Senior Pastor, Testimonies, Ministries, Media Gallery
Social: Facebook, YouTube, WhatsApp
Legal: Privacy, Terms

## PAGE PURPOSES

- `index.html`: Hero with phone mockup and photo cards, welcome, photo rail, Sunday service, visit, values, testimony preview, gallery preview, FAQ, CTA.
- `about.html`: Story, founder, mission/vision, values, timeline, CTA.
- `senior-pastor.html`: Apostle Dr. Mighty Zunga profile, ministry, values, CTA.
- `testimonies.html`: Filterable testimony wall, share form, CTA.
- `ministry.html`: Ministries directory, service doors, CTA.
- `gallery.html`: Filterable photo gallery, lightbox, media links, audio, CTA.
- `impact.html`: Impact areas, prayer, rhythm, CTA.
- `branches-transport.html`: Visit details, directions, transport, fellowships, FAQ, CTA.
- `give.html`: Giving information and channels, impact, CTA.
- `daily-devotional.html`: Devotional text, reading plan, CTA.
- `announcements.html`: Latest announcement from `announcement.json`, standing notices, CTA.
- `contact.html`: Prayer request and connect card forms, contact details, FAQ, CTA.
- `attend.html`: I Am Attending social card maker (canvas), Sunday details, FAQ, CTA.
- `privacy.html`: Privacy policy.
- `terms.html`: Terms of use.

## SHARED ASSETS

- `css__rpa30.css`: standalone design system for the rebuilt site.
- `js__rpa30.js`: header, mobile panel, More menu, reveals, rails, filters, lightbox, card maker, share buttons.
- `js__rpai.js`: mail-form handling and year stamp.
- `js__announcement.js`: announcement JSON loader.
- `js__conference.js`: conference API/Jitsi/registration behavior.
- `scripts/build-site.py`: generator for all shared-layout pages.

## NOT IN DIST

Keep `scripts/`, `site-src/` and other generator-only assets out of `dist/`. Run `node scripts/build-static.mjs` for production output.