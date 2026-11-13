#!/usr/bin/env python3
"""
Build the Royal Priesthood Assemblies International website.

The site keeps the phone-first architecture of the reference anniversary site:
a floating pill navigation, a dark gold design system, editorial sections,
a social-card maker, testimonies, a media gallery, impact, visits and contact.

Run from the repository root:

    python scripts/build-site.py

Generated pages are written to the repository root so the existing static
deployment (scripts/build-static.mjs) keeps working without a JavaScript
framework.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://royal-priesthood-assemblies-int-l-1.onrender.com"

CHURCH = "Royal Priesthood Assemblies International"
SHORT = "RPAI"
TAGLINE = "A place of love where everyone counts."
PHONE_DISPLAY = "+260 977 490 080"
PHONE_TEL = "+260977490080"
EMAIL = "royalpriesthoodassembliesintl@gmail.com"
ADDRESS = "Otwa Events, Long Acres, Ndeke Road, Lusaka, Zambia"
MAP_URL = "https://www.google.com/maps/search/?api=1&query=Otwa+Events%2C+Long+Acres%2C+Ndeke+Road%2C+Lusaka%2C+Zambia"
WHATSAPP = "https://wa.me/260977490080"
FACEBOOK = "https://www.facebook.com/p/ROYAL-Priesthood-100064645061857/"
YOUTUBE = "https://www.youtube.com/@royalpriesthoodassemblies"

YEAR = 2026

ICONS = {
    "arrow": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "play": '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5-11-6.5Z"/></svg>',
    "pin": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M12 21s7-5.2 7-11a7 7 0 1 0-14 0c0 5.8 7 11 7 11Z"/><circle cx="12" cy="10" r="2.6"/></svg>',
    "clock": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg>',
    "phone": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M6.6 3.8 4.2 5.6c-.8.6-1.1 1.7-.7 2.6 2.5 6.2 6.2 9.9 12.4 12.4.9.4 2 .1 2.6-.7l1.8-2.4c.4-.6.3-1.5-.3-1.9l-3.5-2.2c-.5-.3-1.2-.2-1.7.2l-1.6 1.5c-2.4-1.2-4.3-3.1-5.5-5.5l1.5-1.6c.4-.5.5-1.2.2-1.7L7.9 4.1c-.4-.6-1.3-.7-1.9-.3Z"/></svg>',
    "mail": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 7 8.5 6 8.5-6"/></svg>',
    "search": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    "chevron": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>',
    "close": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg>',
    "left": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>',
    "right": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg>',
    "upload": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 16V4m0 0L7 9m5-5 5 5"/><path d="M4 15v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/></svg>',
    "heart": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8l1.1 1.1L12 21l7.8-7.5 1.1-1.1a5.5 5.5 0 0 0-.1-7.8Z"/></svg>',
    "quote": '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M9.5 6C6.5 7.4 4.8 9.8 4.8 13v5h5.4v-5.4H7.5c0-2.2.9-3.7 2.9-4.7L9.5 6Zm9 0c-3 1.4-4.7 3.8-4.7 7v5h5.4v-5.4h-2.7c0-2.2.9-3.7 2.9-4.7L18.5 6Z"/></svg>',
    "whatsapp": '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 1.8a8.2 8.2 0 0 1 6.9 12.6l-.4.6.7 2.6-2.7-.7-.6.3A8.2 8.2 0 1 1 12 3.8Zm-3.1 4c-.2 0-.5.1-.7.4-.2.3-.9.9-.9 2.1s.9 2.4 1 2.6c.1.2 1.8 2.9 4.5 4 2.2.9 2.7.7 3.2.7.5-.1 1.6-.7 1.8-1.3.2-.6.2-1.2.2-1.3-.1-.1-.3-.2-.7-.4l-1.7-.8c-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1-.3-.1-1.2-.4-2.2-1.3-.8-.7-1.3-1.6-1.5-1.9-.1-.2 0-.4.1-.5l.4-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.2Z"/></svg>',
    "facebook": '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 22v-8h2.7l.4-3.1h-3.1V8.9c0-.9.3-1.5 1.6-1.5h1.6V4.6c-.3 0-1.3-.1-2.4-.1-2.4 0-4 1.4-4 4.1v2.3H7.5V14h2.8v8h3.2Z"/></svg>',
    "youtube": '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.6 7.2a2.7 2.7 0 0 0-1.9-1.9C18 4.8 12 4.8 12 4.8s-6 0-7.7.5a2.7 2.7 0 0 0-1.9 1.9C2 8.9 2 12 2 12s0 3.1.4 4.8a2.7 2.7 0 0 0 1.9 1.9c1.7.5 7.7.5 7.7.5s6 0 7.7-.5a2.7 2.7 0 0 0 1.9-1.9C22 15.1 22 12 22 12s0-3.1-.4-4.8ZM10 15.2V8.8l5.7 3.2-5.7 3.2Z"/></svg>',
    "copy": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3"/></svg>',
    "x": '<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.9 2H22l-6.8 7.8L23 22h-6.1l-4.8-6.3L6.6 22H3.5l7.3-8.3L2.8 2h6.2l4.3 5.7L18.9 2Zm-1.1 18h1.7L7.1 3.9H5.3L17.8 20Z"/></svg>',
    "bell": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M18 8a6 6 0 1 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/></svg>',
}

NAV = [
    ("index.html", "Home", "home"),
    ("about.html", "Our Story", "about"),
    ("senior-pastor.html", "Senior Pastor", "pastor"),
    ("testimonies.html", "Testimonies", "testimonies"),
    ("ministry.html", "Ministries", "ministries"),
    ("gallery.html", "Media Gallery", "gallery"),
]

MORE = [
    ("impact.html", "Our Impact", "impact"),
    ("branches-transport.html", "Visit Us", "visit"),
    ("give.html", "Give", "give"),
    ("daily-devotional.html", "Daily Devotional", "devotional"),
    ("announcements.html", "Announcements", "announcements"),
    ("contact.html", "Contact Us", "contact"),
]

ALL_NAV = NAV + MORE

PAGE_META = {
    "index": ("Royal Priesthood Assemblies International | A place of love where everyone counts", "A church family in Lusaka, Zambia, gathered around the Word, prayer and one another. Sunday Divine Service at 09:00 AM.", "hero-about.webp"),
    "about": ("Our Story | Royal Priesthood Assemblies International", "The story of Royal Priesthood Assemblies International: a people of faith, rooted in the Word and growing together in Lusaka, Zambia.", "hero-story.webp"),
    "pastor": ("Our Senior Pastor | Apostle Dr. Mighty Zunga", "Meet Apostle Dr. Mighty Zunga, Founder and General Overseer of Royal Priesthood Assemblies International.", "hero-pastor.webp"),
    "testimonies": ("Testimonies | Royal Priesthood Assemblies International", "Stories of God's faithfulness from the Royal Priesthood family, and a place to share what He has done for you.", "hero-testimonies.webp"),
    "ministries": ("Ministries & Fellowships | Royal Priesthood Assemblies International", "Royal Men's Fellowship, Virtuous Women's Ministry, NextGen Youth & Teen Ministry, and Home Cell & Branch Fellowships.", "hero-ministry.webp"),
    "gallery": ("Media Gallery | Royal Priesthood Assemblies International", "Photographs, worship and messages from the life of Royal Priesthood Assemblies International.", "hero-gallery.webp"),
    "impact": ("Our Impact | Royal Priesthood Assemblies International", "Grace that reaches beyond the walls: worship, discipleship, fellowship and practical care in Lusaka and beyond.", "hero-impact.webp"),
    "visit": ("Plan Your Visit | Royal Priesthood Assemblies International", "Service times, directions, transport and a warm welcome at Otwa Events, Long Acres, Lusaka.", "hero-branches.webp"),
    "give": ("Give | Royal Priesthood Assemblies International", "Partner with the ministry of the Word, prayer, discipleship and practical care at RPAI.", "hero-give.webp"),
    "devotional": ("Daily Devotional | Royal Priesthood Assemblies International", "Start today with God's Word. A daily devotional rhythm from Royal Priesthood Assemblies International.", "hero-devotional.webp"),
    "announcements": ("Announcements | Royal Priesthood Assemblies International", "The latest news and notices from the Royal Priesthood family.", "hero-announcements.webp"),
    "contact": ("Contact Us | Royal Priesthood Assemblies International", "Talk to us, send a prayer request, or find directions to Otwa Events, Long Acres, Lusaka.", "hero-contact.webp"),
    "attend": ("I Am Attending | Royal Priesthood Assemblies International", "Make your own I Am Attending card, then join us this Sunday at 09:00 AM in Lusaka.", "hero-attend.webp"),
    "privacy": ("Privacy | Royal Priesthood Assemblies International", "How Royal Priesthood Assemblies International handles personal information.", "hero-library.webp"),
    "terms": ("Terms of Use | Royal Priesthood Assemblies International", "Terms of use for the Royal Priesthood Assemblies International website.", "hero-conference.webp"),
}

# The hero image each page actually paints, so preload and artwork always agree.
PAGE_HERO = {
    "index": "photos/hero-about.webp",
    "about": "photos/hero-story.webp",
    "pastor": "photos/hero-pastor.webp",
    "testimonies": "photos/hero-testimonies.webp",
    "ministries": "photos/hero-ministry.webp",
    "gallery": "photos/hero-gallery.webp",
    "impact": "photos/hero-impact.webp",
    "visit": "photos/hero-branches.webp",
    "give": "photos/hero-give.webp",
    "devotional": "photos/hero-devotional.webp",
    "announcements": "photos/hero-announcements.webp",
    "contact": "photos/hero-contact.webp",
    "attend": "photos/hero-attend.webp",
    "privacy": "photos/hero-library.webp",
    "terms": "photos/hero-conference.webp",
}


MORE_KEYS = {item[2] for item in MORE}


def nav_link(href: str, label: str, key: str, page: str) -> str:
    current = ' aria-current="page"' if page == key else ""
    return f'<a class="nav-link" href="{href}"{current}>{label}</a>'


def panel_link(href: str, label: str, key: str, page: str) -> str:
    current = ' aria-current="page"' if page == key else ""
    return f'<a href="{href}"{current}>{label}</a>'


def site_header(page: str) -> str:
    primary = "\n".join(nav_link(href, label, key, page) for href, label, key in NAV)
    more_current = " is-current" if page in MORE_KEYS else ""
    more_items = "\n".join(panel_link(href, label, key, page) for href, label, key in MORE)
    panel_items = "\n".join(panel_link(href, label, key, page) for href, label, key in NAV)
    panel_more = "\n".join(panel_link(href, label, key, page) for href, label, key in MORE)
    return f"""
<header class="site-header" data-site-header>
  <div class="nav-shell">
    <a class="brand" href="index.html" aria-label="{CHURCH} home">
      <span class="brand__mark"><img src="logo-rpai.png" alt="" width="38" height="38"></span>
      <span class="brand__text">
        <span class="brand__name">Royal Priesthood</span>
        <span class="brand__sub">Assemblies International</span>
      </span>
    </a>

    <nav class="nav-primary" aria-label="Primary">
      {primary}
      <div class="nav-more{more_current}" data-more>
        <button class="nav-more__toggle" type="button" data-more-toggle aria-expanded="false" aria-controls="more-menu">
          More <span class="nav-more__caret">{ICONS['chevron']}</span>
        </button>
        <div class="nav-more__menu" id="more-menu" data-more-menu>
          {more_items}
        </div>
      </div>
    </nav>

    <div class="nav-actions">
      <div class="rpai-lang-switcher notranslate" data-rpai-lang-switcher translate="no">
      					<button type="button" class="rpai-lang-toggle" data-rpai-lang-toggle aria-expanded="false" aria-haspopup="listbox" aria-controls="rpai-lang-menu" aria-label="Select language">
      						<span class="rpai-lang-globe" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.7 3.8 9S14.5 18.4 12 21c-2.5-2.6-3.8-5.7-3.8-9S9.5 5.6 12 3Z"/></svg></span>
      						<span class="rpai-lang-current" data-rpai-lang-current>English</span>
      						<span class="rpai-lang-chevron" aria-hidden="true"></span>
      					</button>
      					<div class="rpai-lang-menu" id="rpai-lang-menu" data-rpai-lang-menu role="listbox" aria-label="Select language" hidden>
      						<p class="rpai-lang-group" role="presentation"><img src="flag-zm.svg" alt="" aria-hidden="true" width="20" height="14" loading="lazy" decoding="async"> <span data-i18n="lang.zambian">Zambian languages</span></p>
      						<button type="button" role="option" data-lang="bem" aria-selected="false"> Bemba</button>
      						<button type="button" role="option" data-lang="nya" aria-selected="false"> Nyanja</button>
      						<button type="button" role="option" data-lang="toi" aria-selected="false"> Tonga</button>
      						<button type="button" role="option" data-lang="loz" aria-selected="false"> Lozi</button>
      						<button type="button" role="option" data-lang="tum" aria-selected="false"> Tumbuka</button>
      						<p class="rpai-lang-group" role="presentation" data-i18n="lang.world">World languages</p>
      					<button type="button" role="option" data-lang="en" aria-selected="true"><img src="flag-gb.svg" alt="" aria-hidden="true" width="20" height="14" loading="lazy" decoding="async"> English</button>
      
      <button type="button" role="option" data-lang="hi" aria-selected="false"><img src="flag-in.svg" alt="" aria-hidden="true" width="20" height="14" loading="lazy" decoding="async"> Hindi</button>
      
      <button type="button" role="option" data-lang="fr" aria-selected="false"><img src="flag-fr.svg" alt="" aria-hidden="true" width="20" height="14" loading="lazy" decoding="async"> French</button>
      
      <button type="button" role="option" data-lang="de" aria-selected="false"><img src="flag-de.svg" alt="" aria-hidden="true" width="20" height="14" loading="lazy" decoding="async"> German</button>
      
      <button type="button" role="option" data-lang="it" aria-selected="false"><img src="flag-it.svg" alt="" aria-hidden="true" width="20" height="14" loading="lazy" decoding="async"> Italian</button>
      
      <button type="button" role="option" data-lang="pt" aria-selected="false"><img src="flag-pt.svg" alt="" aria-hidden="true" width="20" height="14" loading="lazy" decoding="async"> Portuguese</button>
      
      <button type="button" role="option" data-lang="ru" aria-selected="false"><img src="flag-ru.svg" alt="" aria-hidden="true" width="20" height="14" loading="lazy" decoding="async"> Russian</button>
      
      <button type="button" role="option" data-lang="es" aria-selected="false"><img src="flag-es.svg" alt="" aria-hidden="true" width="20" height="14" loading="lazy" decoding="async"> Spanish</button>
      
      </div>
      				</div>
      <a class="btn btn-primary btn-sm nav-cta" href="attend.html">I am visiting church on Sunday</a>
      <button class="nav-burger" type="button" data-nav-toggle aria-expanded="false" aria-controls="nav-panel" aria-label="Open menu">
        <span class="nav-burger__box" aria-hidden="true"><span></span><span></span><span></span></span>
      </button>
    </div>

    <div class="nav-panel" id="nav-panel" data-nav-panel>
      <p class="nav-panel__group">Explore</p>
      {panel_items}
      <p class="nav-panel__group">Take part</p>
      {panel_more}
      <a class="nav-panel__cta" href="attend.html">I am visiting church on Sunday</a>
    </div>
  </div>
</header>
"""


def service_bar() -> str:
    return f"""
<div class="service-bar">
  <div class="container service-bar__inner">
    <span><strong>Sunday Divine Service</strong> 09:00 AM CAT &middot; Otwa Events, Long Acres, Lusaka</span>
    <span class="service-bar__links">
      <a href="{MAP_URL}" target="_blank" rel="noopener">Get directions</a>
      <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
    </span>
  </div>
</div>
"""


FOOTER_STRIP = [
    ("photos/thumb-worship.webp", "Worship at RPAI"),
    ("photos/thumb-word.webp", "The Word at RPAI"),
    ("photos/thumb-family.webp", "The RPAI family"),
    ("photos/thumb-prayer.webp", "Prayer at RPAI"),
    ("photos/thumb-youth.webp", "NextGen youth at RPAI"),
    ("photos/thumb-men.webp", "Royal Men's Fellowship"),
    ("photos/thumb-women.webp", "Virtuous Women's Ministry"),
    ("photos/thumb-choir.webp", "The RPAI choir"),
    ("photos/thumb-community.webp", "Community care at RPAI"),
    ("photos/thumb-celebration.webp", "Celebration at RPAI"),
    ("photos/thumb-music.webp", "Music at RPAI"),
    ("photos/thumb-worship-leader.webp", "Worship leader"),
]


def footer(marquee: bool = True, page: str = "index") -> str:
    marquee_photos = [
        ("photos/card-worship.webp", "Worship at RPAI"),
        ("photos/card-word.webp", "The Word at RPAI"),
        ("photos/card-family.webp", "The RPAI family"),
        ("photos/card-prayer.webp", "Prayer at RPAI"),
        ("photos/card-youth.webp", "NextGen youth"),
        ("photos/card-men.webp", "Royal Men's Fellowship"),
        ("photos/card-women.webp", "Virtuous Women's Ministry"),
        ("photos/card-choir.webp", "The choir"),
        ("photos/card-community.webp", "Community care"),
        ("photos/card-celebration.webp", "Celebration"),
        ("photos/card-preach.webp", "The Word"),
        ("photos/card-fellowship.webp", "Fellowship"),
    ]
    # Each page gets a different slice of the strip so no photo leads twice.
    try:
        offset = [k for k, _, _ in ALL_NAV].index(page) * 2
    except ValueError:
        offset = 0
    strip = FOOTER_STRIP[offset:] + FOOTER_STRIP[:offset]
    marquee_photos = strip
    group = "\n".join(
        f'<img src="{src}" alt="{alt}" width="160" height="105" loading="lazy" decoding="async" '
        f'srcset="{src} 640w" sizes="160px">'
        for src, alt in marquee_photos
    )
    explore = "\n".join(f'<a href="{href}">{label}</a>' for href, label, _ in NAV[:5])
    take_part = "\n".join(f'<a href="{href}">{label}</a>' for href, label, _ in MORE[:6])
    if marquee:
        marquee_html = '<div class="footer-marquee" aria-hidden="true"><div class="marquee"><div class="marquee__group">' + group + '</div><div class="marquee__group">' + group + '</div></div></div>'
    else:
        marquee_html = ""
    return f"""
