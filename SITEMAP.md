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
├── announcements.html .......... Announcements (Facebook feed)
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

| # | Link | Page | What it is for |
|---|------|------|----------------|
| 1 | Home | `index.html` | Front page. Hero welcome, Sunday service times, live-stream link, why-us values, CTA. The only page a visitor must see. |
| 2 | About | `about.html` | Who the church is, the founder, mission and vision, values. Builds trust for first-time visitors. |
| 3 | Ministries | `ministry.html` | The ministry/fellowship directory (Royal Men, Virtuous Women, NextGen Youth, Home Cells). Answers "where do I fit in?". |
| 4 | Gallery | `gallery.html` | Photos, video, worship audio and songs. Proves the church is real and active. |
| 5 | Daily Devotional | `daily-devotional.html` | Daily faith reading. Brings people back daily — the main repeat-visit driver. |
| 6 | Announcements | `announcements.html` | Live Facebook page feed. Keeps visitors current without the church editing the site. |
| 7 | Branches & Transport | `branches-transport.html` | Branch/home-cell locations, Sunday transport, directions. Practical info people ask for most. |
| 8 | Give | `give.html` | Giving details and how to partner financially. |
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
| `facebook.com/.../` (as "Open the church's Facebook page") | announcements | Fallback if the embedded feed is blocked |
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
| Facebook page plugin (iframe) | announcements | Shows the church feed automatically |
| Google Map (iframe) | contact | Shows where the church is |

---

## 8. WHAT IS MISSING (recommended additions)

These do not exist yet. Each is listed with why it is worth adding.

| Missing item | Why it is needed |
|--------------|------------------|
| `sitemap.xml` | Tells Google every page. Smallest possible SEO win. |
| `robots.txt` | Controls how search engines crawl the site. |
| `404.html` | Visitors who hit a dead link currently see nothing helpful. |
| Privacy Policy page | The site loads the Facebook plugin and Google Maps, which use cookies. A policy page is expected and builds trust. |
| Canonical URLs (`<link rel="canonical">`) | Prevents duplicate-content confusion in search results. |
| Open Graph tags | Without these, sharing the site on Facebook/WhatsApp shows no preview image or description. Important for a church shared heavily on WhatsApp. |
| Real audio in `#audio` | The gallery advertises worship audio but the section is empty. |
| Giving payment details | **Not published yet.** The Give page intentionally shows "Number to be confirmed" and "To be confirmed" rather than live account details. The payment backend is built in `server/` and can be wired up when the church is ready. |

### Giving page (current state)

The Give page deliberately publishes **no live account details**. Mobile money
and bank cards show "Number to be confirmed" and "To be confirmed", and the
page points people to email or phone the church for verified details.

A payment backend already exists in `server/` (Node + Express, Paystack Charge
API with webhook confirmation and a bank-transfer fallback module). It is not
connected to the page, and the Paystack secret key lives only in the server
environment, never in HTML.

**Never publish the Paystack secret key** (`sk_test_` / `sk_live_`) in this
site. Only the public key (`pk_`) or a hosted payment link may appear in a page.
| Consistent phone numbers | Resolved. The site uses one number only: **+260 767 716 936** (also used for WhatsApp). |

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