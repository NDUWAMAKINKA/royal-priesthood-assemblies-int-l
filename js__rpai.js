(function () {
	'use strict';

	var churchEmail = 'royalpriesthoodassembliesintl@gmail.com';

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