<footer class="site-footer">
  {marquee_html}

  <div class="footer-main">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a class="brand" href="index.html" aria-label="{CHURCH} home">
            <span class="brand__mark"><img src="logo-rpai.png" alt="" width="42" height="42"></span>
            <span class="brand__text">
              <span class="brand__name">Royal Priesthood</span>
              <span class="brand__sub">Assemblies International</span>
            </span>
          </a>
          <p class="footer-tagline">{TAGLINE}</p>
          <p class="footer-about">A church family in Lusaka, Zambia, gathered around the Word, prayer and one another. Come as you are; there is room for you here.</p>
          <div class="footer-contact">
            <a href="{MAP_URL}" target="_blank" rel="noopener">{ADDRESS}</a>
            <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
            <a href="mailto:{EMAIL}">{EMAIL}</a>
            <span>Sunday Divine Service · 09:00 AM CAT</span>
          </div>
          <div class="footer-social">
            <a href="{WHATSAPP}" target="_blank" rel="noopener" aria-label="WhatsApp"><img src="https://cdn.simpleicons.org/whatsapp/ffffff" alt="" width="18" height="18"></a>
            <a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook"><img src="https://cdn.simpleicons.org/facebook/ffffff" alt="" width="18" height="18"></a>
            <a href="{YOUTUBE}" target="_blank" rel="noopener" aria-label="YouTube"><img src="https://cdn.simpleicons.org/youtube/ffffff" alt="" width="18" height="18"></a>
          </div>
        </div>

        <div class="footer-col">
          <h2>Explore</h2>
          <div class="footer-links">
            {explore}
            <a href="gallery.html">Media Gallery</a>
          </div>
        </div>

        <div class="footer-col">
          <h2>Take part</h2>
          <div class="footer-links">
            {take_part}
          </div>
        </div>

        <div class="footer-col">
          <h2>Gather with us</h2>
          <div class="footer-links">
            <a href="branches-transport.html">Plan your visit</a>
            <a href="branches-transport.html#transport">Ask about transport</a>
            <a href="contact.html#prayer">Send a prayer request</a>
            <a href="attend.html">Make an attending card</a>
            <a href="give.html">Give online</a>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="container">
    <div class="footer-bottom">
      <span>© <span data-year data-rpai-year>{YEAR}</span> {CHURCH}. All rights reserved.</span>
      <div class="footer-bottom__links">
        <a href="privacy.html">Privacy</a>
        <a href="terms.html">Terms</a>
        <a href="announcements.html">Announcements</a>
        <a href="contact.html">Contact</a>
      </div>
    </div>
  </div>
</footer>
"""


BASE = """<!doctype html>
<html lang="en" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{title}}</title>
  <meta name="description" content="{{description}}">
  <link rel="canonical" href="{{canonical}}">
  <meta name="theme-color" content="#0b2240">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{{church}}">
  <meta property="og:title" content="{{title}}">
  <meta property="og:description" content="{{description}}">
  <meta property="og:url" content="{{canonical}}">
  <meta property="og:image" content="{{site}}/og-rpai.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@royalpriesthood">
  <meta name="theme-color" content="#0b2240">
  <meta name="twitter:title" content="{{title}}">
  <meta name="twitter:description" content="{{description}}">
  <meta name="twitter:image" content="{{site}}/og-rpai.jpg">
  <link rel="icon" type="image/png" href="logo-rpai.png">
  <link rel="apple-touch-icon" sizes="180x180" href="logo-rpai.png">
  <link rel="manifest" href="site.webmanifest">
  <link rel="preload" href="photos/{{hero_file}}-960.webp" as="image" type="image/webp" fetchpriority="high">
  <link rel="stylesheet" href="css__fonts.css">
  <link rel="stylesheet" href="css__rpa30.css?v=2">
  <script>document.documentElement.classList.remove('no-js');document.documentElement.classList.add('js');</script>
  {{head_extra}}
</head>
<body data-page="{{page}}" {{body_attrs}}>
  <a class="skip-link" href="#main">Skip to main content</a>
  {{servicebar}}
  {{header}}
  <main id="main">
    {{body}}
  </main>
  {{footer}}
  <script src="js__rpa30.js?v=2" defer></script>
  <script src="js__rpai.js?v=64" defer></script>
  {{scripts_extra}}
</body>
</html>
"""


def hero(eyebrow, title, lead, actions="", image="photos/hero-about.webp", home=False):
    klass = "hero hero--home" if home else "page-hero"
    base = image.rsplit("/", 1)[-1].replace(".webp", "")
    srcset = f"photos/{base}-960.webp 960w, {image} 1280w"
    sizes = "(max-width: 640px) 100vw, 1280px"
    return f"""
<section class="{klass}">
  <img class="{'hero__bg' if home else 'page-hero__bg'}" src="photos/{base}-960.webp" srcset="{srcset}" sizes="{sizes}" alt="" aria-hidden="true" width="1280" height="720" fetchpriority="high" decoding="async">
  <span class="{'hero__ticks' if home else 'page-hero__ticks'}" aria-hidden="true"></span>
  <div class="container">
    <div class="{'hero__inner' if home else 'page-hero__inner'} reveal">
      <p class="{'hero__date' if home else 'page-hero__eyebrow'}">{eyebrow}</p>
      <h1 class="h1">{title}</h1>
      <p class="{'hero__lead' if home else 'page-hero__lead'}">{lead}</p>
      {actions}
    </div>
  </div>
</section>
"""


def section_head(eyebrow, title, lead="", center=False, extra=""):
    klass = "section-head section-head--center" if center else "section-head"
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    return f"""
<div class="{klass} reveal">
  <p class="eyebrow">{eyebrow}</p>
  <h2 class="h2">{title}</h2>
  {lead_html}
  {extra}
</div>
"""


def button(label, href, kind="btn-primary", extra=""):
    external = href.startswith("http") or href.startswith("mailto:") or href.startswith("tel:")
    target = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
    return f'<a class="btn {kind}" href="{href}"{target}{extra}>{label}</a>'


def share_row():
    return f"""
<div class="share-row">
  <span class="share-row__label">Share</span>
  <button class="share-btn" type="button" data-share="whatsapp" aria-label="Share on WhatsApp">{ICONS['whatsapp']}</button>
  <button class="share-btn" type="button" data-share="facebook" aria-label="Share on Facebook">{ICONS['facebook']}</button>
  <button class="share-btn" type="button" data-share="x" aria-label="Share on X">{ICONS['x']}</button>
  <button class="share-btn" type="button" data-share="email" aria-label="Share by email">{ICONS['mail']}</button>
  <button class="share-btn" type="button" data-share="copy" aria-label="Copy link">{ICONS['copy']}</button>
  <span class="share-status" data-share-status role="status"></span>
</div>
"""


def faq(items):
    rows = "\n".join(
        f"<details><summary>{question}</summary><p>{answer}</p></details>"
        for question, answer in items
    )
    return f'<div class="faq reveal">{rows}</div>'


PAGE_FILES = {
    "index": "index.html",
    "about": "about.html",
    "pastor": "senior-pastor.html",
    "testimonies": "testimonies.html",
    "ministries": "ministry.html",
    "gallery": "gallery.html",
    "impact": "impact.html",
    "visit": "branches-transport.html",
    "give": "give.html",
    "devotional": "daily-devotional.html",
    "announcements": "announcements.html",
    "contact": "contact.html",
    "attend": "attend.html",
    "privacy": "privacy.html",
    "terms": "terms.html",
}


def write_page(key, body, head_extra="", scripts_extra="", body_attrs="", marquee=True):
    title, description, og_image = PAGE_META[key]
    filename = PAGE_FILES[key]
    hero_file = PAGE_HERO[key].rsplit("/", 1)[-1].replace(".webp", "")
    canonical = f"{SITE}/" if key == "index" else f"{SITE}/{filename}"
    html = (
        BASE.replace("{{title}}", title)
        .replace("{{description}}", description)
        .replace("{{canonical}}", canonical)
        .replace("{{church}}", CHURCH)
        .replace("{{site}}", SITE)
        .replace("{{og_image}}", og_image)
        .replace("{{hero_file}}", hero_file)
        .replace("{{page}}", key)
        .replace("{{body_attrs}}", body_attrs)
        .replace("{{head_extra}}", head_extra)
        .replace("{{servicebar}}", service_bar())
        .replace("{{header}}", site_header(key))
        .replace("{{body}}", body)
        .replace("{{footer}}", footer(marquee=marquee, page=key))
        .replace("{{scripts_extra}}", scripts_extra)
    )
    (ROOT / filename).write_text(html, encoding="utf-8")
    print(f"wrote {filename}")


# ============================================================================
# PAGE CONTENT
# ============================================================================

ABOUT_BODY = f"""
{hero(
    "Our story",
    "A story of love, faith and family.",
    "Royal Priesthood Assemblies International began with a call to gather God’s people in Lusaka — to teach His Word, make room for His presence, and love one another well.",
    f'<div class="page-hero__actions">{button("Meet our shepherd", "senior-pastor.html")}{button("Our ministries", "ministry.html", "btn-outline")}</div>',
    image="photos/hero-story.webp",
)}

<section class="section">
  <div class="container">
    <div class="split split--wide">
      <div class="split__body reveal">
        <p class="eyebrow">The beginning</p>
        <h2 class="h2">It started with one instruction.</h2>
        <p class="lead">Gather my people. Teach them my Word. Make room for my presence.</p>
        <p>That conviction became a church family. What began quietly — in prayer, conversation and a handful of believing hearts — grew into a house where children, youth, parents and grandparents could worship together.</p>
        <p>We did not begin with a building. We began with a people. And that is still who we are: a family learning to love God and one another in everyday life.</p>
        <div class="stat-grid mt-2">
          <div class="stat"><div class="stat__value">1</div><div class="stat__label">church family</div><div class="stat__note">Many stories, one table</div></div>
          <div class="stat"><div class="stat__value">4</div><div class="stat__label">ministry communities</div><div class="stat__note">A place for every season</div></div>
        </div>
      </div>
      <div class="split__media reveal" data-delay="1">
        <div class="media-stack">
          <figure>
            <img src="photos/about-worship.webp" alt="Worship at Royal Priesthood Assemblies International" width="700" height="875" loading="lazy" decoding="async">
            <figcaption><span>Worship</span>Honouring God together</figcaption>
          </figure>
          <figure>
            <img src="photos/about-word.webp" alt="The Word at RPAI" width="560" height="747" loading="lazy" decoding="async">
            <figcaption><span>The Word</span>Rooted in Scripture</figcaption>
          </figure>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="container">
    <div class="year-card year-card--quote reveal" style="position:relative;top:auto">
      <span class="year-card__era">Our confession</span>
      <p class="scripture">“But you are a chosen generation, a royal priesthood, a holy nation, His own special people, that you may proclaim the praises of Him who called you out of darkness into His marvelous light.”</p>
      <p class="scripture"><cite>1 Peter 2:9</cite></p>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="split split--wide">
      <div class="split__media reveal">
        <div class="profile" style="border-radius:var(--radius-lg)">
          <figure class="profile__media" style="grid-column:1/-1;min-height:420px">
            <img src="photos/thumb-family.webp" srcset="photos/quick-family.webp 420w, photos/thumb-family.webp 640w, photos/card-family.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="A family at RPAI" width="800" height="900" loading="lazy" decoding="async">
            <figcaption><strong>Apostle Dr. Mighty Zunga</strong><span>Founder &amp; General Overseer</span></figcaption>
          </figure>
        </div>
      </div>
      <div class="split__body reveal" data-delay="1">
        <p class="eyebrow">Our founder</p>
        <h2 class="h2">A life given to the Word and to people.</h2>
        <p>Apostle Dr. Mighty Zunga is the Founder and General Overseer of Royal Priesthood Assemblies International in Lusaka, Zambia.</p>
        <p>His ministry is expressed through preaching, prayer, discipleship and the leadership of the church community. He encourages believers to grow in their understanding of Scripture and to put their faith into practice through service.</p>
        <p>Under his leadership, the church has become a family where the Word is taught with clarity, prayer is given room, and every person is encouraged to take their place.</p>
        <div class="row mt-2">
          {button("Meet our senior pastor", "senior-pastor.html")}
          {button("Listen to messages", YOUTUBE, "btn-ghost")}
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_head("What we are building", "Rooted in faith. United in fellowship.", "Our mission, vision and values are simple enough to remember and strong enough to build a life on.")}
    <div class="grid grid-3">
      <article class="reveal">
        <span class="card__label">Our mission</span>
        <h3 class="h3 mt-2">Faith in word and action.</h3>
        <p class="card__text">To proclaim the Gospel, encourage spiritual growth through Scripture and prayer, and serve our neighbours with compassion.</p>
      </article>
      <article class="reveal" data-delay="1">
        <span class="card__label">Our vision</span>
        <h3 class="h3 mt-2">A community strengthened by hope.</h3>
        <p class="card__text">To see people and communities strengthened by the hope of Christ and equipped to live out their faith in everyday life.</p>
      </article>
      <article class="reveal" data-delay="2">
        <span class="card__label">Our goal</span>
        <h3 class="h3 mt-2">Connecting people with God and one another.</h3>
        <p class="card__text">To make room for worship, belonging and service — so that no one has to walk through life alone.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    {section_head("What matters to us", "Faith lived together.", "Four commitments shape the rhythm of our life as a church.")}
    <div class="grid grid-4">
      <article class="reveal"><span class="story-card__num">01</span><h3 class="h3 mt-2">Worship</h3><p class="card__text">We gather to honour God and make room for prayer, praise and gratitude.</p></article>
      <article class="reveal" data-delay="1"><span class="story-card__num">02</span><h3 class="h3 mt-2">Growing in faith</h3><p class="card__text">We build a life of faith through Scripture, prayer and encouragement.</p></article>
      <article class="reveal" data-delay="2"><span class="story-card__num">03</span><h3 class="h3 mt-2">Fellowship</h3><p class="card__text">We welcome one another, share life and serve our community with care.</p></article>
      <article class="reveal" data-delay="3"><span class="story-card__num">04</span><h3 class="h3 mt-2">Service</h3><p class="card__text">We put love into action, especially where there is practical need.</p></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split split--wide">
      <div class="split__body reveal">
        <p class="eyebrow">The journey so far</p>
        <h2 class="h2">Every chapter has been grace.</h2>
        <p class="lead">We do not have a straight line to show you. We have a faithful God and a family that keeps saying yes.</p>
        <div class="timeline mt-2">
          <div class="timeline__item"><span class="timeline__dot" aria-hidden="true"></span><div class="timeline__body"><span>The call</span><h3>A conviction to gather</h3><p>A call to teach the Word, pray and welcome people into a family.</p></div></div>
          <div class="timeline__item"><span class="timeline__dot" aria-hidden="true"></span><div class="timeline__body"><span>The first gatherings</span><h3>A handful of believers</h3><p>Small beginnings, honest prayer and a growing hunger for God.</p></div></div>
          <div class="timeline__item"><span class="timeline__dot" aria-hidden="true"></span><div class="timeline__body"><span>Growing roots</span><h3>A church for every generation</h3><p>Children, youth, women, men and families finding a place to belong.</p></div></div>
          <div class="timeline__item"><span class="timeline__dot" aria-hidden="true"></span><div class="timeline__body"><span>Beyond Sunday</span><h3>Home cells and care</h3><p>Fellowship and practical love carried into homes and neighbourhoods.</p></div></div>
          <div class="timeline__item"><span class="timeline__dot" aria-hidden="true"></span><div class="timeline__body"><span>Today</span><h3>A people still being formed</h3><p>Still learning, still growing, still making room for one another.</p></div></div>
        </div>
      </div>
      <div class="split__media reveal" data-delay="1">
        <img src="photos/about-graduation.webp" alt="The RPAI family celebrating together" width="900" height="1125" loading="lazy" decoding="async" style="min-height:420px">
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="container">
    <div class="cta-card reveal">
      <p class="eyebrow" style="justify-self:center">Come and see</p>
      <h2 class="h2">There is a place for you in this story.</h2>
      <p>Visit us this Sunday, or reach out and let us know how we can pray with you.</p>
      <div class="cta-card__actions">
        {button("Plan your visit", "branches-transport.html")}
        {button("Contact us", "contact.html", "btn-outline")}
      </div>
      {share_row()}
    </div>
  </div>
