# SITEMAP & LINK STRUCTURE
### Royal Priesthood Assemblies International

This document lists every page, every link, and what each one is **for**.
It is a planning reference — nothing here changes the live site.

Generated from an audit of the 9 HTML pages in the project root.

---

## 1. SITE STRUCTURE AT A GLANCE

```
royalpriesthood/
│
├── index.html .................. Home
├── about.html .................. About the church
├── ministry.html ............... Ministries & Fellowships
├── gallery.html ................ Gallery & Media
│   ├── #photos ................. Sunday gallery (photo slider)
│   ├── #video ................. Service video
│   ├── #audio ................. Worship audio          (placeholder)
│   └── #songs ................. Songs and downloads
├── daily-devotional.html ....... Daily Devotional
├── announcements.html .......... Announcements (local announcement.json)
├── branches-transport.html ..... Branches & Transport
├── give.html ................... Give
└── contact.html ................ Contact
    ├── #prayer-request ......... Prayer request form
    └── #connect-card ........... "I'm New Here" connect card
```

**9 pages total. All 9 are in the main menu. No page is orphaned** —
every page can be reached from every other page.

---

## 2. PRIMARY NAVIGATION (the 9 menu links)

These appear in the header menu **and** the mobile menu on **all 9 pages**.

Every page also carries the same language switcher: the five major Zambian
languages (Bemba, Nyanja, Tonga, Lozi, Tumbuka) and seven world languages
(English, French, German, Italian, Portuguese, Russian, Spanish). The choice is
remembered in the browser and translates the navigation plus the giving page
prompts and buttons. Church names, bank names and account names are never
translated.

| # | Link | Page | What it is for |
|---|------|------|----------------|
| 1 | Home | `index.html` | Front page. Hero welcome, Sunday service times, live-stream link, why-us values, CTA. The only page a visitor must see. |
| 2 | About | `about.html` | Who the church is, the founder, mission and vision, values. Builds trust for first-time visitors. |
| 3 | Ministries | `ministry.html` | The ministry/fellowship directory (Royal Men, Virtuous Women, NextGen Youth, Home Cells). Answers "where do I fit in?". |
| 4 | Gallery | `gallery.html` | Photos, video, worship audio and songs. Proves the church is real and active. A **slideshow that is always running** (Pause / Play / Previous / Next). **Show all pictures** lays every photo out at once; a **Back to slideshow** button sits above the grid and sticks to the top of the screen so the way out is always in reach. No photo count is shown. |
| 5 | Daily Devotional | `daily-devotional.html` | Daily faith reading. Brings people back daily — the main repeat-visit driver. |
| 6 | Announcements | `announcements.html` | The current church notice, rendered from `announcement.json` by `js__announcement.js`. A scheduled GitHub Action keeps the JSON in step with the church's Facebook Page. No Facebook login, iframe, cookie or browser-side third-party request is involved. |
| 7 | Branches & Transport | `branches-transport.html` | Branch/home-cell locations, Sunday transport, directions. Practical info people ask for most. |
| 8 | Give | `give.html` | Hero heading "Give". Zambian giving details: cards for Zanaco, Stanbic, Absa, FNB and Standard Chartered (account name, number and centre), mobile-money details for Airtel, MTN and Zamtel, plus PayPal as the only international gateway. PayPal details are shown as text, with no payment link. |
| 9 | Contact | `contact.html` | Prayer request form, "I'm New Here" card, map, address, phone, email. |

---

## 3. CROSS-PAGE CALL-TO-ACTION LINKS

These jump from one page straight into a specific block on another.

| Link | Used on | Where it lands | Why it's needed |
|------|---------|----------------|-----------------|
| `contact.html#connect-card` | index, ministry, branches-transport | The "I'm New Here" connect card | Lets "Plan Your Visit" and "Find a fellowship" buttons skip the Contact page top and open the right card. |
| `contact.html#prayer-request` | index | The prayer request form | The "Share a Prayer Request" button opens the actual form, not just the page. |

---

## 4. IN-PAGE SECTION LINKS (anchor targets)

| Anchor | Page | Section | Status |
|--------|------|---------|--------|
| `#live-service` | index | Live Service block (stream + service times) | Live |
| `#photos` | gallery | Sunday gallery | Live |
| `#video` | gallery | Service video | Live |
| `#songs` | gallery | Songs and downloads | Live |
| `#audio` | gallery | Worship audio | **Placeholder — heading and note only, no audio file** |
| `#prayer-request` | contact | Prayer request form | Live |
| `#connect-card` | contact | I'm New Here card | Live |

> Note: every page also has a `href="#"` burger button. That is the mobile
> menu toggle handled by JavaScript — it is not a real destination.

---

## 5. CONTACT LINKS

| Purpose | Link | Where used |
|---------|------|-----------|
| Church email | `mailto:royalpriesthoodassembliesintl@gmail.com` | All 9 footers + "email the church" on Give |
| Church phone | `tel:+260767716936` | Give, Branches & Transport |

