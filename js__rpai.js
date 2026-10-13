(function () {
	'use strict';

	var churchEmail = 'royalpriesthoodassembliesintl@gmail.com';

	/* The gallery uses tiny-slider, which marks the off-screen slides with
	   aria-hidden="true" but leaves their links focusable. That traps keyboard
	   and screen-reader users, so mirror aria-hidden with the inert attribute. */
	document.querySelectorAll('.rpai-media-gallery').forEach(function (gallery) {
		var syncInert = function () {
			gallery.querySelectorAll('.tns-item').forEach(function (item) {
				if (item.getAttribute('aria-hidden') === 'true') {
					item.setAttribute('inert', '');
				} else {
					item.removeAttribute('inert');
				}
			});
		};

		syncInert();
		new MutationObserver(syncInert).observe(gallery, {
			subtree: true,
			attributes: true,
			attributeFilter: ['aria-hidden']
		});
	});

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