</section>
"""

PASTOR_BODY = f"""
{hero(
    "Our Senior Pastor",
    "A shepherd’s heart. A father’s faith.",
    "Apostle Dr. Mighty Zunga leads Royal Priesthood Assemblies International with a clear commitment to the Word, prayer and the care of people.",
    f'<div class="page-hero__actions">{button("Watch and listen", YOUTUBE)}{button("Meet the church", "about.html", "btn-outline")}</div>',
    image="photos/hero-pastor.webp",
)}

<section class="section">
  <div class="container">
    <div class="profile reveal">
      <figure class="profile__media">
        <img src="photos/thumb-pastor.webp" srcset="photos/quick-pastor.webp 420w, photos/thumb-pastor.webp 640w, photos/card-pastor.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="Apostle Dr. Mighty Zunga" width="900" height="1000" loading="lazy" decoding="async">
        <figcaption><strong>Apostle Dr. Mighty Zunga</strong><span>Founder &amp; General Overseer</span></figcaption>
      </figure>
      <div class="profile__body">
        <p class="eyebrow">Founder &amp; General Overseer</p>
        <h2 class="h2">A life given to the Word and to people.</h2>
        <p>Apostle Dr. Mighty Zunga is the Founder and General Overseer of Royal Priesthood Assemblies International in Lusaka, Zambia.</p>
        <p>His ministry is expressed through preaching, prayer, discipleship and the leadership of the church community. He encourages believers to grow in their understanding of Scripture and to put their faith into practice through service.</p>
        <p>Those who sit under his teaching describe a pastor who loves the Word, values prayer and believes that every person matters. His burden is to see a church family that is strong in faith, warm in fellowship and generous in love.</p>
        <div class="profile__tags">
          <span>Teaching</span><span>Prayer</span><span>Discipleship</span><span>Leadership</span>
        </div>
        <div class="row mt-2">
          {button("Watch messages", YOUTUBE)}
          {button("Plan your visit", "branches-transport.html", "btn-ghost")}
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="split split--wide">
      <div class="split__body reveal">
        <p class="eyebrow">The call</p>
        <h2 class="h2">A ministry shaped by prayer.</h2>
        <p class="lead">Before it was a public ministry, it was a private yes.</p>
        <p>His ministry is expressed through preaching, prayer, discipleship, and the leadership of the church community. He encourages believers to grow in their understanding of Scripture and to put their faith into practice through service.</p>
        <p>At the heart of his leadership is a simple conviction: the Word of God is enough to change a life, and prayer is the atmosphere in which that change takes root.</p>
        <blockquote class="year-card year-card--quote" style="position:relative;top:auto;padding:20px">
          <p class="scripture" style="font-size:1.1rem">“Let your light so shine before men, that they may see your good works and glorify your Father in heaven.”</p>
          <p class="scripture" style="font-size:.8rem"><cite>Matthew 5:16</cite></p>
        </blockquote>
      </div>
      <div class="split__media reveal" data-delay="1">
        <img src="photos/thumb-preaching.webp" srcset="photos/quick-preaching.webp 420w, photos/thumb-preaching.webp 640w, photos/card-preaching.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="Apostle Dr. Mighty Zunga teaching the Word" width="900" height="1000" loading="lazy" decoding="async" style="min-height:430px">
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_head("What he has given his life to", "Four things that never move.", "The priorities that shape his leadership and our life together.")}
    <div class="grid grid-4">
      <article class="reveal"><span class="story-card__num">01</span><h3 class="h3 mt-2">The Word</h3><p class="card__text">Clear, faithful teaching that helps people know Jesus and live what they believe.</p></article>
      <article class="reveal" data-delay="1"><span class="story-card__num">02</span><h3 class="h3 mt-2">Prayer</h3><p class="card__text">Making room for God to speak, heal and guide — personally and as a church.</p></article>
      <article class="reveal" data-delay="2"><span class="story-card__num">03</span><h3 class="h3 mt-2">People</h3><p class="card__text">Pastoring the family, celebrating milestones and standing with people in hard seasons.</p></article>
      <article class="reveal" data-delay="3"><span class="story-card__num">04</span><h3 class="h3 mt-2">Raising leaders</h3><p class="card__text">Helping sons and daughters grow into their calling and take their place in the house.</p></article>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="split split--wide">
      <div class="split__media reveal">
        <img src="photos/thumb-leadership.webp" srcset="photos/quick-leadership.webp 420w, photos/thumb-leadership.webp 640w, photos/card-leadership.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="The RPAI leadership family" width="900" height="650" loading="lazy" decoding="async">
      </div>
      <div class="split__body reveal" data-delay="1">
        <p class="eyebrow">He and the church</p>
        <h2 class="h2">Leading a family, not just a service.</h2>
        <p>Apostle Zunga leads alongside the RPAI leadership team and the wider church family. Together they carry the work of the ministry — teaching, prayer, home cells, youth, women, men and practical care.</p>
        <p>His heart is for a church where the next generation is not an afterthought, where the elderly are honoured, and where every person is seen and known.</p>
        <div class="row mt-2">
          {button("Our story", "about.html")}
          {button("Our ministries", "ministry.html", "btn-ghost")}
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_head("Watch and listen", "Stay connected to the ministry.", "Follow the church’s official channels for live services, messages, worship and announcements.")}
    <div class="media-links reveal">
      <a class="media-link" href="{YOUTUBE}" target="_blank" rel="noopener"><span class="media-link__icon">{ICONS['youtube']}</span><span class="media-link__text"><strong>YouTube</strong><span>Messages, worship and church highlights</span></span></a>
      <a class="media-link" href="{FACEBOOK}" target="_blank" rel="noopener"><span class="media-link__icon">{ICONS['facebook']}</span><span class="media-link__text"><strong>Facebook</strong><span>Live services and church updates</span></span></a>
      <a class="media-link" href="announcements.html"><span class="media-link__icon">{ICONS['bell']}</span><span class="media-link__text"><strong>Announcements</strong><span>The latest news from the family</span></span></a>
      <a class="media-link" href="contact.html#prayer"><span class="media-link__icon">{ICONS['heart']}</span><span class="media-link__text"><strong>Prayer request</strong><span>Let us stand with you in prayer</span></span></a>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="cta-card reveal">
      <p class="eyebrow" style="justify-self:center">Come and meet us</p>
      <h2 class="h2">There is a seat for you this Sunday.</h2>
      <p>Join the family at 09:00 AM, or send a prayer request and let us stand with you.</p>
      <div class="cta-card__actions">
        {button("Plan your visit", "branches-transport.html")}
        {button("Send a prayer request", "contact.html#prayer", "btn-outline")}
      </div>
      {share_row()}
    </div>
  </div>
</section>
"""

TESTIMONY_ITEMS = [
    ("Healing", "A new beginning", "I came in broken and carrying questions. I found a family that prayed with me, taught me the Word and walked with me until I could stand again.", "Brian M.", "Church family"),
    ("Family", "A home restored", "Our home was tired and divided. Through prayer, counselling and the love of this family, we learned to talk again and to forgive. God is still working, but He has done what we could not do.", "Grace C.", "Church family"),
    ("Provision", "A door opened", "I waited a long time without work. The church kept praying with me and reminding me that God had not forgotten me. When the job came, we thanked God together.", "Joseph K.", "Church family"),
    ("Peace", "Peace in the storm", "The diagnosis frightened us. The prayers of the church carried us through treatment and uncertainty. I do not know how we would have walked that road alone.", "Martha P.", "Church family"),
    ("Family", "A child after waiting", "After years of waiting, God gave us our daughter. We dedicate her to Him and remain grateful for every prayer that held us up.", "The Banda family", "Church family"),
    ("Salvation", "A place to belong", "I came to church because a friend invited me. I stayed because I met Jesus here. My life has a new direction and a new family.", "Chanda T.", "Church family"),
    ("Academic", "Strength for the journey", "I nearly gave up on my studies. The youth ministry encouraged me, prayed with me and kept me accountable. Today I can see God’s hand in it all.", "Natasha M.", "NextGen"),
    ("Freedom", "Free from fear", "Fear followed me for years. Through prayer and the Word, I have learned to trust God with tomorrow. I am not the same person.", "Daniel S.", "Church family"),
    ("Family", "A marriage restored", "We were close to giving up. The church did not take sides; it helped us pray, listen and begin again. We are grateful for grace.", "Mr &amp; Mrs Phiri", "Church family"),
]

T_ITEMS_HTML = "\n".join(
    f"""
      <article class="quote-card reveal" data-testimony data-category="{category.lower()}">
        <span class="quote-card__mark">“</span>
        <div class="row"><span class="card__label">{category}</span></div>
        <h3 class="h4">{title}</h3>
        <blockquote>{story}</blockquote>
        <div class="quote-card__person"><span class="quote-card__avatar">{''.join(part[0] for part in name.replace('&amp;', '').split()[:2])}</span><div><p class="quote-card__name">{name}</p><p class="quote-card__meta">{meta} · Shared with permission</p></div></div>
      </article>
    """
    for category, title, story, name, meta in TESTIMONY_ITEMS
)

TESTIMONIES_BODY = f"""
{hero(
    "Testimonies",
    "Stories of His faithfulness.",
    "God is still at work in ordinary lives. These are a few words from the Royal Priesthood family — and an invitation to share your own.",
    f'<div class="page-hero__actions">{button("Share your testimony", "#share")}{button("Plan a visit", "branches-transport.html", "btn-outline")}</div>',
    image="photos/hero-testimonies.webp",
)}

<section class="section">
  <div class="container">
    <div class="between">
      {section_head("The testimony wall", "Every story matters.", "Search by what God has done, or read a little of what life in this family looks like.")}
      <p class="gallery-count" data-testimony-count aria-live="polite"></p>
    </div>
    <div data-testimonies>
      <div class="filter-bar reveal">
        <div class="search-box">
          {ICONS['search']}
          <label class="sr-only" for="testimony-search">Search testimonies</label>
          <input id="testimony-search" type="search" placeholder="Search testimonies…" data-testimony-search autocomplete="off">
        </div>
        <div class="chip-row" role="group" aria-label="Filter testimonies">
          <button class="chip" type="button" data-testimony-filter="all" aria-pressed="true">All</button>
          <button class="chip" type="button" data-testimony-filter="salvation" aria-pressed="false">Salvation</button>
          <button class="chip" type="button" data-testimony-filter="healing" aria-pressed="false">Healing</button>
          <button class="chip" type="button" data-testimony-filter="family" aria-pressed="false">Family</button>
          <button class="chip" type="button" data-testimony-filter="provision" aria-pressed="false">Provision</button>
          <button class="chip" type="button" data-testimony-filter="peace" aria-pressed="false">Peace</button>
          <button class="chip" type="button" data-testimony-filter="academic" aria-pressed="false">Academic</button>
          <button class="chip" type="button" data-testimony-filter="freedom" aria-pressed="false">Freedom</button>
        </div>
      </div>
      <div class="grid grid-3 mt-3">
        {T_ITEMS_HTML}
      </div>
      <p class="form-note mt-3">Names are shortened for privacy. Testimonies are shared with permission and lightly edited for length and clarity.</p>
    </div>
  </div>
</section>

<section class="section section--flush-top" id="share">
  <div class="container">
    <div class="split split--wide">
      <div class="split__body reveal">
        <p class="eyebrow">Share your story</p>
        <h2 class="h2">What has God done for you?</h2>
        <p class="lead">Your testimony could be the encouragement someone needs today. Tell us what happened, and our team will follow up before anything is published.</p>
        <ul class="check-list">
          <li>Share as much or as little as you are comfortable with.</li>
          <li>We will not publish your story without your permission.</li>
          <li>If you need prayer, you can also send a prayer request.</li>
        </ul>
        <p class="small">Prefer to talk? Call or WhatsApp <a class="gold" href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.</p>
      </div>
      <form class="form-card reveal" data-delay="1" data-rpai-mail-form data-subject="Testimony submission — RPAI website">
        <div class="form-grid">
          <div class="form-field"><label for="testimony-name">Your name</label><input id="testimony-name" name="name" type="text" autocomplete="name" required></div>
          <div class="form-field"><label for="testimony-email">Email <span>optional</span></label><input id="testimony-email" name="email" type="email" autocomplete="email"></div>
          <div class="form-field"><label for="testimony-phone">Phone / WhatsApp <span>optional</span></label><input id="testimony-phone" name="phone" type="tel" autocomplete="tel"></div>
          <div class="form-field"><label for="testimony-category">What is this about?</label><select id="testimony-category" name="category"><option>Salvation</option><option>Healing</option><option>Family</option><option>Provision</option><option>Peace</option><option>Academic</option><option>Freedom</option><option>Other</option></select></div>
          <div class="form-field form-field--full"><label for="testimony-title">A short title</label><input id="testimony-title" name="title" type="text" placeholder="e.g. A door opened" required></div>
          <div class="form-field form-field--full"><label for="testimony-story">Your testimony</label><textarea id="testimony-story" name="story" required placeholder="Tell us what God has done…"></textarea></div>
          <label class="form-check form-field--full"><input type="checkbox" name="consent" value="yes" required> I am happy for the church to contact me about this testimony. I understand it will not be published without my permission.</label>
        </div>
        <div class="row mt-3"><button class="btn btn-primary" type="submit">Send your testimony</button><span class="form-status" data-form-status role="status"></span></div>
        <p class="form-note mt-2">This form opens your email app. You can also email <a class="gold" href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      </form>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="cta-card reveal">
      <p class="eyebrow" style="justify-self:center">A living story</p>
      <h2 class="h2">Come and write the next chapter with us.</h2>
      <p>Join us this Sunday at 09:00 AM, or share this page with someone who needs hope.</p>
      <div class="cta-card__actions">
        {button("Plan your visit", "branches-transport.html")}
        {button("Send a prayer request", "contact.html#prayer", "btn-outline")}
      </div>
      {share_row()}
    </div>
  </div>
</section>
"""


HOME_BODY = f"""
{hero(
    "Sunday Divine Service · 09:00 AM · Lusaka, Zambia",
    "A place of love where everyone counts.",
    "Royal Priesthood Assemblies International is a church family in Lusaka, gathered around the Word, prayer and one another. Come as you are — there is room for you here.",
    f'<div class="hero__actions">{button("Plan your visit", "branches-transport.html")}{button("Our story", "about.html", "btn-outline")}</div><span class="hero__note">Otwa Events · Long Acres · Ndeke Road</span>',
    home=True,
)}

<section class="section section--tight">
  <div class="container">
    <div class="expect-card reveal">
      <div class="expect-card__head">
        <p class="eyebrow">First time?</p>
        <h2 class="h2">What to expect on your first Sunday.</h2>
        <p class="lead">You are welcome the moment you walk in. Here is the whole Sunday in four simple steps.</p>
      </div>
      <ol class="expect-steps">
        <li><span>01</span><div><strong>Arrive</strong><p>Come a few minutes early. Our welcome team will greet you and show you where to sit.</p></div></li>
        <li><span>02</span><div><strong>Worship</strong><p>Songs, prayer and a time to honour God, together with the whole family.</p></div></li>
        <li><span>03</span><div><strong>The Word</strong><p>A practical message from Scripture that speaks to everyday life.</p></div></li>
        <li><span>04</span><div><strong>Family</strong><p>Stay for a word with someone. Ask about a home cell and how to get involved.</p></div></li>
      </ol>
      <div class="row mt-3">
        {button("Plan your visit", "branches-transport.html")}
        {button("See service times", "announcements.html", "btn-outline")}
      </div>
    </div>
  </div>
</section>

<section class="card-run" aria-label="Life at Royal Priesthood Assemblies International">
  <div class="container">
    <div class="card-run__stage">
      <figure class="run-card run-card--1">
        <img src="photos/thumb-worship.webp" srcset="photos/quick-worship.webp 420w, photos/thumb-worship.webp 640w, photos/card-worship.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="Worship at Royal Priesthood Assemblies International" width="440" height="550" loading="lazy" decoding="async">
        <figcaption><span>Sunday</span>Worship together</figcaption>
      </figure>
      <figure class="run-card run-card--2">
        <img src="photos/thumb-word.webp" srcset="photos/quick-word.webp 420w, photos/thumb-word.webp 640w, photos/card-word.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="The Word being taught at RPAI" width="440" height="550" loading="lazy" decoding="async">
        <figcaption><span>The Word</span>Truth for every season</figcaption>
      </figure>
      <figure class="run-card run-card--3">
