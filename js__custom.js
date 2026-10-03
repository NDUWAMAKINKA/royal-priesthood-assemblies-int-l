/* This JavaScript file makes the page feel alive. */
/* It starts animations, sliders, and small effects on the website. */
/* Think of this as the helper that makes the page move and react. */

(function () {

	'use strict'

	/* Start the scroll animation library for sections that should fade in. */
	AOS.init({
		duration: 800,
		easing: 'slide',
		once: true
	});


	/* This function hides the loading screen after a short moment. */
	/* It makes the page look smoother when visitors first open it. */
	var preloader = function() {

		var loader = document.querySelector('.loader');
		var overlay = document.getElementById('overlayer');

		function fadeOut(el) {
			el.style.opacity = 1;
			(function fade() {
				if ((el.style.opacity -= .1) < 0) {
					el.style.display = "none";
				} else {
					requestAnimationFrame(fade);
				}
			})();
		};

		setTimeout(function() {
			fadeOut(loader);
			fadeOut(overlay);
		}, 200);
	};
	preloader();
	
	/* This section creates the sliding image and testimonial carousels. */
	/* It helps the page show several items in a small space. */
	var tinyslier = function() {

		var heroSlider = document.querySelectorAll('.hero-slide');
		var propertySlider = document.querySelectorAll('.property-slider');
		var imgPropertySlider = document.querySelectorAll('.img-property-slide');
		var testimonialCenter = document.querySelectorAll('.testimonial-center');
		var mediaGallery = document.querySelectorAll('.rpai-media-gallery');
		

		if ( heroSlider.length > 0 ) {
			var tnsHeroSlider = tns({
				container: '.hero-slide',
				mode: 'carousel',
				speed: 700,
				autoplay: true,
				controls: false,
				nav: false,
				autoplayButtonOutput: false,
				controlsContainer: '#hero-nav',
			});
		}


		if ( imgPropertySlider.length > 0 ) {
			var tnsPropertyImageSlider = tns({
				container: '.img-property-slide',
				mode: 'carousel',
				speed: 700,
				items: 1,
				autoplay: true,
				controls: false,
				nav: true,
				autoplayButtonOutput: false
			});
		}

		if ( mediaGallery.length > 0 ) {
			/* Show smaller images in groups of three or four on wider screens. */
			var gallerySlider = tns({
				container: '.rpai-media-gallery',
				mode: 'carousel',
				items: 3,
				slideBy: 'page',
				gutter: 24,
				speed: 700,
				loop: false,
				rewind: true,
				autoplay: !window.matchMedia('(prefers-reduced-motion: reduce)').matches,
				autoplayTimeout: 2000,
				autoplayHoverPause: true,
				autoplayButtonOutput: false,
				controls: false,
				nav: false,
				responsive: {
					0: { items: 1 },
					576: { items: 2 },
					768: { items: 3 },
					1200: { items: 4 }
				}
			});
			var galleryControls = document.querySelector('.rpai-gallery-controls');
			var previousButton = galleryControls.querySelector('[data-gallery-prev]');
			var nextButton = galleryControls.querySelector('[data-gallery-next]');
			var toggleButton = galleryControls.querySelector('[data-gallery-toggle]');
			var slideshowPaused = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

			previousButton.addEventListener('click', function () { gallerySlider.goTo('prev'); });
			nextButton.addEventListener('click', function () { gallerySlider.goTo('next'); });
			toggleButton.textContent = slideshowPaused ? 'Play slideshow' : 'Pause slideshow';
			toggleButton.setAttribute('aria-pressed', String(slideshowPaused));
			toggleButton.addEventListener('click', function () {
				slideshowPaused = !slideshowPaused;
				if (slideshowPaused) gallerySlider.pause();
				else gallerySlider.play();
				toggleButton.textContent = slideshowPaused ? 'Play slideshow' : 'Pause slideshow';
				toggleButton.setAttribute('aria-pressed', String(slideshowPaused));
			});
		}

		if ( propertySlider.length> 0 ) {
			var tnsSlider = tns({
				container: '.property-slider',
				mode: 'carousel',
				speed: 700,
				items: 3,
				autoplay: true,
				autoplayButtonOutput: false,
				controlsContainer: '#property-nav',
				responsive: {
					0: {
						items: 1
					},
					700: {
						items: 2
					},
					900: {
						items: 3
					}
				}
			});
		}






		if ( testimonialCenter.length> 0 ) {
			var testimonialSlider = tns({
				container: '#testimonial-center',
				items: 1,
				mode: 'carousel',
				slideBy: 'page',
				nav: true,
				controls: true,
				gutter: 50,
				edgePadding: 0,
				center: true,
				controlsContainer: '#testimonial-nav',
				
				loop: false,
				swipeAngle: false,
				speed: 700,

				responsive: {
					350: {
						edgePadding: 0,
					},
					500: {
						edgePadding: 0,
						// items: 1
					},
					700: {
						edgePadding: 20,
					},
					1000: {
						edgePadding: 50,
					}
				}

			});
		}

	}
	tinyslier();

	/* This opens media in a popup lightbox so videos look nicer. */
	var lightbox = function() {
		var lightboxVideo = GLightbox({
			selector: '.glightbox'
		});
	};
	lightbox();


	/* This countdown script is used for time-based content. */
	/* It updates numbers on the page so visitors can see time remaining. */
	var countdown = function() {
		var el = document.querySelectorAll('.js-countdown');

		console.log(el.length);



		if ( el.length > 0 ) {

			const finaleDate = new Date("December 10, 2022 00:00:00").getTime();

			const timer = () =>{
				const now = new Date().getTime();
				let diff = finaleDate - now;

				if(diff < 0){

					document.querySelector('.custom-alert').style.display = 'block';
					document.querySelector('.counter-wrap').style.display = 'none';
				}

				let days = Math.floor(diff / (1000*60*60*24));
				let hours = Math.floor(diff % (1000*60*60*24) / (1000*60*60));
				let minutes = Math.floor(diff % (1000*60*60)/ (1000*60));
				let seconds = Math.floor(diff % (1000*60) / 1000);

				days <= 99 ? days = `0${days}` : days;
				days <= 9 ? days = `00${days}` : days;
				hours <= 9 ? hours = `0${hours}` : hours;
				minutes <= 9 ? minutes = `0${minutes}` : minutes;
				seconds <= 9 ? seconds = `0${seconds}` : seconds;   

				document.querySelector('#days').textContent = days;
				document.querySelector('#hours').textContent = hours;
				document.querySelector('#minutes').textContent = minutes;
				document.querySelector('#seconds').textContent = seconds;

			}
			timer();
			setInterval(timer,1000);
		}
	}

	countdown();



})()