---

## 6. EXTERNAL LINKS

### Social & community (appear in the footer of all 9 pages)

| Link | Purpose |
|------|---------|
| `facebook.com/p/ROYAL-Priesthood-100064645061857/` | Main church Facebook page |
| `youtube.com/@royalpriesthoodassemblies` | Church YouTube channel |
| `instagram.com/explore/search/...` | Church Instagram |
| `wa.me/260767716936?text=...` | WhatsApp — fastest reply channel for visitors |

### Purpose-specific external links

| Link | Page | Purpose |
|------|------|---------|
| `facebook.com/.../` (as "Stream live service") | index | Live service streaming |
| `youtube.com/watch?v=mwtbEGNABWU` | index, ministry | The one known working church video |
| `youtube.com/results?search_query=...service` | gallery | Service video search |
| `wa.me/...Sunday transport.` | branches-transport | WhatsApp specifically about Sunday transport |
| `google.com/maps/search/?api=1&query=Otwa Events...` | contact, branches | "Get directions" buttons |
| `read.rhapsodyofrealities.org/` | daily-devotional | Source of the daily reading |
| Apple Music / YouTube Music / Spotify (2 each) | gallery | Where to listen to worship music |

---

## 7. EMBEDDED CONTENT

| Embed | Page | Purpose |
|-------|------|---------|
| Local announcement card (`announcement.json` + `js__announcement.js`) | announcements | Shows the current church notice without a third-party embed |
| Google Map (iframe) | contact | Shows where the church is |

### Announcement sync

`.github/workflows/sync-announcements.yml` runs every 30 minutes and on demand. It calls the Facebook Graph API with the `FB_PAGE_ACCESS_TOKEN` repository secret and rewrites `announcement.json` only when the Page has a newer text post. The workflow skips photo-only posts and never overwrites a newer manual announcement. The browser never contacts Facebook; it fetches the committed JSON. Page ID `100064645061857` is built in. Setup and token instructions: `FACEBOOK-SYNC-SETUP.md`.

---

## 8. WHAT IS MISSING (recommended additions)

These do not exist yet. Each is listed with why it is worth adding.

| Missing item | Why it is needed |
|--------------|------------------|
| `sitemap.xml` | Tells Google every page. Smallest possible SEO win. |
| `robots.txt` | Controls how search engines crawl the site. |
| `404.html` | Visitors who hit a dead link currently see nothing helpful. |
| Privacy Policy page | The site embeds Google Maps, which may use cookies. A policy page is expected and builds trust. |
| Canonical URLs (`<link rel="canonical">`) | Prevents duplicate-content confusion in search results. |
| Open Graph tags | Without these, sharing the site on Facebook/WhatsApp shows no preview image or description. Important for a church shared heavily on WhatsApp. |
| Real audio in `#audio` | The gallery advertises worship audio but the section is empty. |
| Giving account numbers | **Not published yet.** The Give page lists the five Zambian banks and PayPal, but each bank card shows "To be confirmed" for the account number until the church office supplies verified details. Never guess or invent an account number. |

### Giving page (current state)

The Give page is fully localised to Zambia. It lists five bank cards — Zanaco,
Stanbic, Absa, FNB and Standard Chartered — each showing the account name
(**Dunamis International Gospel Centre**), the church centre and the account
number. Account numbers stay as "To be confirmed" until the church office
supplies verified details. Airtel, MTN and Zamtel mobile-money details are also
shown as "To be confirmed". PayPal is the only international gateway; its email
and account name are shown as non-clickable text until the office supplies
verified details.

The old Node + Express payment backend in `server/` is **not connected** to the
page and is no longer used by it. It should be retired or reviewed separately
before anything is deployed; its secrets remain server-side only.

**Never publish payment secrets** (for example a Paystack `sk_test_` / `sk_live_`
key) in this site. Only a hosted payment link may appear in a page.

**Consistent phone numbers:** resolved. The site uses one number only:
**+260 767 716 936** (also used for WhatsApp).

---

## 9. RECOMMENDED FINAL LINK MAP

If everything above is completed, the site would have this complete structure:

```
HOME ─┬─ About ──────── Founder, mission, vision, values
      ├─ Ministries ─── 6 ministry pages (see note)
      ├─ Gallery ──┬─ Photos
      │            ├─ Video
      │            ├─ Audio
      │            └─ Songs
      ├─ Daily Devotional
      ├─ Announcements
      ├─ Branches ─┬─ Locations
      │            └─ Transport
      ├─ Give
      └─ Contact ─┬─ Prayer request
                   └─ I'm New Here
```

**Note:** Ministries, Branches and Gallery currently keep everything on one
page each. Splitting them into individual pages (as above) is only worth doing
when each group has enough content to stand on its own. At the current content
level, the single-page versions are fine and load faster.

---

*Document covers all 9 pages, 11 anchor targets, 2 cross-page CTAs,
10 email links, 2 phone links, 15 external destinations and 2 embeds.*