<img src="photos/thumb-prayer.webp" srcset="photos/quick-prayer.webp 420w, photos/thumb-prayer.webp 640w, photos/card-prayer.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="Prayer at RPAI" width="440" height="550" loading="lazy" decoding="async">
        <figcaption><span>Prayer</span>Seeking Him together</figcaption>
      </figure>
      <figure class="run-card run-card--4">
        <img src="photos/thumb-family.webp" srcset="photos/quick-family.webp 420w, photos/thumb-family.webp 640w, photos/card-family.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="The church family at RPAI" width="440" height="550" loading="lazy" decoding="async">
        <figcaption><span>Family</span>Everyone counts</figcaption>
      </figure>

        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="container">
    <div class="split split--wide">
      <div class="split__body reveal">
        <p class="eyebrow">Welcome home</p>
        <h2 class="h2">A family, not an audience.</h2>
        <p class="lead">We gather to worship God, grow in His Word, and carry one another's burdens. Whether you have walked with Jesus for years or you are just curious, you are welcome here.</p>
        <p>Royal Priesthood is a people before it is a place. We believe love is more than a kind word — it is the life of Christ made visible in the way we welcome, forgive, serve, and stand beside one another.</p>
        <ul class="check-list">
          <li>A warm welcome and a seat saved for you</li>
          <li>Word, worship and prayer that meet you where you are</li>
          <li>A church family for every generation</li>
        </ul>
        <div class="row mt-2">
          {button("Know more about us", "about.html", "btn-outline")}
          <a class="link-arrow" href="ministry.html">Find your place</a>
        </div>
      </div>
      <div class="split__media reveal" data-delay="1">
        <figure class="media-single">
          <img src="photos/thumb-congregation.webp" srcset="photos/quick-congregation.webp 420w, photos/thumb-congregation.webp 640w, photos/card-congregation.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="The RPAI church family gathered together" width="900" height="600" loading="lazy" decoding="async">
          <figcaption><span>Our family</span>Everyone counts</figcaption>
        </figure>
      </div>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="feature reveal">
      <div class="feature__body">
        <span class="feature__badge">{ICONS['clock']} Every Sunday</span>
        <div>
          <p class="eyebrow">Join us in person</p>
          <h2 class="h2">Sunday Divine Service</h2>
        </div>
        <p class="lead">Come and worship with us at 09:00 AM. Expect the Word, prayer, worship and a family glad to meet you.</p>
        <ul class="feature__list">
          <li><span class="feature__icon">{ICONS['pin']}</span><span><strong>Otwa Events, Long Acres</strong><span>Ndeke Road, Lusaka, Zambia</span></span></li>
          <li><span class="feature__icon">{ICONS['clock']}</span><span><strong>Sunday · 09:00 AM CAT</strong><span>Midweek fellowship · Wednesday · 05:30 PM</span></span></li>
          <li><span class="feature__icon">{ICONS['heart']}</span><span><strong>Come as you are</strong><span>No special dress, no special language — just come.</span></span></li>
        </ul>
        <div class="row">
          {button("Plan your visit", "branches-transport.html")}
          {button("Get directions", MAP_URL, "btn-ghost")}
        </div>
      </div>
      <div class="feature__media">
        <img src="photos/thumb-praise.webp" srcset="photos/quick-praise.webp 420w, photos/thumb-praise.webp 640w, photos/card-praise.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="The congregation at Royal Priesthood Assemblies International" width="900" height="700" loading="lazy" decoding="async">
      </div>
    </div>
  </div>
</section>
        <div>
          <h3 class="h3">Coming from outside Lusaka?</h3>
          <p class="small mt-1">Let us know you are coming and we will help with transport, directions and a warm welcome.</p>
        </div>
        <a class="link-arrow" href="branches-transport.html#transport">Ask about a visit</a>
      </article>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_head("Our story", "Four movements of grace.", "What God began in a handful of hearts, He is still building today.")}
    <div class="story-grid">
      <article class="story-card reveal">
        <div><span class="story-card__num">01</span><h3 class="h3">A vision of love</h3><p>A call to gather God’s people, teach His Word and make room for His presence in Lusaka.</p></div>
        <a class="link-arrow story-card__link" href="about.html">Read our story</a>
      </article>
      <article class="story-card reveal" data-delay="1">
        <div><span class="story-card__num">02</span><h3 class="h3">A family gathered</h3><p>One table, many stories. Royal Priesthood became a home for every generation and every background.</p></div>
        <a class="link-arrow story-card__link" href="ministry.html">Meet the family</a>
      </article>
      <article class="story-card reveal" data-delay="2">
        <div><span class="story-card__num">03</span><h3 class="h3">A house of prayer</h3><p>We are learning to pray together, to wait on God and to carry one another before Him.</p></div>
        <a class="link-arrow story-card__link" href="contact.html#prayer">Send a prayer request</a>
      </article>
      <article class="story-card reveal" data-delay="3">
        <div><span class="story-card__num">04</span><h3 class="h3">A people sent</h3><p>Love that stays in the building is not yet love. We carry the gospel into homes, streets and workplaces.</p></div>
        <a class="link-arrow story-card__link" href="impact.html">See our impact</a>
      </article>
    </div>
  </div>
</section>

<section class="year-section">
  <div class="container">
    {section_head("Every season has a testimony", "God has been faithful in every chapter.", "Scroll slowly. These are the marks of His kindness among us.")}
    <div class="year-stack">
      <article class="year-card reveal">
        <span class="year-card__era">The beginning</span>
        <h3>One instruction. One yes.</h3>
        <p>A call to gather, a handful of believers, and a conviction that God had more in store for this city. The work began quietly, rooted in prayer.</p>
      </article>
      <article class="year-card reveal">
        <span class="year-card__era">A growing family</span>
        <h3>Room for every person.</h3>
        <p>Children, youth, parents, grandparents, singles and families found a place to belong. The church grew not only in number, but in love.</p>
      </article>
      <article class="year-card reveal">
        <span class="year-card__era">Rooted in the Word</span>
        <h3>A people of the Word.</h3>
        <p>Teaching, discipleship and prayer became the rhythm of the house. We learned that transformation happens when truth is lived together.</p>
      </article>
      <article class="year-card reveal">
        <span class="year-card__era">Beyond these walls</span>
        <h3>Love that leaves the room.</h3>
        <p>Home cells, community care, transport and online gatherings carried the family beyond Sunday and into everyday life.</p>
      </article>
      <article class="year-card year-card--quote reveal">
        <span class="year-card__era">Today</span>
        <p class="scripture">“Let your light so shine before men, that they may see your good works and glorify your Father in heaven.”</p>
        <p class="scripture"><cite>Matthew 5:16</cite></p>
      </article>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="container">
    <div class="between">
      {section_head("Every year has a testimony", "Stories of His faithfulness.", "A few words from the RPAI family.")}
      <a class="link-arrow" href="testimonies.html">Read all testimonies</a>
    </div>
    <div class="grid grid-3">
      <article class="quote-card reveal">
        <span class="quote-card__mark">“</span>
        <blockquote>I came in carrying questions and left with a family. The Word here met me exactly where I was.</blockquote>
        <div class="quote-card__person"><span class="quote-card__avatar">GM</span><div><p class="quote-card__name">Grace M.</p><p class="quote-card__meta">Church family</p></div></div>
      </article>
      <article class="quote-card reveal" data-delay="1">
        <span class="quote-card__mark">“</span>
        <blockquote>Prayer is not a programme here; it is the air we breathe. I have learned to bring everything to God.</blockquote>
        <div class="quote-card__person"><span class="quote-card__avatar">JK</span><div><p class="quote-card__name">Joseph K.</p><p class="quote-card__meta">Church family</p></div></div>
      </article>
      <article class="quote-card reveal" data-delay="2">
        <span class="quote-card__mark">“</span>
        <blockquote>Our children have a place to grow, ask questions and belong. That is a gift we do not take for granted.</blockquote>
        <div class="quote-card__person"><span class="quote-card__avatar">TB</span><div><p class="quote-card__name">The Banda family</p><p class="quote-card__meta">Church family</p></div></div>
      </article>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="split split--wide card card--lg" style="padding:18px">
      <div class="split__media">
<img src="photos/thumb-welcome.webp" srcset="photos/quick-welcome.webp 420w, photos/thumb-welcome.webp 640w, photos/card-welcome.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="A moment of prayer at RPAI" width="800" height="600" loading="lazy" decoding="async">
      </div>
      <div class="split__body" style="padding:14px">
        <p class="eyebrow">Your story matters</p>
        <h2 class="h2">Did you find God here?</h2>
        <p class="lead">Maybe you prayed a prayer, found healing, met a need, or simply found a home. Your testimony could strengthen someone who is still waiting.</p>
        <div class="row mt-2">
          {button("Share your testimony", "testimonies.html#share")}
          {button("Send a prayer request", "contact.html#prayer", "btn-ghost")}
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="container">
    {section_head("Some moments we love", "Grace, captured.", "A rotating glimpse of the life we share. Hover or focus to pause.", center=True)}
    <div class="ring-wrap" aria-label="A rotating gallery of church moments">
      <div class="ring">
        {''.join(f'<div class="ring__item" style="--i:{i}"><img src="photos/{name}" alt="{alt}" width="186" height="248" loading="lazy" decoding="async"></div>' for i, (name, alt) in enumerate([
            ("quick-worship.webp","Worship"),("quick-word.webp","The Word"),("quick-prayer.webp","Prayer"),("quick-family.webp","Family grace"),("quick-youth.webp","NextGen"),("quick-women.webp","Women's fellowship"),("quick-men.webp","Men's fellowship"),("quick-fellowship.webp","Home cell"),("quick-community.webp","Community"),("quick-celebration.webp","Celebration")]))}
      </div>
    </div>
    <div class="center mt-4"><a class="btn btn-outline" href="gallery.html">See the full gallery</a></div>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_head("Questions people ask", "Before you come.", "A few honest answers for first-time guests and friends.", center=True)}
    {faq([
        ("What should I expect on Sunday?", "A warm welcome, heartfelt worship, prayer and a practical message from the Word. The service usually lasts around two hours. You are free to participate as much as you are comfortable."),
        ("Where do you meet?", "We meet at Otwa Events, Long Acres, along Ndeke Road in Lusaka. Sunday Divine Service begins at 09:00 AM. Midweek fellowship is on Wednesday at 05:30 PM."),
        ("What should I wear?", "Come as you are. Some people dress up, others come in everyday clothes. What matters is that you are here."),
        ("Is there something for children and teenagers?", "Yes. Our NextGen Youth & Teen Ministry and children’s activities make room for the next generation to learn, ask questions and belong."),
        ("How do I get involved?", "Start by joining a Sunday service or a home cell. Then talk to us about the Royal Men’s Fellowship, Virtuous Women’s Ministry, NextGen or serving on a team. We will help you find your place."),
        ("Can I watch online?", "Yes. You can join our video conference from your phone, tablet or computer, or follow the ministry on Facebook and YouTube."),
    ])}
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="cta-card reveal">
      <img src="photos/thumb-graduation.webp" srcset="photos/quick-graduation.webp 420w, photos/thumb-graduation.webp 640w, photos/card-graduation.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px"" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="The RPAI family" width="900" height="500" loading="lazy" decoding="async" style="width:100%;max-height:260px;object-fit:contain;border-radius:12px;margin-bottom:18px">
      <p class="eyebrow" style="justify-self:center">You’re part of this story</p>
      <h2 class="h2">Come and see what God is doing.</h2>
      <p>Join us this Sunday at 09:00 AM — or tell someone about the place where you found love, faith and family.</p>
      <div class="cta-card__actions">
        {button("Plan your visit", "branches-transport.html")}
        {button("I am visiting church on Sunday", "attend.html", "btn-outline")}
      </div>
      {share_row()}
    </div>
  </div>
</section>
"""

HOME_HEAD = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Church",
      "@id": "https://royal-priesthood-assemblies-int-l-1.onrender.com/#church",
      "name": "Royal Priesthood Assemblies International",
      "alternateName": "RPAI",
      "slogan": "A place of love where everyone counts.",
      "url": "https://royal-priesthood-assemblies-int-l-1.onrender.com/",
      "logo": {
        "@type": "ImageObject",
        "url": "https://royal-priesthood-assemblies-int-l-1.onrender.com/logo-rpai.png"
      },
      "image": "https://royal-priesthood-assemblies-int-l-1.onrender.com/og-rpai.jpg",
      "description": "A church family in Lusaka, Zambia, gathered around the Word, prayer and one another. Sunday Divine Service at 09:00 AM.",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Otwa Events, Long Acres, Ndeke Road",
        "addressLocality": "Lusaka",
        "addressCountry": "ZM"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": -15.3875,
        "longitude": 28.3228
      },
      "telephone": "+260977490080",
      "email": "royalpriesthoodassembliesintl@gmail.com",
      "priceRange": "Free",
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": "Sunday",
          "opens": "09:00",
          "closes": "12:00"
        },
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": "Wednesday",
          "opens": "17:30",
          "closes": "20:00"
        }
      ],
      "sameAs": [
        "https://www.facebook.com/p/ROYAL-Priesthood-100064645061857/",
        "https://www.youtube.com/@royalpriesthoodassemblies"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://royal-priesthood-assemblies-int-l-1.onrender.com/#website",
      "url": "https://royal-priesthood-assemblies-int-l-1.onrender.com/",
      "name": "Royal Priesthood Assemblies International",
      "publisher": { "@id": "https://royal-priesthood-assemblies-int-l-1.onrender.com/#church" },
      "inLanguage": "en"
    },
    {
      "@type": "Event",
      "name": "Sunday Divine Service",
      "startDate": "2026-11-15T09:00:00+02:00",
      "eventStatus": "https://schema.org/EventScheduled",
      "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
      "organizer": { "@id": "https://royal-priesthood-assemblies-int-l-1.onrender.com/#church" },
      "eventSchedule": {
        "@type": "Schedule",
        "byDay": "Sunday",
        "startTime": "09:00",
        "repeatFrequency": "P1W"
      },
      "location": {
        "@type": "Place",
        "name": "Otwa Events, Long Acres",
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "Otwa Events, Long Acres, Ndeke Road",
          "addressLocality": "Lusaka",
          "addressCountry": "ZM"
        }
      }
    }
  ]
}
</script>
"""

