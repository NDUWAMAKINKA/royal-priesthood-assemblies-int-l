/*
 * RPAI announcements.
 *
 * The announcements page used to embed Facebook's Page Plugin. Facebook only
 * draws that timeline for visitors who are signed in, so most people were
 * shown an empty box. The page now reads a small local JSON file instead:
 * no cookies, no third-party requests, no login.
 *
 * The card in announcements.html already holds the current announcement, so
 * the page is complete before this script runs and stays complete if the
 * request fails. The script only refreshes it from announcement.json.
 */
(function () {
	'use strict';

	var SOURCE = 'announcement.json';
	var TIMEOUT_MS = 8000;
	var MAX_MESSAGE_LENGTH = 4000;

	/* Intl understands the world languages but not every Zambian language
	   code. Falling back to English keeps the date readable rather than
	   throwing on an unsupported locale. */
	var LOCALES = {
		en: 'en-GB',
		bem: 'en-ZM', ny: 'en-ZM', nya: 'en-ZM',
		toi: 'en-ZM', loz: 'en-ZM', tum: 'en-ZM',
		hi: 'hi-IN',
		fr: 'fr-FR',
		de: 'de-DE',
		it: 'it-IT',
		pt: 'pt-PT',
		ru: 'ru-RU',
		es: 'es-ES'
	};

	function localeFor(language) {
		return LOCALES[String(language || '').toLowerCase()] || 'en-GB';
	}

	function formatDate(date, language) {
		try {
			return new Intl.DateTimeFormat(localeFor(language), {
				day: 'numeric',
				month: 'long',
				year: 'numeric',
				// The church publishes in Lusaka. Pinning the zone means a
				// visitor in another country still sees the date the notice
				// was posted, not their own yesterday or tomorrow.
				timeZone: 'Africa/Lusaka'
			}).format(date);
		} catch (error) {
			return date.toISOString().slice(0, 10);
		}
	}

	/* The date is the only text this script writes. It is formatted for the
	   language the visitor has chosen and reformatted when they switch. */
	function renderTime(card, date) {
		var meta = card.querySelector('[data-announcement-meta]');
		var time = card.querySelector('[data-announcement-time]');
		if (!meta || !time) return;

		card.__rpaiAnnouncementDate = date;
		time.setAttribute('datetime', date.toISOString());
		time.textContent = formatDate(date, document.documentElement.getAttribute('lang'));
		meta.hidden = false;
	}

	/* Announcements come from the church, not from visitors, but building the
	   text with text nodes means a stray angle bracket can never become markup.
	   A blank line starts a new paragraph; a single line break is kept. */
	function renderMessage(card, message) {
		var target = card.querySelector('[data-announcement-message]');
		if (!target) return;

		var paragraphs = message.replace(/\r\n?/g, '\n').split(/\n\s*\n/);
		target.textContent = '';

		paragraphs.forEach(function (paragraph) {
			var text = paragraph.trim();
			if (!text) return;

			var p = document.createElement('p');
			text.split('\n').forEach(function (line, index) {
				if (index > 0) p.appendChild(document.createElement('br'));
				p.appendChild(document.createTextNode(line.trim()));
			});
			target.appendChild(p);
		});

		if (!target.firstChild) target.textContent = message;
	}

	/* Accept only the shape the page can render. Anything else is treated as
	   a failed refresh, so the fallback already in the HTML stays on screen. */
	function readAnnouncement(data) {
		if (!data || typeof data !== 'object' || Array.isArray(data)) return null;
		if (typeof data.message !== 'string') return null;

		var message = data.message.replace(/\r\n?/g, '\n').trim();
		if (!message || message.length > MAX_MESSAGE_LENGTH) return null;

		/* timestamp is the field written by the GitHub Actions sync and the
		   admin bot. updatedAt is accepted from older announcement files. */
		var stamp = typeof data.timestamp === 'string' && data.timestamp
			? data.timestamp
			: data.updatedAt;

		var updatedAt = null;
		if (typeof stamp === 'string' && stamp) {
			updatedAt = new Date(stamp);
			if (isNaN(updatedAt.getTime())) updatedAt = null;
		}

		return { message: message, updatedAt: updatedAt };
	}

	function render(card, announcement) {
		renderMessage(card, announcement.message);
		if (announcement.updatedAt) renderTime(card, announcement.updatedAt);
		card.setAttribute('data-announcement-state', 'live');
	}

	function refresh(card) {
		if (typeof window.fetch !== 'function') {
			card.setAttribute('data-announcement-state', 'fallback');
			card.setAttribute('aria-busy', 'false');
			return;
		}

		card.setAttribute('aria-busy', 'true');

		var controller = typeof window.AbortController === 'function'
			? new window.AbortController()
			: null;
		var timer = window.setTimeout(function () {
			if (controller) controller.abort();
		}, TIMEOUT_MS);

		window.fetch(SOURCE, {
			cache: 'no-cache',
			credentials: 'same-origin',
			headers: { Accept: 'application/json' },
			signal: controller ? controller.signal : undefined
		}).then(function (response) {
			if (!response.ok) throw new Error('HTTP ' + response.status);
			return response.json();
		}).then(function (data) {
			var announcement = readAnnouncement(data);
			if (!announcement) throw new Error('announcement.json is not in the expected shape');
			render(card, announcement);
		}).catch(function (error) {
			/* Offline, a blocked request, or a malformed file: the card keeps
			   the published announcement already written in the HTML. */
			card.setAttribute('data-announcement-state', 'fallback');
			if (window.console && typeof window.console.warn === 'function') {
				window.console.warn('[RPAI] The announcement could not be refreshed.', error);
			}
		}).then(function () {
			window.clearTimeout(timer);
			card.setAttribute('aria-busy', 'false');
		});
	}

	function watchLanguage(card) {
		if (typeof window.MutationObserver !== 'function') return;

		new window.MutationObserver(function () {
			if (card.__rpaiAnnouncementDate) {
				renderTime(card, card.__rpaiAnnouncementDate);
			}
		}).observe(document.documentElement, {
			attributes: true,
			attributeFilter: ['lang']
		});
	}

	function init() {
		var cards = document.querySelectorAll('[data-announcement-card]');
		Array.prototype.forEach.call(cards, function (card) {
			watchLanguage(card);
			refresh(card);
		});
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', init);
	} else {
		init();
	}
})();
