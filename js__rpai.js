(function () {
	'use strict';

	var churchEmail = 'royalpriesthoodassembliesintl@gmail.com';

	/* Keep the footer copyright current without document.write. The markup ships
	   with the current year, so the page is still correct when JavaScript is off. */
	var rpaiYear = function () {
		var year = String(new Date().getFullYear());
		document.querySelectorAll('[data-rpai-year]').forEach(function (element) {
			element.textContent = year;
		});
	};

	rpaiYear();

	/* The gallery uses tiny-slider, which marks the off-screen slides with
	   aria-hidden="true" but leaves their links focusable. That traps keyboard
	   and screen-reader users, so mirror aria-hidden with the inert attribute.

	   Tiny Slider replaces the container node when it is destroyed and rebuilt
	   by the "Show all pictures" toggle, so the observer cannot be attached once
	   and forgotten. Rebuilds announce themselves with rpai:gallery-rebuilt and
	   the sync is re-attached to whatever container is in the document now. */
	var galleryInertObservers = [];

	var markSlidesInert = function (gallery) {
		gallery.querySelectorAll('.tns-item').forEach(function (item) {
			if (item.getAttribute('aria-hidden') === 'true') {
				item.setAttribute('inert', '');
			} else {
				item.removeAttribute('inert');
			}
		});
	};

	var syncGalleryInert = function () {
		/* Stop watching containers that Tiny Slider has replaced. */
		galleryInertObservers = galleryInertObservers.filter(function (entry) {
			if (entry.gallery.isConnected) return true;
			entry.observer.disconnect();
			return false;
		});

		document.querySelectorAll('.rpai-media-gallery').forEach(function (gallery) {
			if (!gallery.__rpaiInert) {
				gallery.__rpaiInert = true;
				galleryInertObservers.push({
					gallery: gallery,
					observer: new MutationObserver(function () { markSlidesInert(gallery); })
				});
			}
			galleryInertObservers.forEach(function (entry) {
				if (entry.gallery === gallery) {
					entry.observer.observe(gallery, {
						subtree: true,
						attributes: true,
						attributeFilter: ['aria-hidden']
					});
				}
			});
			markSlidesInert(gallery);
		});
	};

	syncGalleryInert();
	document.addEventListener('rpai:gallery-rebuilt', syncGalleryInert);

	/* A direct WhatsApp contact button on every page. It is added here so the
	   existing page markup does not need to be repeated or changed. */
	var rpaiWhatsApp = function () {
		if (document.querySelector('.rpai-whatsapp-float')) return;
		var link = document.createElement('a');
		link.className = 'rpai-whatsapp-float';
		link.href = 'https://wa.me/260767716936?text=' + encodeURIComponent('Hello RPAI, I would like to know more about the church.');
		link.target = '_blank';
		link.rel = 'noopener noreferrer';
		link.setAttribute('aria-label', 'Chat with Royal Priesthood Assemblies International on WhatsApp');
		link.innerHTML = '<img src="icon-whatsapp.svg?v=1" width="28" height="28" loading="lazy" decoding="async" alt="">';
		document.body.appendChild(link);
	};

	rpaiWhatsApp();

	/* Back-to-top control, revealed after the visitor has read a little. */
	var rpaiBackToTop = function () {
		var button = document.querySelector('.rpai-back-to-top');
		if (!button) {
			button = document.createElement('button');
			button.type = 'button';
			button.className = 'rpai-back-to-top';
			button.setAttribute('aria-label', 'Back to top');
			button.innerHTML = '&uarr;';
			button.addEventListener('click', function () {
				window.scrollTo({ top: 0, behavior: 'smooth' });
			});
			document.body.appendChild(button);
		}

		var toggle = function () {
			button.classList.toggle('is-visible', window.scrollY > 600);
		};

		window.addEventListener('scroll', toggle, { passive: true });
		toggle();
	};

	rpaiBackToTop();

	/* --- Mobile menu -------------------------------------------------------
	   The theme's own menu script toggles the off-canvas menu but leaves three
	   things undone: the close control is a bare <span> that no keyboard can
	   reach, the burger never reports whether the menu is open, and Escape does
	   nothing. All three are fixed here rather than in the theme's own file. */
	var rpaiMobileMenu = function () {
		var body = document.body;
		var burger = document.querySelector('a.js-menu-toggle');
		if (!burger) return;

		var isOpen = function () {
			return body.classList.contains('offcanvas-menu');
		};

		/* aria-expanded on the burger, kept in step with the body class the
		   theme script toggles. The label changes with it. */
		var syncBurger = function () {
			var open = isOpen();
			burger.setAttribute('aria-expanded', String(open));
			burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
		};
		new MutationObserver(syncBurger).observe(body, {
			attributes: true,
			attributeFilter: ['class']
		});
		syncBurger();

		/* The close control is drawn as a <span>, so Enter and Space have to be
		   handled by hand. Anything natively focusable is left to the browser. */
		document.querySelectorAll('.js-menu-toggle').forEach(function (control) {
			if (control.tagName === 'A' || control.tagName === 'BUTTON' || control.tagName === 'INPUT') return;
			control.addEventListener('keydown', function (event) {
				if (event.key !== 'Enter' && event.key !== ' ' && event.key !== 'Spacebar') return;
				event.preventDefault();
				control.click();
			});
		});

		/* Escape closes the menu and hands focus back to the burger, so the
		   keyboard user is not dropped at the top of the page. */
		document.addEventListener('keydown', function (event) {
			if (event.key !== 'Escape' || !isOpen()) return;
			body.classList.remove('offcanvas-menu');
			document.querySelectorAll('.js-menu-toggle').forEach(function (control) {
				control.classList.remove('active');
			});
			syncBurger();
			burger.focus();
		});
	};

	rpaiMobileMenu();

	document.querySelectorAll('[data-rpai-mail-form]').forEach(function (form) {
		form.addEventListener('submit', function (event) {
			event.preventDefault();
			if (!form.reportValidity()) return;

			var formData = new FormData(form);
			var message = Array.from(formData.entries())
				.map(function (entry) { return entry[0] + ': ' + entry[1]; })
				.join('\n');
			var subject = form.getAttribute('data-subject');
			var status = form.querySelector('[data-form-status]');

			status.textContent = 'Your email app is opening with your message ready. Please review and send it to the church.';
			window.location.href = 'mailto:' + churchEmail + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(message);
		});
	});
})();