MINISTRIES_BODY = f"""
{hero(
    "Ministries &amp; fellowships",
    "A place to belong and to grow.",
    "Church is more than a Sunday service. It is men and women, youth and children, homes and neighbourhoods — learning to follow Jesus together.",
    f'<div class="page-hero__actions">{button("Find your place", "contact.html")}{button("Plan a visit", "branches-transport.html", "btn-outline")}</div>',
    image="photos/hero-ministry.webp",
)}

<section class="section">
  <div class="container">
    <div class="split split--wide">
      <div class="split__body reveal">
        <p class="eyebrow">Life together</p>
        <h2 class="h2">Every season has a room.</h2>
        <p class="lead">We want every person who walks through our doors to find more than a seat — a place to grow, to serve and to be known.</p>
        <p>Our ministries are not separate churches. They are expressions of one family, each making room for a different season of life while keeping the same centre: the Word, prayer and love.</p>
        <blockquote class="year-card year-card--quote" style="position:relative;top:auto;padding:18px">
          <p class="scripture" style="font-size:1.02rem">“And let us consider one another in order to stir up love and good works, not forsaking the assembling of ourselves together.”</p>
          <p class="scripture" style="font-size:.76rem"><cite>Hebrews 10:24–25</cite></p>
        </blockquote>
      </div>
      <div class="split__media reveal" data-delay="1">
        <img src="photos/thumb-fellowship.webp" srcset="photos/quick-fellowship.webp 420w, photos/thumb-fellowship.webp 640w, photos/card-fellowship.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="Fellowship at RPAI" width="900" height="700" loading="lazy" decoding="async" style="min-height:390px">
      </div>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    {section_head("Our ministries", "Find your people.", "Four communities, one family. Each one is a doorway into deeper fellowship and service.")}
    <div class="grid grid-2">
      <article class="card card--hover reveal">
        <div class="card__media card__media--wide"><img src="photos/thumb-men.webp" srcset="photos/quick-men.webp 420w, photos/thumb-men.webp 640w, photos/card-men.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="Royal Men's Fellowship" width="900" height="560" loading="lazy" decoding="async"></div>
        <div class="card__body">
          <span class="card__label">Men</span>
          <h3 class="h3 mt-1">Royal Men’s Fellowship <span class="muted">(The Pillars)</span></h3>
          <p class="card__text">A brotherhood of men learning to lead with integrity, pray with courage and carry responsibility with grace. We sharpen one another, study the Word and serve the house together.</p>
          <div class="card__foot"><a class="link-arrow" href="contact.html">Ask about the fellowship</a></div>
        </div>
      </article>
      <article class="card card--hover reveal" data-delay="1">
        <div class="card__media card__media--wide"><img src="photos/thumb-women.webp" srcset="photos/quick-women.webp 420w, photos/thumb-women.webp 640w, photos/card-women.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="Virtuous Women's Ministry" width="900" height="560" loading="lazy" decoding="async"></div>
        <div class="card__body">
          <span class="card__label">Women</span>
          <h3 class="h3 mt-1">Virtuous Women’s Ministry</h3>
          <p class="card__text">A community of women growing in faith, purpose and friendship. We pray together, study the Word, celebrate milestones and support one another through every season.</p>
          <div class="card__foot"><a class="link-arrow" href="contact.html">Ask about the ministry</a></div>
        </div>
      </article>
      <article class="card card--hover reveal" data-delay="2">
        <div class="card__media card__media--wide"><img src="photos/thumb-youth.webp" srcset="photos/quick-youth.webp 420w, photos/thumb-youth.webp 640w, photos/card-youth.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="NextGen Youth and Teen Ministry" width="900" height="560" loading="lazy" decoding="async"></div>
        <div class="card__body">
          <span class="card__label">Next generation</span>
          <h3 class="h3 mt-1">NextGen Youth &amp; Teen Ministry</h3>
          <p class="card__text">A place for young people to ask honest questions, grow in their own faith and discover their gifts. We combine fun, friendship and discipleship that meets them where they are.</p>
          <div class="card__foot"><a class="link-arrow" href="contact.html">Ask about NextGen</a></div>
        </div>
      </article>
      <article class="card card--hover reveal" data-delay="3">
        <div class="card__media card__media--wide"><img src="photos/thumb-leadership.webp" srcset="photos/quick-leadership.webp 420w, photos/thumb-leadership.webp 640w, photos/card-leadership.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="Home cell and branch fellowships" width="900" height="560" loading="lazy" decoding="async"></div>
        <div class="card__body">
          <span class="card__label">Home cells</span>
          <h3 class="h3 mt-1">Home Cell &amp; Branch Fellowships</h3>
          <p class="card__text">Church beyond Sunday. Home cells gather across Lusaka for prayer, Bible study, encouragement and practical support. It is where the family becomes personal.</p>
          <div class="card__foot"><a class="link-arrow" href="branches-transport.html">Find a fellowship</a></div>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_head("The rhythm", "Three doors into the life of the house.", "Whether you are new or have been here for years, these are the easiest next steps.")}
    <div class="grid grid-3">
      <article class="reveal"><span class="story-card__num">01</span><h3 class="h3 mt-2">Sunday Divine Service</h3><p class="card__text">Worship, the Word and prayer at 09:00 AM at Otwa Events, Long Acres.</p><div class="card__foot"><a class="link-arrow" href="branches-transport.html">Plan your visit</a></div></article>
      <article class="reveal" data-delay="1"><span class="story-card__num">02</span><h3 class="h3 mt-2">Midweek fellowship</h3><p class="card__text">Wednesday at 05:30 PM — a smaller space for teaching, questions and prayer.</p><div class="card__foot"><a class="link-arrow" href="contact.html">Contact us</a></div></article>
      <article class="reveal" data-delay="2"><span class="story-card__num">03</span><h3 class="h3 mt-2">A home cell near you</h3><p class="card__text">Share life, study Scripture and pray with people who live close to you.</p><div class="card__foot"><a class="link-arrow" href="branches-transport.html#cells">Find a home cell</a></div></article>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="split split--wide">
      <div class="split__media reveal">
        <img src="photos/thumb-community.webp" srcset="photos/quick-community.webp 420w, photos/thumb-community.webp 640w, photos/card-community.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="Serving the community at RPAI" width="900" height="700" loading="lazy" decoding="async" style="min-height:390px">
      </div>
      <div class="split__body reveal" data-delay="1">
        <p class="eyebrow">Serve with us</p>
        <h2 class="h2">Serving together, growing together.</h2>
        <p>Every gift matters. Whether you can welcome a guest, sing, teach a child, set up a room, pray with someone or help behind the scenes, there is a place for you.</p>
        <ul class="check-list">
          <li>Hospitality and welcome</li>
          <li>Worship, choir and media</li>
          <li>Children, teens and youth</li>
          <li>Prayer, follow-up and practical care</li>
        </ul>
        <div class="row mt-2">
          {button("Tell us how you can serve", "contact.html")}
          {button("Send a prayer request", "contact.html#prayer", "btn-ghost")}
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="cta-card reveal">
      <p class="eyebrow" style="justify-self:center">You belong here</p>
      <h2 class="h2">Find your place in the family.</h2>
      <p>Come for a Sunday, visit a home cell, or talk to us about the ministry that fits your season.</p>
      <div class="cta-card__actions">
        {button("Plan your visit", "branches-transport.html")}
        {button("Contact us", "contact.html", "btn-outline")}
      </div>
      {share_row()}
    </div>
  </div>
</section>
"""

GALLERY_ITEMS = [
    ("worship", "Sunday worship", "quick-worship.webp"),
    ("worship", "Lifting one voice", "quick-praise.webp"),
    ("worship", "The choir", "quick-choir.webp"),
    ("worship", "Songs of the Lord", "quick-music.webp"),
    ("word", "The Word taught", "quick-word.webp"),
    ("word", "Preaching the Gospel", "quick-preaching.webp"),
    ("word", "Our shepherd", "quick-pastor.webp"),
    ("word", "Leadership together", "quick-leadership.webp"),
    ("prayer", "A moment of prayer", "quick-prayer.webp"),
    ("prayer", "The congregation", "quick-congregation.webp"),
    ("family", "The RPAI family", "quick-family.webp"),
    ("family", "Welcome home", "quick-welcome.webp"),
    ("family", "Celebration", "quick-celebration.webp"),
    ("family", "Milestones", "quick-graduation.webp"),
    ("youth", "NextGen", "quick-youth.webp"),
    ("community", "Community", "quick-community.webp"),
    ("community", "Fellowship", "quick-fellowship.webp"),
    ("community", "Royal Men", "quick-men.webp"),
    ("community", "Virtuous Women", "quick-women.webp"),
    ("worship", "Worship leader", "quick-worship-leader.webp"),
]

GALLERY_HTML = "\n".join(
    f'<button class="gallery-item" type="button" data-gallery-item data-category="{category}" data-caption="{caption}" data-full="photos/{name}" aria-label="View {caption}">'
    f'<img src="photos/{name}" alt="{caption} at Royal Priesthood Assemblies International" loading="lazy" decoding="async" width="600" height="450">'
    f'<span class="gallery-caption">{caption}</span></button>'
    for category, caption, name in GALLERY_ITEMS
)

GALLERY_BODY = f"""
{hero(
    "Media gallery",
    "Moments of grace.",
    "A glimpse of what God is doing in our family — from Sunday worship to prayer, fellowship and celebration.",
    f'<div class="page-hero__actions">{button("Watch and listen", YOUTUBE)}{button("Our story", "about.html", "btn-outline")}</div>',
    image="photos/hero-gallery.webp",
)}

<section class="section">
  <div class="container" data-gallery>
    <div class="filter-bar reveal">
      <div class="search-box">
        {ICONS['search']}
        <label class="sr-only" for="gallery-search">Search photographs</label>
        <input id="gallery-search" type="search" placeholder="Search photographs…" data-gallery-search autocomplete="off">
      </div>
      <div class="chip-row" role="group" aria-label="Filter photographs">
        <button class="chip" type="button" data-gallery-filter="all" aria-pressed="true">All</button>
        <button class="chip" type="button" data-gallery-filter="worship" aria-pressed="false">Worship</button>
        <button class="chip" type="button" data-gallery-filter="word" aria-pressed="false">The Word</button>
        <button class="chip" type="button" data-gallery-filter="prayer" aria-pressed="false">Prayer</button>
        <button class="chip" type="button" data-gallery-filter="family" aria-pressed="false">Family</button>
        <button class="chip" type="button" data-gallery-filter="youth" aria-pressed="false">NextGen</button>
        <button class="chip" type="button" data-gallery-filter="community" aria-pressed="false">Community</button>
      </div>
    </div>

    <p class="gallery-count mt-2" data-gallery-count aria-live="polite"></p>
    <div class="gallery-grid">
      {GALLERY_HTML}
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="split split--wide">
      <div class="split__body reveal">
        <p class="eyebrow">Watch</p>
        <h2 class="h2">Faith comes by hearing.</h2>
        <p>Follow the church’s official channels for live services, messages, worship and announcements. If you cannot be with us in person, join us online.</p>
        <div class="media-links mt-2">
          <a class="media-link" href="{YOUTUBE}" target="_blank" rel="noopener"><span class="media-link__icon">{ICONS['youtube']}</span><span class="media-link__text"><strong>YouTube</strong><span>Messages, worship and church highlights</span></span></a>
          <a class="media-link" href="{FACEBOOK}" target="_blank" rel="noopener"><span class="media-link__icon">{ICONS['facebook']}</span><span class="media-link__text"><strong>Facebook</strong><span>Live services and church updates</span></span></a>
          <a class="media-link" href="announcements.html"><span class="media-link__icon">{ICONS['bell']}</span><span class="media-link__text"><strong>Announcements</strong><span>The latest news from the family</span></span></a>
        </div>
      </div>
      <a class="video-card reveal" data-delay="1" href="{YOUTUBE}" target="_blank" rel="noopener" aria-label="Watch RPAI on YouTube">
        <img src="photos/thumb-music.webp" srcset="photos/quick-music.webp 420w, photos/thumb-music.webp 640w, photos/card-music.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="Worship at RPAI" width="900" height="600" loading="lazy" decoding="async">
        <span class="video-card__play"><span>{ICONS['play']}</span></span>
        <span class="video-card__label">Watch worship and messages on YouTube</span>
      </a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split split--wide">
      <div class="split__body reveal">
        <p class="eyebrow">Listen</p>
        <h2 class="h2">Worship for the road.</h2>
        <p class="lead">Take a moment to listen. These recordings are shared from the life of the church for personal encouragement.</p>
      </div>
      <div class="audio-list reveal" data-delay="1">
        <div class="audio-item"><div><strong>Worship session</strong><span>Recorded live at RPAI</span></div><audio controls preload="none" src="audio-song-013d05.mp3"></audio></div>
        <div class="audio-item"><div><strong>Song of praise</strong><span>From the RPAI choir</span></div><audio controls preload="none" src="audio-song-56a527.mp3"></audio></div>
        <div class="audio-item"><div><strong>Message excerpt</strong><span>A word for the journey</span></div><audio controls preload="none" src="audio-message-5d1ec3.mp3"></audio></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="cta-card reveal">
      <p class="eyebrow" style="justify-self:center">Be part of the picture</p>
      <h2 class="h2">The best moments are shared.</h2>
      <p>Come and worship with us this Sunday, or invite someone who needs a family.</p>
      <div class="cta-card__actions">
        {button("Plan your visit", "branches-transport.html")}
        {button("I am visiting church on Sunday", "attend.html", "btn-outline")}
      </div>
      {share_row()}
    </div>
  </div>
</section>

<dialog class="lightbox" id="galleryLightbox" aria-label="Photograph viewer">
  <div class="lightbox__head">
    <div><p class="lightbox__caption" data-lightbox-caption></p><p class="lightbox__count" data-lightbox-count></p></div>
    <button class="icon-btn" type="button" data-lightbox-close aria-label="Close viewer">{ICONS['close']}</button>
  </div>
  <div class="lightbox__stage"><img data-lightbox-image src="" alt=""></div>
  <div class="lightbox__nav">
    <button class="icon-btn" type="button" data-lightbox-prev aria-label="Previous photograph">{ICONS['left']}</button>
    <button class="icon-btn" type="button" data-lightbox-next aria-label="Next photograph">{ICONS['right']}</button>
  </div>
</dialog>
"""

IMPACT_BODY = f"""
{hero(
    "Our impact",
    "Grace that reaches beyond the walls.",
    "What happens on Sunday is meant to shape Monday. We measure impact by lives being formed, families being strengthened and love being carried into the community.",
    f'<div class="page-hero__actions">{button("Share your story", "testimonies.html#share")}{button("Our story", "about.html", "btn-outline")}</div>',
    image="photos/hero-impact.webp",
)}

<section class="section section--tight">
  <div class="container">
    <div class="stat-grid reveal">
      <div class="stat"><div class="stat__value">4</div><div class="stat__label">ministry communities</div><div class="stat__note">Men, women, NextGen, home cells</div></div>
      <div class="stat"><div class="stat__value">2</div><div class="stat__label">weekly gatherings</div><div class="stat__note">Sunday and midweek</div></div>
      <div class="stat"><div class="stat__value">09:00</div><div class="stat__label">Sunday worship</div><div class="stat__note">Every week, in person</div></div>
      <div class="stat"><div class="stat__value">1</div><div class="stat__label">gospel</div><div class="stat__note">For every generation</div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_head("Where it shows", "Faith made visible.", "The fruit of grace is not only in what we say, but in how we live.")}
    <div class="grid grid-3">
      <article class="reveal"><span class="story-card__num">01</span><h3 class="h3 mt-2">Worship</h3><p class="card__text">A church learning to honour God with whole lives — Sunday and every day.</p></article>
      <article class="reveal" data-delay="1"><span class="story-card__num">02</span><h3 class="h3 mt-2">Discipleship</h3><p class="card__text">People growing in Scripture, prayer and obedience, not simply attending services.</p></article>
      <article class="reveal" data-delay="2"><span class="story-card__num">03</span><h3 class="h3 mt-2">Fellowship</h3><p class="card__text">Relationships where people are known, carried and encouraged through hard seasons.</p></article>
      <article class="reveal" data-delay="3"><span class="story-card__num">04</span><h3 class="h3 mt-2">Service</h3><p class="card__text">Practical care that meets needs and shows the love of Christ in action.</p></article>
      <article class="reveal" data-delay="4"><span class="story-card__num">05</span><h3 class="h3 mt-2">Next generation</h3><p class="card__text">Children and youth given room to grow, ask questions and take their place.</p></article>
      <article class="reveal" data-delay="5"><span class="story-card__num">06</span><h3 class="h3 mt-2">Community</h3><p class="card__text">A church that looks beyond its walls and seeks the good of the city.</p></article>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="feature reveal">
      <div class="feature__body">
        <span class="feature__badge">{ICONS['heart']} Our foundation</span>
        <div><p class="eyebrow">A house of prayer</p><h2 class="h2">Nothing grows without prayer.</h2></div>
        <p class="lead">Before the programmes, the plans and the services, there is a God who hears. Prayer is not a department of church life; it is the life of the church.</p>
        <ul class="feature__list">
          <li><span class="feature__icon">{ICONS['heart']}</span><span><strong>Prayer for one another</strong><span>We carry each other’s burdens before the Lord.</span></span></li>
          <li><span class="feature__icon">{ICONS['heart']}</span><span><strong>Prayer for the city</strong><span>Seeking God’s peace and good for Lusaka.</span></span></li>
          <li><span class="feature__icon">{ICONS['heart']}</span><span><strong>Prayer for the next generation</strong><span>Standing in the gap for those coming after us.</span></span></li>
        </ul>
        <div class="row">{button("Send a prayer request", "contact.html#prayer")}{button("Plan your visit", "branches-transport.html", "btn-ghost")}</div>
      </div>
      <div class="feature__media"><img src="photos/thumb-welcome.webp" srcset="photos/quick-welcome.webp 420w, photos/thumb-welcome.webp 640w, photos/card-welcome.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="Prayer at RPAI" width="900" height="700" loading="lazy" decoding="async"></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split split--wide">
      <div class="split__body reveal">
        <p class="eyebrow">Our gatherings</p>
        <h2 class="h2">A rhythm that forms us.</h2>
        <p class="lead">We gather to be sent. Every service, every home cell and every prayer meeting is meant to shape how we live when we scatter.</p>
        <div class="detail-list mt-2">
          <div><dt>Sunday Divine Service</dt><dd><strong>09:00 AM CAT</strong> · Otwa Events, Long Acres, Lusaka</dd></div>
          <div><dt>Midweek Interactive Fellowship</dt><dd><strong>Wednesday · 05:30 PM CAT</strong> · In person and online</dd></div>
          <div><dt>Home cells</dt><dd>Across Lusaka · Ask us for the one nearest to you</dd></div>
        </div>
        <div class="row mt-2">{button("Plan your visit", "branches-transport.html")}{button("Find a home cell", "branches-transport.html#cells", "btn-ghost")}</div>
      </div>
      <div class="split__media reveal" data-delay="1">
        <img src="photos/thumb-congregation.webp" srcset="photos/quick-congregation.webp 420w, photos/thumb-congregation.webp 640w, photos/card-congregation.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="The congregation gathered at RPAI" width="900" height="700" loading="lazy" decoding="async" style="min-height:390px">
      </div>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="cta-card reveal">
      <p class="eyebrow" style="justify-self:center">Be part of the story</p>
      <h2 class="h2">Your life can be a testimony.</h2>
      <p>Come and see what God is doing, or share what He has already done.</p>
      <div class="cta-card__actions">
        {button("Plan your visit", "branches-transport.html")}
        {button("Share your testimony", "testimonies.html#share", "btn-outline")}
      </div>
      {share_row()}
    </div>
  </div>
</section>
"""

VISIT_BODY = f"""
{hero(
    "Plan your visit",
    "Come as you are.",
    "We would love to welcome you in person. Sunday Divine Service begins at 09:00 AM CAT at Otwa Events, Long Acres, along Ndeke Road.",
    f'<div class="page-hero__actions">{button("Get directions", MAP_URL)}{button("Ask about transport", WHATSAPP + "?text=Hello%20RPAI%2C%20I%20would%20like%20to%20ask%20about%20Sunday%20transport.", "btn-outline")}</div>',
    image="photos/hero-branches.webp",
)}

<section class="section">
  <div class="container">
    <div class="split split--wide">
      <div class="split__body reveal">
        <p class="eyebrow">Sunday at RPAI</p>
        <h2 class="h2">A seat saved for you.</h2>
        <p class="lead">From the first greeting to the final prayer, there is room for you and your family.</p>
        <div class="detail-list">
          <div><dt>Sunday Divine Service</dt><dd><strong>09:00 AM CAT</strong> · Every Sunday</dd></div>
          <div><dt>Midweek Interactive Fellowship</dt><dd><strong>Wednesday · 05:30 PM CAT</strong> · In person and online</dd></div>
          <div><dt>Where we meet</dt><dd><strong>Otwa Events, Long Acres</strong><br>Ndeke Road, Lusaka, Zambia</dd></div>
        </div>
        <div class="row mt-2">
          {button("Open directions", MAP_URL)}
          {button("Call the church", "tel:" + PHONE_TEL, "btn-ghost")}
        </div>
      </div>
      <div class="map-card reveal" data-delay="1">
        <div class="map-card__inner">
          <span class="map-card__pin">{ICONS['pin']}</span>
          <h3>Otwa Events, Long Acres</h3>
          <p>Ndeke Road, Lusaka. Look for the RPAI welcome team at the entrance.</p>
          <a class="link-arrow" href="{MAP_URL}" target="_blank" rel="noopener">Open in Google Maps</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--flush-top" id="transport">
  <div class="container">
    <div class="split split--wide">
      <div class="split__body reveal">
        <p class="eyebrow">Coming from outside Lusaka?</p>
        <h2 class="h2">Let us help you find your way.</h2>
        <p>If you are visiting from another town or country, tell us when you are coming and what you need. We will do our best to help with directions, transport and a warm welcome.</p>
        <ul class="check-list">
          <li>Ask about Sunday transport and pickup points.</li>
          <li>Tell us if you are coming with children or a group.</li>
          <li>Let us know if you need help finding the venue.</li>
        </ul>
        <p class="small">Prefer WhatsApp? <a class="gold" href="{WHATSAPP}?text=Hello%20RPAI%2C%20I%20am%20visiting%20Lusaka%20and%20would%20like%20to%20attend.">Message the church office</a>.</p>
      </div>
      <form class="form-card reveal" data-delay="1" data-rpai-mail-form data-subject="Visit enquiry — RPAI website">
        <div class="form-grid">
          <div class="form-field"><label for="visit-name">Full name</label><input id="visit-name" name="name" type="text" autocomplete="name" required></div>
          <div class="form-field"><label for="visit-phone">Phone / WhatsApp</label><input id="visit-phone" name="phone" type="tel" autocomplete="tel" required></div>
          <div class="form-field"><label for="visit-email">Email <span>optional</span></label><input id="visit-email" name="email" type="email" autocomplete="email"></div>
          <div class="form-field"><label for="visit-country">Coming from</label><input id="visit-country" name="coming_from" type="text" placeholder="City / country"></div>
          <div class="form-field"><label for="visit-date">Date of visit</label><input id="visit-date" name="visit_date" type="date"></div>
          <div class="form-field"><label for="visit-needs">What do you need?</label><select id="visit-needs" name="needs"><option>Directions only</option><option>Sunday transport</option><option>Help for a family or group</option><option>Accommodation guidance</option><option>Something else</option></select></div>
          <div class="form-field form-field--full"><label for="visit-message">Tell us more</label><textarea id="visit-message" name="message" placeholder="How can we help you prepare for your visit?"></textarea></div>
          <label class="form-check form-field--full"><input type="checkbox" name="consent" value="yes" required> I am happy for the church to contact me about this visit.</label>
        </div>
        <div class="row mt-3"><button class="btn btn-primary" type="submit">Send visit enquiry</button><span class="form-status" data-form-status role="status"></span></div>
        <p class="form-note mt-2">This form opens your email app. You can also WhatsApp <a class="gold" href="{WHATSAPP}">{PHONE_DISPLAY}</a>.</p>
      </form>
    </div>
  </div>
</section>

<section class="section" id="cells">
  <div class="container">
    {section_head("Fellowship locations", "Find a church community near you.", "RPAI gathers in homes and branch fellowships, including gatherings in Chalala. Contact the church for current meeting locations, schedules and details about other branches.")}
    <div class="grid grid-3">
      <article class="reveal"><span class="card__label">Sunday</span><h3 class="h3 mt-2">Main gathering</h3><p class="card__text">Otwa Events, Long Acres, Ndeke Road, Lusaka. Sunday at 09:00 AM.</p><div class="card__foot"><a class="link-arrow" href="{MAP_URL}" target="_blank" rel="noopener">Directions</a></div></article>
      <article class="reveal" data-delay="1"><span class="card__label">Home cell</span><h3 class="h3 mt-2">Chalala fellowship</h3><p class="card__text">A local gathering for prayer, Bible study and friendship. Contact us for the current meeting details.</p><div class="card__foot"><a class="link-arrow" href="contact.html">Ask about Chalala</a></div></article>
      <article class="reveal" data-delay="2"><span class="card__label">Transport</span><h3 class="h3 mt-2">Need a ride?</h3><p class="card__text">Ask about current Sunday transport availability, pickup points and arrangements.</p><div class="card__foot"><a class="link-arrow" href="{WHATSAPP}?text=Hello%20RPAI%2C%20I%20would%20like%20to%20ask%20about%20Sunday%20transport.">Ask on WhatsApp</a></div></article>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    {section_head("What to expect", "A warm welcome. A living Word.", "You do not need to have it all together to come. Just come.", center=True)}
    <div class="grid grid-4">
      <article class="reveal"><span class="story-card__num">01</span><h3 class="h3 mt-2">A welcome</h3><p class="card__text">Someone will greet you, help you find a seat and answer your questions.</p></article>
      <article class="reveal" data-delay="1"><span class="story-card__num">02</span><h3 class="h3 mt-2">Worship</h3><p class="card__text">Songs, prayer and space to meet with God — no performance required.</p></article>
      <article class="reveal" data-delay="2"><span class="story-card__num">03</span><h3 class="h3 mt-2">The Word</h3><p class="card__text">A practical message from Scripture that speaks to everyday life.</p></article>
      <article class="reveal" data-delay="3"><span class="story-card__num">04</span><h3 class="h3 mt-2">Family</h3><p class="card__text">Children and teens are welcome. Ask us about NextGen and children’s activities.</p></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_head("Before you come", "A few practical answers.", "", center=True)}
    {faq([
        ("Do I need to tell you I am coming?", "You are always welcome to simply arrive. If you use the visit form, we can look out for you and help with transport or directions."),
        ("Is there parking?", "Yes. Otwa Events has parking at the venue. Our welcome team will help you find your way."),
        ("What time should I arrive?", "Arrive a little before 09:00 AM so you have time to park, meet the welcome team and settle in."),
        ("Can I bring my children?", "Yes. Children are part of the family. Ask our team about children’s activities and NextGen on the day."),
        ("How do I ask about transport?", "Send a WhatsApp message or use the visit form above. We will confirm current availability and pickup points."),
    ])}
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="cta-card reveal">
      <p class="eyebrow" style="justify-self:center">We will look out for you</p>
      <h2 class="h2">Your first Sunday starts here.</h2>
      <p>Tell us you are coming, or simply arrive at 09:00 AM. Either way, you are welcome.</p>
      <div class="cta-card__actions">
        {button("I am visiting church on Sunday", "attend.html")}
        {button("Contact us", "contact.html", "btn-outline")}
      </div>
      {share_row()}
    </div>
  </div>
</section>
"""

GIVE_BODY = f"""
{hero(
    "Give",
    "Worship through generosity.",
    "Giving is an act of worship. It supports the ministry of the Word, prayer, discipleship and practical care for people in our church family and community.",
    f'<div class="page-hero__actions">{button("Talk to the church office", WHATSAPP + "?text=Hello%20RPAI%2C%20I%20would%20like%20to%20give%20and%20need%20the%20current%20giving%20details.")}{button("Why we give", "#ways", "btn-outline")}</div>',
    image="photos/hero-give.webp",
)}

<section class="section section--tight">
  <div class="container">
    <div class="year-card year-card--quote reveal" style="position:relative;top:auto">
      <span class="year-card__era">A word for the giver</span>
      <p class="scripture">"Honour the Lord with your possessions, and with the firstfruits of all your increase."</p>
      <p class="scripture"><cite>Proverbs 3:9</cite></p>
    </div>
  </div>
</section>

<section class="section" id="ways">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Ways to give</p>
      <h2 class="h2">Giving details</h2>
      <p class="lead">Give directly to any of our Zambian bank accounts. Please use your name as the reference so the church can acknowledge your gift.</p>
    </div>

    <h3 class="h3 mt-4 reveal">Mobile Money</h3>
    <div class="grid grid-3 mt-2">
      <article class="pay-card reveal">
        <div class="pay-card__logo"><img src="https://cdn.simpleicons.org/airtel/EB1C24" alt="Airtel Mobile Money" width="72" height="72" loading="lazy" decoding="async"></div>
        <h4 class="h3 mt-2">AIRTEL MOBILE MONEY</h4>
        <dl class="detail-list mt-2">
          <div><dt>Number</dt><dd class="rpai-bank-pending">To be confirmed</dd></div>
          <div><dt>Name</dt><dd>Royal Priesthood Assemblies International</dd></div>
        </dl>
      </article>
      <article class="pay-card reveal" data-delay="1">
        <div class="pay-card__logo"><img src="https://upload.wikimedia.org/wikipedia/commons/a/af/MTN_Logo.svg" alt="MTN Mobile Money" width="72" height="72" loading="lazy" decoding="async"></div>
        <h4 class="h3 mt-2">MTN MOBILE MONEY</h4>
        <dl class="detail-list mt-2">
          <div><dt>Number</dt><dd class="rpai-bank-pending">To be confirmed</dd></div>
          <div><dt>Name</dt><dd>Royal Priesthood Assemblies International</dd></div>
        </dl>
      </article>
      <article class="pay-card reveal" data-delay="2">
        <div class="pay-card__logo"><img src="payment-zamtel.png" alt="Zamtel Mobile Money" width="72" height="72" loading="lazy" decoding="async"></div>
        <h4 class="h3 mt-2">ZAMTEL MOBILE MONEY</h4>
        <dl class="detail-list mt-2">
          <div><dt>Number</dt><dd class="rpai-bank-pending">To be confirmed</dd></div>
          <div><dt>Name</dt><dd>Royal Priesthood Assemblies International</dd></div>
        </dl>
      </article>
    </div>

    <h3 class="h3 mt-4 reveal">Zambian banks</h3>
    <div class="grid grid-2 mt-2">
      <article class="pay-card reveal">
        <div class="pay-card__logo pay-card__logo--wide"><img src="bank-zanaco.png" alt="Zanaco logo" width="120" height="32" loading="lazy" decoding="async"></div>
        <h3 class="h3 mt-2">Zanaco</h3>
        <p class="small muted">Zambia National Commercial Bank</p>
        <dl class="detail-list mt-2">
          <div><dt>Account number</dt><dd class="rpai-bank-pending">To be confirmed</dd></div>
          <div><dt>Account name</dt><dd>Royal Priesthood Assemblies International</dd></div>
          <div><dt>Centre</dt><dd>Lusaka Main Centre</dd></div>
        </dl>
      </article>
      <article class="pay-card reveal" data-delay="1">
        <div class="pay-card__logo pay-card__logo--wide"><img src="bank-stanbic.svg" alt="Stanbic Bank logo" width="120" height="32" loading="lazy" decoding="async"></div>
        <h3 class="h3 mt-2">Stanbic Bank</h3>
        <p class="small muted">Stanbic Bank Zambia</p>
        <dl class="detail-list mt-2">
          <div><dt>Account number</dt><dd class="rpai-bank-pending">To be confirmed</dd></div>
          <div><dt>Account name</dt><dd>Royal Priesthood Assemblies International</dd></div>
          <div><dt>Centre</dt><dd>Lusaka Main Centre</dd></div>
        </dl>
      </article>
      <article class="pay-card reveal">
        <div class="pay-card__logo"><img src="bank-absa.png" alt="Absa Bank logo" width="64" height="64" loading="lazy" decoding="async"></div>
        <h3 class="h3 mt-2">Absa Bank</h3>
        <p class="small muted">Absa Bank Zambia</p>
        <dl class="detail-list mt-2">
          <div><dt>Account number</dt><dd class="rpai-bank-pending">To be confirmed</dd></div>
          <div><dt>Account name</dt><dd>Royal Priesthood Assemblies International</dd></div>
          <div><dt>Centre</dt><dd>Lusaka Main Centre</dd></div>
        </dl>
      </article>
      <article class="pay-card reveal" data-delay="1">
        <div class="pay-card__logo pay-card__logo--wide"><img src="bank-fnb.png" alt="First National Bank logo" width="110" height="60" loading="lazy" decoding="async"></div>
        <h3 class="h3 mt-2">First National Bank</h3>
        <p class="small muted">FNB Zambia</p>
        <dl class="detail-list mt-2">
          <div><dt>Account number</dt><dd class="rpai-bank-pending">To be confirmed</dd></div>
          <div><dt>Account name</dt><dd>Royal Priesthood Assemblies International</dd></div>
          <div><dt>Centre</dt><dd>Lusaka Main Centre</dd></div>
        </dl>
      </article>
      <article class="pay-card reveal">
        <div class="pay-card__logo pay-card__logo--wide"><img src="bank-standard-chartered.svg" alt="Standard Chartered logo" width="130" height="51" loading="lazy" decoding="async"></div>
        <h3 class="h3 mt-2">Standard Chartered</h3>
        <p class="small muted">Standard Chartered Zambia</p>
        <dl class="detail-list mt-2">
          <div><dt>Account number</dt><dd class="rpai-bank-pending">To be confirmed</dd></div>
          <div><dt>Account name</dt><dd>Royal Priesthood Assemblies International</dd></div>
          <div><dt>Centre</dt><dd>Lusaka Main Centre</dd></div>
        </dl>
      </article>
    </div>

    <h3 class="h3 mt-4 reveal">International giving</h3>
    <div class="card card--pad reveal mt-2">
      <p>Giving from outside Zambia? Use our only international gateway, PayPal.</p>
      <dl class="detail-list mt-2">
        <div><dt>PayPal email</dt><dd class="rpai-bank-pending">To be confirmed</dd></div>
        <div><dt>Account name</dt><dd class="rpai-bank-pending">To be confirmed</dd></div>
      </dl>
      <p class="form-note mt-2">For help with any of these details, contact the church office.</p>
    </div>

    <div class="logo-strip mt-4" aria-hidden="true">
      <div class="marquee">
        <div class="marquee__group">
          <img src="https://cdn.simpleicons.org/airtel/EB1C24" alt="Airtel" width="56" height="56" loading="lazy" decoding="async">
          <img src="https://upload.wikimedia.org/wikipedia/commons/a/af/MTN_Logo.svg" alt="MTN" width="56" height="56" loading="lazy" decoding="async">
          <img src="payment-zamtel.png" alt="Zamtel" width="56" height="56" loading="lazy" decoding="async">
          <img src="bank-zanaco.png" alt="Zanaco" width="150" height="40" loading="lazy" decoding="async">
          <img src="bank-stanbic.svg" alt="Stanbic Bank" width="150" height="40" loading="lazy" decoding="async">
          <img src="bank-absa.png" alt="Absa Bank" width="56" height="56" loading="lazy" decoding="async">
          <img src="bank-fnb.png" alt="First National Bank" width="110" height="60" loading="lazy" decoding="async">
          <img src="bank-standard-chartered.svg" alt="Standard Chartered" width="160" height="63" loading="lazy" decoding="async">
        </div>
        <div class="marquee__group">
          <img src="https://cdn.simpleicons.org/airtel/EB1C24" alt="Airtel" width="56" height="56" loading="lazy" decoding="async">
          <img src="https://upload.wikimedia.org/wikipedia/commons/a/af/MTN_Logo.svg" alt="MTN" width="56" height="56" loading="lazy" decoding="async">
          <img src="payment-zamtel.png" alt="Zamtel" width="56" height="56" loading="lazy" decoding="async">
          <img src="bank-zanaco.png" alt="Zanaco" width="150" height="40" loading="lazy" decoding="async">
          <img src="bank-stanbic.svg" alt="Stanbic Bank" width="150" height="40" loading="lazy" decoding="async">
          <img src="bank-absa.png" alt="Absa Bank" width="56" height="56" loading="lazy" decoding="async">
          <img src="bank-fnb.png" alt="First National Bank" width="110" height="60" loading="lazy" decoding="async">
          <img src="bank-standard-chartered.svg" alt="Standard Chartered" width="160" height="63" loading="lazy" decoding="async">
        </div>
      </div>
    </div>

    <div class="note-box mt-4 reveal"><strong>Important:</strong> The church will never ask you to send money to a personal account. If you are unsure about any giving detail, please confirm directly with the church office before sending anything.</div>
    <div class="reveal mt-4" style="text-align:center">
      <p class="small">Questions about giving? Contact the church office.</p>
      <div class="row mt-2" style="justify-content:center">
        {button("WhatsApp the office", WHATSAPP, "btn-primary")}
        {button("Contact us", "contact.html", "btn-outline")}
      </div>
    </div>
  </div>
</section>
"""

DEVOTIONAL_BODY = f"""
{hero(
    "Daily devotional",
    "Start today with God.",
    "A quiet moment in the Word can change the shape of your day. Read, reflect and pray — then carry His presence with you.",
    f'<div class="page-hero__actions">{button("Read today’s devotional", "https://read.rhapsodyofrealities.org/")}{button("Watch a message", YOUTUBE, "btn-outline")}</div>',
    image="photos/hero-devotional.webp",
)}

<section class="section">
  <div class="container">
    <div class="split split--wide">
      <div class="devotional-card reveal">
        <p class="eyebrow">Today’s word</p>
        <p class="scripture mt-2">“Through the Lord’s mercies we are not consumed, because His compassions fail not. They are new every morning; great is Your faithfulness.”</p>
        <p class="scripture"><cite>Lamentations 3:22–23</cite></p>
        <p class="mt-3">God’s mercy is not a reserve for special days. It is new this morning — for the meeting you are dreading, the conversation you need to have, the strength you feel you do not have.</p>
        <p class="mt-2">Begin here: receive His mercy, then walk in it. You do not have to manufacture faithfulness today; you are invited to trust the One who is faithful.</p>
        <div class="row mt-3">{button("Read the full devotional", "https://read.rhapsodyofrealities.org/")}{button("Send a prayer request", "contact.html#prayer", "btn-ghost")}</div>
      </div>
      <div class="split__body reveal" data-delay="1">
        <p class="eyebrow">A simple rhythm</p>
        <h2 class="h2">Read. Reflect. Pray.</h2>
        <div class="number-list mt-2">
          <li><div><strong>Read</strong>Open the Word and read slowly. Ask the Holy Spirit to speak to you.</div></li>
          <li><div><strong>Reflect</strong>What does this reveal about God? What is He asking of you today?</div></li>
          <li><div><strong>Pray</strong>Turn what you have read into conversation — thanks, confession, request, surrender.</div></li>
          <li><div><strong>Carry</strong>Choose one small act of obedience and do it today.</div></li>
        </div>
        <div class="note-box mt-4"><strong>Rhapsody of Realities</strong><br>Read the complete daily devotional from the official Rhapsody of Realities reading page.</div>
      </div>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    {section_head("This week", "A reading plan for the week.", "Seven short readings to help you stay rooted. Read one each day.")}
    <div class="grid grid-3">
      <article class="day-card reveal"><span>Day 1</span><strong>Psalm 23</strong><p>The Lord is my shepherd. Rest in His care.</p></article>
      <article class="day-card reveal" data-delay="1"><span>Day 2</span><strong>Isaiah 40:28–31</strong><p>Strength for the weary. Wait on the Lord.</p></article>
      <article class="day-card reveal" data-delay="2"><span>Day 3</span><strong>Philippians 4:4–9</strong><p>Peace that guards the heart.</p></article>
      <article class="day-card reveal" data-delay="3"><span>Day 4</span><strong>James 1:19–25</strong><p>Hear the Word and put it into practice.</p></article>
      <article class="day-card reveal" data-delay="4"><span>Day 5</span><strong>1 Peter 2:9–10</strong><p>A royal priesthood, called into light.</p></article>
      <article class="day-card reveal" data-delay="5"><span>Day 6</span><strong>Matthew 5:13–16</strong><p>Salt and light in everyday life.</p></article>
      <article class="day-card reveal" data-delay="6"><span>Day 7</span><strong>Hebrews 10:19–25</strong><p>Draw near, hold fast, gather together.</p></article>
      <article class="day-card reveal" data-delay="7"><span>Every day</span><strong>Pray without ceasing</strong><p>Keep the conversation with God open all day.</p></article>
      <article class="day-card reveal" data-delay="8"><span>Every day</span><strong>Walk in love</strong><p>Let what you read become how you treat people.</p></article>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="cta-card reveal">
      <p class="eyebrow" style="justify-self:center">Grow together</p>
      <h2 class="h2">You were not made to read alone.</h2>
      <p>Join a home cell or come and study with the family this week.</p>
      <div class="cta-card__actions">
        {button("Find a home cell", "branches-transport.html#cells")}
        {button("Contact us", "contact.html", "btn-outline")}
      </div>
      {share_row()}
    </div>
  </div>
</section>
"""

ANNOUNCEMENTS_BODY = f"""
{hero(
    "Announcements",
    "What’s happening in the family.",
    "The latest notices from Royal Priesthood Assemblies International. Check back here for service changes, gatherings and church news.",
    f'<div class="page-hero__actions">{button("See service times", "branches-transport.html")}{button("Contact us", "contact.html", "btn-outline")}</div>',
    image="photos/hero-announcements.webp",
)}

<section class="section">
  <div class="container">
    <article class="notice reveal" data-announcement-card aria-busy="true">
      <div class="notice__meta" data-announcement-meta>Latest update <time data-announcement-time datetime="2026-10-25">25 October 2026</time></div>
      <h2>Latest announcement</h2>
      <div class="notice__body" data-announcement-message>
        <p>Sunday service moves to 8am from 1 December.</p>
      </div>
      <div class="row mt-3"><a class="link-arrow" href="branches-transport.html">Plan your Sunday</a></div>
    </article>
    <p class="small mt-2">This notice refreshes automatically from the church’s announcement file. If it cannot refresh, the published notice above remains visible.</p>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    {section_head("Also good to know", "A few standing notices.", "These are the regular rhythms and reminders for the church family.")}
    <div class="grid grid-3">
      <article class="reveal"><span class="card__label">Sunday</span><h3 class="h3 mt-2">Divine Service</h3><p class="card__text">Join us every Sunday at 09:00 AM CAT at Otwa Events, Long Acres, Ndeke Road, Lusaka.</p><div class="card__foot"><a class="link-arrow" href="branches-transport.html">Plan your visit</a></div></article>
      <article class="reveal" data-delay="1"><span class="card__label">Wednesday</span><h3 class="h3 mt-2">Midweek fellowship</h3><p class="card__text">Interactive fellowship at 05:30 PM CAT. Join us in person or online.</p><div class="card__foot"><a class="link-arrow" href="contact.html">Contact us</a></div></article>
      <article class="reveal" data-delay="2"><span class="card__label">Home cells</span><h3 class="h3 mt-2">Fellowship near you</h3><p class="card__text">Home cells gather across Lusaka, including Chalala. Ask us for the group nearest to you.</p><div class="card__foot"><a class="link-arrow" href="branches-transport.html#cells">Find a home cell</a></div></article>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="cta-card reveal">
      <p class="eyebrow" style="justify-self:center">Stay close</p>
      <h2 class="h2">Never miss a word from the house.</h2>
      <p>Follow the church on Facebook and YouTube for live services, messages and updates.</p>
      <div class="cta-card__actions">
        {button("Follow on Facebook", FACEBOOK)}
        {button("Watch on YouTube", YOUTUBE, "btn-outline")}
      </div>
      {share_row()}
    </div>
  </div>
</section>
"""

CONFERENCE_BODY = f"""
{hero(
    "Online with RPAI",
    "You don’t have to miss church.",
    "Join the meeting from your phone, tablet or computer. No app and no account are needed — just a quiet space and a heart ready to worship.",
    f'<div class="page-hero__actions">{button("Request the meeting link", "#register")}{button("See the meeting details", "#meeting", "btn-outline")}</div>',
    image="photos/hero-conference.webp",
)}

<section class="section">
  <div class="container">
    <div class="split split--wide">
      <div class="split__media reveal">
        <img src="photos/thumb-pastor.webp" srcset="photos/quick-pastor.webp 420w, photos/thumb-pastor.webp 640w, photos/card-pastor.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="Worship team leading the church in praise" width="1100" height="700" loading="lazy" decoding="async" style="min-height:400px">
      </div>
      <div class="split__body reveal" data-delay="1">
        <p class="eyebrow">Online with RPAI</p>
        <h2 class="h2">Church wherever you are.</h2>
        <p class="lead">Join the church family for worship, prayer and the Word from your phone or computer.</p>
        <p>Whether you are travelling, unwell, caring for family or simply far from Lusaka, you can still gather with us. Request the meeting link by email and it will be sent to you automatically.</p>
        <ul class="check-list">
          <li>No app required — the room opens in your browser.</li>
          <li>Allow camera and microphone only if you want to be seen and heard.</li>
          <li>Your email is used only to send the meeting link.</li>
        </ul>
        <div class="row mt-2">{button("Request the link", "#register")}{button("Watch on YouTube", YOUTUBE, "btn-ghost")}</div>
      </div>
    </div>
  </div>
</section>

<section class="section section--flush-top" id="meeting">
  <div class="container">
    {section_head("The meeting", "Join us from anywhere.", "The meeting card below is updated by the church office. If details do not load, contact us for the current link.", center=True)}
    <div class="split split--wide">
      <section class="rpai-conference-card reveal" aria-labelledby="conference-meeting-title">
        <span class="eyebrow">The meeting</span>
        <p class="rpai-conference-status is-loading" data-conference-status role="status" aria-live="polite">Loading meeting details</p>
        <h2 data-conference-title id="conference-meeting-title">RPAI Online Meeting</h2>
        <p class="rpai-conference-schedule" data-conference-schedule>Sundays at 9:00 AM CAT</p>
        <p class="rpai-conference-description" data-conference-description>Join the church family for worship, prayer and the Word from your phone or computer.</p>
        <dl class="rpai-conference-details">
          <div><dt>Host</dt><dd data-conference-host>Royal Priesthood Assemblies International</dd></div>
          <div data-conference-dialin hidden><dt>Backup dial-in</dt><dd><a data-conference-phone href="#register">Phone number</a></dd></div>
          <div data-conference-code hidden><dt>Backup access code</dt><dd data-conference-code-value></dd></div>
        </dl>
        <a aria-disabled="true" class="btn btn-primary rpai-conference-join is-disabled" data-conference-join href="#register">Request the link</a>
        <p class="rpai-conference-powered" data-conference-powered>The room opens in your browser through Jitsi Meet — no account or app needed.</p>
        <p class="rpai-conference-powered" data-conference-backup-wrap hidden><a data-conference-backup href="#" rel="noopener noreferrer" target="_blank">Open the backup meeting link</a></p>
      </section>

      <div id="register" class="reveal" data-delay="1">
        <div class="form-card">
          <p class="eyebrow">Get the link</p>
          <h2 class="h2 mt-1" data-conference-form-heading>Receive the meeting link by email</h2>
          <p class="small mt-1" data-conference-form-intro>Enter your name and email address. The link is sent automatically, so no one has to send it by hand.</p>
          <form data-conference-form class="mt-2">
            <div class="form-grid">
              <div class="form-field form-field--full"><label for="conference-name">Name <span class="rpai-optional">(optional)</span></label><input class="form-control" id="conference-name" name="name" type="text" maxlength="120" autocomplete="name" disabled></div>
              <div class="form-field form-field--full"><label for="conference-email">Email address</label><input class="form-control" id="conference-email" name="email" type="email" inputmode="email" maxlength="254" autocomplete="email" required disabled></div>
              <div class="form-field form-field--full"><label class="form-check"><input id="conference-consent" name="consent" type="checkbox" required disabled> I agree to register for this meeting and receive the meeting link.</label></div>
              <div class="rpai-conference-honeypot" aria-hidden="true"><label for="conference-website">Leave this field empty</label><input id="conference-website" name="website" type="text" tabindex="-1" autocomplete="off" disabled></div>
            </div>
            <div class="row mt-3"><button class="btn btn-primary" type="submit" disabled>Register and join</button><span class="rpai-form-status" data-conference-form-status role="status" aria-live="polite">Please wait while the meeting details load.</span></div>
            <a class="btn btn-primary mt-3" data-conference-form-join href="#" target="_blank" rel="noopener noreferrer" hidden>Join the meeting now</a>
            <p class="rpai-conference-privacy mt-2">We use your email only to register you for this meeting. It is not added to a marketing list and is never shown publicly.</p>
          </form>
          <noscript><p class="form-note mt-2">The registration form needs JavaScript. Please email <a class="gold" href="mailto:{EMAIL}">{EMAIL}</a> or message us on WhatsApp for the meeting link.</p></noscript>
        </div>
      </div>
    </div>

    <section aria-label="Embedded meeting room" class="rpai-conference-room" data-conference-room hidden>
      <div class="rpai-conference-room-head">
        <div><span class="eyebrow">Live room</span><h2 class="h2 mt-1">You are in the meeting room</h2></div>
        <button class="btn btn-primary" data-conference-leave type="button">Leave meeting</button>
      </div>
      <div class="rpai-conference-embed" data-conference-embed></div>
      <p class="rpai-conference-room-status" data-conference-room-status role="status" aria-live="polite"></p>
      <p class="rpai-conference-room-note">If the room does not load, <a data-conference-room-open href="https://meet.jit.si" rel="noopener noreferrer" target="_blank">open it in a new tab</a>.</p>
    </section>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split split--wide">
      <div class="split__body reveal">
        <p class="eyebrow">How it works</p>
        <h2 class="h2">From your inbox to the meeting.</h2>
        <p class="lead">Three simple steps. No account is needed to join.</p>
        <div class="number-list mt-2">
          <li><div><strong>Request the link</strong>Enter your email on this page and submit the form.</div></li>
          <li><div><strong>Check your inbox</strong>The meeting link arrives automatically. Check the spam folder if you do not see it.</div></li>
          <li><div><strong>Join the meeting</strong>Press the join button on this page, or open the link from your email. The room works in the browser.</div></li>
        </div>
      </div>
      <div class="split__media reveal" data-delay="1">
        <img src="photos/thumb-worship.webp" srcset="photos/quick-worship.webp 420w, photos/thumb-worship.webp 640w, photos/card-worship.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="Worship at RPAI" width="900" height="700" loading="lazy" decoding="async" style="min-height:370px">
      </div>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    {section_head("Before you join", "A few honest answers.", "", center=True)}
    {faq([
        ("Do I need a Jitsi account or an app?", "No. The room opens in your browser. Allow the camera and microphone when the browser asks. No account is needed."),
        ("How long can a meeting last?", "Jitsi’s free public service currently limits a meeting to 95 minutes. For a longer service, the church may publish a backup link on the meeting card."),
        ("Can I join by phone instead of video?", "If the church has published a backup dial-in number and access code, they appear on the meeting card. If they are not shown, use the room on a phone or computer."),
        ("Is my email safe?", "Yes. We use your email only to register you for the meeting. It is not added to a marketing list and is never shown publicly."),
        ("What if the room does not load?", "Use the “open it in a new tab” link in the meeting room, or contact the church office on WhatsApp and we will help."),
    ])}
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="cta-card reveal">
      <p class="eyebrow" style="justify-self:center">Gather with us</p>
      <h2 class="h2">Distance is no longer a reason to miss church.</h2>
      <p>Request the link, or join us in person this Sunday at 09:00 AM.</p>
      <div class="cta-card__actions">
        {button("Request the link", "#register")}
        {button("Plan your visit", "branches-transport.html", "btn-outline")}
      </div>
      {share_row()}
    </div>
  </div>
</section>
"""

CONTACT_BODY = f"""
{hero(
    "Contact us",
    "Talk to us.",
    "Whether you need prayer, directions, a conversation or simply want to say hello, we would be glad to hear from you.",
    f'<div class="page-hero__actions">{button("Send a prayer request", "#prayer")}{button("Plan your visit", "branches-transport.html", "btn-outline")}</div>',
    image="photos/hero-contact.webp",
)}

<section class="section">
  <div class="container">
    <div class="contact-grid">
      <a class="contact-card reveal" href="{WHATSAPP}" target="_blank" rel="noopener"><span class="contact-card__icon">{ICONS['whatsapp']}</span><div><strong>WhatsApp</strong><p>{PHONE_DISPLAY}</p><span>Fastest way to reach the church office</span></div></a>
      <a class="contact-card reveal" data-delay="1" href="tel:{PHONE_TEL}"><span class="contact-card__icon">{ICONS['phone']}</span><div><strong>Call</strong><p>{PHONE_DISPLAY}</p><span>Speak to the church office</span></div></a>
      <a class="contact-card reveal" data-delay="2" href="mailto:{EMAIL}"><span class="contact-card__icon">{ICONS['mail']}</span><div><strong>Email</strong><p>{EMAIL}</p><span>For enquiries, prayer and giving</span></div></a>
      <a class="contact-card reveal" data-delay="3" href="{MAP_URL}" target="_blank" rel="noopener"><span class="contact-card__icon">{ICONS['pin']}</span><div><strong>Visit</strong><p>Otwa Events, Long Acres</p><span>Ndeke Road, Lusaka, Zambia</span></div></a>
    </div>
  </div>
</section>

<section class="section section--flush-top" id="prayer">
  <div class="container">
    <div class="split split--wide">
      <form class="form-card reveal" data-rpai-mail-form data-subject="Prayer request — RPAI website">
        <p class="eyebrow">Prayer request</p>
        <h2 class="h2 mt-1">How can we pray with you?</h2>
        <p class="small mt-1">Your request will be handled prayerfully and privately by the pastoral team.</p>
        <div class="form-grid mt-2">
          <div class="form-field"><label for="prayer-name">Full name</label><input id="prayer-name" name="name" type="text" autocomplete="name" required></div>
          <div class="form-field"><label for="prayer-phone">Phone / WhatsApp <span>optional</span></label><input id="prayer-phone" name="phone" type="tel" autocomplete="tel"></div>
          <div class="form-field form-field--full"><label for="prayer-email">Email <span>optional</span></label><input id="prayer-email" name="email" type="email" autocomplete="email"></div>
          <div class="form-field form-field--full"><label for="prayer-request">Your prayer request</label><textarea id="prayer-request" name="request" required placeholder="Share as much or as little as you are comfortable with…"></textarea></div>
          <label class="form-check form-field--full"><input type="checkbox" name="consent" value="yes" required> I am happy for the church to contact me about this request.</label>
        </div>
        <div class="row mt-3"><button class="btn btn-primary" type="submit">Send prayer request</button><span class="form-status" data-form-status role="status"></span></div>
        <p class="form-note mt-2">This form opens your email app. If you prefer, message us on <a class="gold" href="{WHATSAPP}">WhatsApp</a>.</p>
      </form>

      <form class="form-card reveal" data-delay="1" data-rpai-mail-form data-subject="Connect card — RPAI website">
        <p class="eyebrow">Connect card</p>
        <h2 class="h2 mt-1">Let us know you came.</h2>
        <p class="small mt-1">Visiting for the first time? Tell us a little about yourself and we will help you take the next step.</p>
        <div class="form-grid mt-2">
          <div class="form-field"><label for="connect-name">Full name</label><input id="connect-name" name="name" type="text" autocomplete="name" required></div>
          <div class="form-field"><label for="connect-phone">Phone / WhatsApp</label><input id="connect-phone" name="phone" type="tel" autocomplete="tel" required></div>
          <div class="form-field form-field--full"><label for="connect-email">Email <span>optional</span></label><input id="connect-email" name="email" type="email" autocomplete="email"></div>
          <div class="form-field"><label for="connect-visit">Are you new?</label><select id="connect-visit" name="visit"><option>First-time visitor</option><option>Returning visitor</option><option>Member</option><option>Just exploring</option></select></div>
          <div class="form-field"><label for="connect-interest">I am interested in</label><select id="connect-interest" name="interest"><option>Attending a service</option><option>A home cell</option><option>NextGen youth</option><option>Men’s or women’s fellowship</option><option>Serving on a team</option><option>Prayer</option></select></div>
          <div class="form-field form-field--full"><label for="connect-message">Anything else? <span>optional</span></label><textarea id="connect-message" name="message" placeholder="Tell us how we can help…"></textarea></div>
          <label class="form-check form-field--full"><input type="checkbox" name="consent" value="yes" required> I am happy for the church to contact me.</label>
        </div>
        <div class="row mt-3"><button class="btn btn-primary" type="submit">Send connect card</button><span class="form-status" data-form-status role="status"></span></div>
      </form>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split split--wide">
      <div class="split__body reveal">
        <p class="eyebrow">Find us</p>
        <h2 class="h2">Worship with us any week.</h2>
        <div class="service-list mt-2">
          <div class="service-item"><div><strong>Sunday Divine Service</strong><span>Every Sunday · in person</span></div><time datetime="09:00">09:00 AM</time></div>
          <div class="service-item"><div><strong>Midweek Interactive Fellowship</strong><span>Wednesday · in person and online</span></div><time datetime="17:30">05:30 PM</time></div>
          <div class="service-item"><div><strong>Home cells</strong><span>Across Lusaka · ask for the nearest group</span></div><time>Weekly</time></div>
        </div>
        <address class="mt-3" style="font-style:normal;color:var(--soft);font-size:13.5px">{ADDRESS}</address>
        <div class="row mt-2">{button("Get directions", MAP_URL)}{button("Ask about transport", WHATSAPP + "?text=Hello%20RPAI%2C%20I%20would%20like%20to%20ask%20about%20Sunday%20transport.", "btn-ghost")}</div>
      </div>
      <div class="map-card reveal" data-delay="1">
        <div class="map-card__inner">
          <span class="map-card__pin">{ICONS['pin']}</span>
          <h3>Otwa Events, Long Acres</h3>
          <p>Ndeke Road, Lusaka. Our welcome team will help you find your way.</p>
          <a class="link-arrow" href="{MAP_URL}" target="_blank" rel="noopener">Open in Google Maps</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="between">
      <div class="section-head reveal" style="margin-bottom:0"><p class="eyebrow">Follow us</p><h2 class="h2">Stay connected.</h2><p class="lead">Live services, messages, worship and church updates.</p></div>
      <div class="social-grid reveal" data-delay="1">
        <a class="social-pill" href="{FACEBOOK}" target="_blank" rel="noopener"><img src="icon-facebook.svg" alt="" width="15" height="15"> Facebook</a>
        <a class="social-pill" href="{YOUTUBE}" target="_blank" rel="noopener"><img src="icon-youtube.svg" alt="" width="15" height="15"> YouTube</a>
        <a class="social-pill" href="{WHATSAPP}" target="_blank" rel="noopener"><img src="icon-whatsapp.svg" alt="" width="15" height="15"> WhatsApp</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    {section_head("Questions people ask", "Before you reach out.", "", center=True)}
    {faq([
        ("What is the best way to contact the church?", "WhatsApp is usually the fastest. You can also call, email or send a prayer request through the form on this page."),
        ("How quickly will someone respond?", "We aim to respond within a day or two. Prayer requests are handled by the pastoral team as soon as possible."),
        ("Can I request a visit from the pastor?", "Yes. Send a message with your name, location and the reason for the visit. The office will follow up."),
        ("I am new. What should I do first?", "Fill in the connect card or simply come to a Sunday service. Our welcome team will help you take the next step."),
    ])}
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="cta-card reveal">
      <p class="eyebrow" style="justify-self:center">We are here</p>
      <h2 class="h2">You do not have to walk alone.</h2>
      <p>Send a prayer request, ask a question, or come and meet the family this Sunday.</p>
      <div class="cta-card__actions">
        {button("WhatsApp the church", WHATSAPP)}
        {button("Plan your visit", "branches-transport.html", "btn-outline")}
      </div>
      {share_row()}
    </div>
  </div>
</section>
"""

ATTEND_BODY = f"""
{hero(
    "I Am Attending",
    "Tell people you’re coming.",
    "Make your own welcome card, then share it with family and friends. Add your name and a photo — everything stays on your device.",
    f'<div class="page-hero__actions">{button("Plan your visit", "branches-transport.html")}{button("Get directions", MAP_URL, "btn-outline")}</div>',
    image="photos/hero-attend.webp",
)}

<section class="section">
  <div class="container">
    <div class="card-maker" data-card-maker>
      <div class="card-maker__preview reveal">
        <canvas width="1080" height="1350" data-card-canvas role="img" aria-label="Preview of your I Am Attending card">Your browser does not support the card preview. You can still join us this Sunday at 09:00 AM.</canvas>
        <p class="form-note center">Preview · 1080 × 1350 · ready for WhatsApp and social media</p>
      </div>
      <div class="card-maker__controls reveal" data-delay="1">
        <div class="step-chips" aria-hidden="true">
          <span class="step-chip"><b>1</b> Add your name</span>
          <span class="step-chip"><b>2</b> Add a photo</span>
          <span class="step-chip"><b>3</b> Download and share</span>
        </div>
        <div class="form-field">
          <label for="attend-name">Your name</label>
          <input id="attend-name" type="text" maxlength="40" value="Your Name" placeholder="Your name" data-card-name autocomplete="name">
        </div>
        <div class="upload-box">
          {ICONS['upload']}
          <strong>Add your photo</strong>
          <span>JPG or PNG. Your photo never leaves your device.</span>
          <label class="sr-only" for="attend-photo">Choose a photo</label>
          <input id="attend-photo" type="file" accept="image/*" data-card-photo>
        </div>
        <div>
          <p class="small soft" style="margin-bottom:7px">Choose a background</p>
          <div class="backdrop-row" role="group" aria-label="Card background">
            <button class="backdrop-swatch" type="button" data-card-backdrop="1" aria-pressed="true" aria-label="Gold on black"></button>
            <button class="backdrop-swatch backdrop-swatch--2" type="button" data-card-backdrop="2" aria-pressed="false" aria-label="Gold on navy"></button>
            <button class="backdrop-swatch backdrop-swatch--3" type="button" data-card-backdrop="3" aria-pressed="false" aria-label="Gold on burgundy"></button>
            <button class="backdrop-swatch backdrop-swatch--4" type="button" data-card-backdrop="4" aria-pressed="false" aria-label="Gold on forest green"></button>
          </div>
        </div>
        <div class="card-maker__actions">
          <button class="btn btn-primary" type="button" data-card-download>Download card</button>
          <button class="btn btn-outline" type="button" data-card-share>Share</button>
          <button class="btn btn-ghost" type="button" data-card-reset>Reset</button>
        </div>
        <p class="form-status" data-card-status role="status" aria-live="polite"></p>
        <p class="form-note">Your photo is processed in your browser and is never uploaded to a server. If sharing is not available on your device, use Download card.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="split split--wide">
      <div class="split__body reveal">
        <p class="eyebrow">Your Sunday</p>
        <h2 class="h2">We will look out for you.</h2>
        <p class="lead">Sunday Divine Service begins at 09:00 AM CAT at Otwa Events, Long Acres, along Ndeke Road.</p>
        <div class="detail-list">
          <div><dt>Sunday Divine Service</dt><dd><strong>09:00 AM CAT</strong> · Every Sunday</dd></div>
          <div><dt>Midweek fellowship</dt><dd><strong>Wednesday · 05:30 PM CAT</strong> · In person and online</dd></div>
          <div><dt>Where we meet</dt><dd><strong>Otwa Events, Long Acres</strong><br>Ndeke Road, Lusaka, Zambia</dd></div>
        </div>
        <div class="row mt-2">{button("Plan your visit", "branches-transport.html")}{button("Ask about transport", WHATSAPP + "?text=Hello%20RPAI%2C%20I%20am%20coming%20this%20Sunday%20and%20would%20like%20to%20ask%20about%20transport.", "btn-ghost")}</div>
      </div>
      <div class="split__media reveal" data-delay="1">
        <img src="photos/thumb-welcome.webp" srcset="photos/quick-welcome.webp 420w, photos/thumb-welcome.webp 640w, photos/card-welcome.webp 1000w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 520px" alt="Welcome to RPAI" width="900" height="700" loading="lazy" decoding="async" style="min-height:380px">
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_head("A few helpful answers", "Before you come.", "", center=True)}
    {faq([
        ("What should I expect?", "A warm welcome, worship, prayer and a practical message from the Word. You are free to participate as much as you are comfortable."),
        ("What should I wear?", "Come as you are. Some people dress up, others come in everyday clothes. What matters is that you are here."),
        ("Is there something for children?", "Yes. Children are part of the family. Ask our welcome team about children’s activities and NextGen on the day."),
        ("Can I share my card on WhatsApp?", "Yes. Use the Share button on a supported phone, or tap Download card and attach the image to any message."),
    ])}
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="cta-card reveal">
      <p class="eyebrow" style="justify-self:center">See you Sunday</p>
      <h2 class="h2">A place of love where everyone counts.</h2>
      <p>Invite a friend, bring your family, and come as you are.</p>
      <div class="cta-card__actions">
        {button("Plan your visit", "branches-transport.html")}
        {button("Contact us", "contact.html", "btn-outline")}
      </div>
      {share_row()}
    </div>
  </div>
</section>
"""

PRIVACY_BODY = f"""
{hero(
    "Privacy",
    "Your privacy matters to us.",
    "How Royal Priesthood Assemblies International handles personal information shared through this website.",
    "",
    image="photos/hero-library.webp",
)}

<section class="section">
  <div class="container">
    <div class="prose reveal">
      <p><strong>Last updated:</strong> November 2026</p>
      <h2>Who we are</h2>
      <p>Royal Priesthood Assemblies International is a church based in Lusaka, Zambia. You can reach us at <a href="mailto:{EMAIL}">{EMAIL}</a> or on <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.</p>

      <h2>What we collect</h2>
      <p>When you use a form on this website, you may choose to share your name, email address, phone number, prayer request, testimony, visit details or other information you include in your message.</p>
      <p>Our hosting provider may also process basic technical information such as your IP address, browser type and pages visited, in order to serve the site securely.</p>

      <h2>How we use it</h2>
      <ul>
        <li>To respond to your prayer request, enquiry or message.</li>
        <li>To help you plan a visit, arrange transport or find a home cell.</li>
        <li>To follow up on a testimony or connect card, with your consent.</li>
        <li>To keep the website secure and understand how it is used.</li>
      </ul>

      <h2>Email forms</h2>
      <p>Some forms on this site open your own email application so that you can send a message directly to the church. In that case, your email is handled by your email provider and by the church’s email service.</p>
      <p>The video conference registration form sends your email address to the church’s booking service for the purpose of sending you the meeting link. It is not added to a marketing list.</p>

      <h2>Sharing</h2>
      <p>We do not sell your personal information. We may share information with trusted service providers who help us operate the website, email or video meetings, or where we are required to do so by law.</p>

      <h2>Your choices</h2>
      <p>You may ask us to access, correct or delete the personal information we hold about you, or withdraw consent for future contact. Email <a href="mailto:{EMAIL}">{EMAIL}</a> and we will respond as soon as we can.</p>

      <h2>Children</h2>
      <p>We care about the privacy of children. Please do not submit personal information about a child through this website without the consent of a parent or guardian. Children’s ministry records are handled separately by the church office.</p>

      <h2>Security</h2>
      <p>We take reasonable steps to protect the information shared with us. No method of transmission over the internet is completely secure, so please avoid sending sensitive information unless it is necessary.</p>

      <h2>Changes</h2>
      <p>We may update this notice from time to time. The date at the top of this page shows when it was last revised.</p>

      <h2>Contact</h2>
      <p>Questions about privacy? Email <a href="mailto:{EMAIL}">{EMAIL}</a> or write to us at {ADDRESS}.</p>
    </div>
  </div>
</section>
"""

TERMS_BODY = f"""
{hero(
    "Terms of use",
    "A few simple terms.",
    "Please read these terms before using the Royal Priesthood Assemblies International website.",
    "",
    image="photos/hero-conference.webp",
)}

<section class="section">
  <div class="container">
    <div class="prose reveal">
      <p><strong>Last updated:</strong> November 2026</p>
      <h2>Welcome</h2>
      <p>This website is provided by Royal Priesthood Assemblies International to share information about the church, its services, ministries and events. By using the site, you agree to these terms.</p>

      <h2>Content</h2>
      <p>We aim to keep the information on this site accurate and current, but service times, meetings and giving details can change. Please contact the church office to confirm important details before making a decision or a gift.</p>
      <p>The content, design, photographs and recordings on this site belong to the church or are used with permission. You may share links and the “I Am Attending” card for personal, non-commercial use. Please do not republish other content without permission.</p>

      <h2>Giving</h2>
      <p>Giving is voluntary. The church will never ask you to send money to a personal account. Always confirm current giving details directly with the church office before sending a gift. Giving details are provided in good faith but may change.</p>

      <h2>External links</h2>
      <p>This site may link to external websites and services, such as YouTube, Facebook, Jitsi Meet or Rhapsody of Realities. We are not responsible for the content or privacy practices of those services.</p>

      <h2>Video meetings</h2>
      <p>Online meetings are provided for worship, prayer and fellowship. Please be respectful to others, protect your own privacy and do not record or share a meeting without the consent of those taking part.</p>

      <h2>Testimonies and submissions</h2>
      <p>If you share a testimony or other content with us, you confirm that it is your own story and that you have permission to share it. We will not publish a testimony without your consent, and we may edit for length or clarity.</p>

      <h2>Limitation</h2>
      <p>The website is provided as is. To the extent permitted by law, the church is not liable for any loss arising from reliance on information on this site or from interruptions to the site.</p>

      <h2>Contact</h2>
      <p>Questions about these terms? Email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.</p>
    </div>
  </div>
</section>
"""


if __name__ == "__main__":
    write_page("index", HOME_BODY, HOME_HEAD)
    write_page("about", ABOUT_BODY)
    write_page("pastor", PASTOR_BODY)
    write_page("testimonies", TESTIMONIES_BODY)
    write_page("ministries", MINISTRIES_BODY)
    write_page("gallery", GALLERY_BODY)
    write_page("impact", IMPACT_BODY)
    write_page("visit", VISIT_BODY)
    write_page("give", GIVE_BODY)
    write_page("devotional", DEVOTIONAL_BODY, marquee=False)
    write_page("announcements", ANNOUNCEMENTS_BODY, scripts_extra='<script src="js__announcement.js?v=4" defer></script>', marquee=False)
    write_page("contact", CONTACT_BODY)
    write_page("attend", ATTEND_BODY)
    write_page("privacy", PRIVACY_BODY)
    write_page("terms", TERMS_BODY)








