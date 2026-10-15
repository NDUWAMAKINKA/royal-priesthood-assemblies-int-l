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

		var mediaGallery = document.querySelectorAll('.rpai-media-gallery');

		if ( mediaGallery.length > 0 ) {
			/* Anyone who has asked their system to reduce motion gets a still
			   gallery. Everyone else gets the slideshow, always running. */
			var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

			/* Options are held in a function so the slider can be rebuilt after it
			   has been destroyed. Showing every photo tears the carousel down; going
			   back to the slideshow builds it again. */
			var galleryOptions = function () {
				return {
					container: '.rpai-media-gallery',
					mode: 'carousel',
					items: 4,
					slideBy: 'page',
					gutter: 24,
					speed: 700,
					loop: false,
					rewind: true,
					/* The slideshow must never simply stop. With loop off,
					   autoplay halts on the last page and the pictures sit still
					   for ever. wrapAtEnd() puts it back to the first page once it
					   reaches the end, so it keeps running. */
					preventInteractionOnWrap: false,
					autoplay: !prefersReducedMotion,
					autoplayTimeout: 4000,
					/* Hover must NOT stop the slideshow. The gallery spans the page,
					   so with autoplayHoverPause on, simply resting a cursor near it
					   froze the pictures and it looked broken. Anyone who wants to
					   study a photo still has the Pause slideshow button, which is a
					   deliberate choice rather than an accident of pointer position. */
					autoplayHoverPause: false,
					autoplayButtonOutput: false,
					controls: false,
					nav: false,
					responsive: {
						0: { items: 1 },
						576: { items: 2 },
						768: { items: 3 },
						1200: { items: 4 }
					}
				};
			};

			/* tiny-slider stops its autoplay on the last page when loop is off,
			   so the photographs simply sat still until someone touched a button.
			   This sends it back to the first page once it gets there, which keeps
			   the slideshow running without changing how the buttons behave. */
			var wrapAtEnd = function (slider) {
				if (!slider || typeof slider.getInfo !== 'function') return;
				if (typeof slider.goTo !== 'function') return;
				var returning = false;
				var check = function () {
					if (returning) return;
					var info = slider.getInfo();
					if (!info || !info.slideCount) return;
					var lastPage = info.slideCount - info.items;
					if (lastPage <= 0) return;
					if (info.index >= lastPage) {
						returning = true;
						setTimeout(function () {
							try { slider.goTo(0); } catch (err) { /* nothing to do */ }
							returning = false;
						}, 150);
					}
				};
				check();
				window.setInterval(check, 400);
			};

			var gallerySlider = tns(galleryOptions());
			wrapAtEnd(gallerySlider);

			var galleryControls = document.querySelector('.rpai-gallery-controls');
			var previousButton = galleryControls.querySelector('[data-gallery-prev]');
			var nextButton = galleryControls.querySelector('[data-gallery-next]');
			var toggleButton = galleryControls.querySelector('[data-gallery-toggle]');
			var viewButton = galleryControls.querySelector('[data-gallery-view]');
			var optOutButton = document.querySelector('[data-gallery-optout]');
			var carousel = document.querySelector('.rpai-gallery-carousel');
			var slideshowPlaying = !prefersReducedMotion;

			previousButton.addEventListener('click', function () { gallerySlider.goTo('prev'); });
			nextButton.addEventListener('click', function () { gallerySlider.goTo('next'); });

			/* The button pauses a running slideshow, so it starts as "Pause". */
			toggleButton.textContent = slideshowPlaying ? 'Pause slideshow' : 'Play slideshow';
			toggleButton.setAttribute('aria-pressed', String(slideshowPlaying));
			toggleButton.addEventListener('click', function () {
				slideshowPlaying = !slideshowPlaying;
				if (slideshowPlaying) gallerySlider.play(); else gallerySlider.pause();
				toggleButton.textContent = slideshowPlaying ? 'Pause slideshow' : 'Play slideshow';
				toggleButton.setAttribute('aria-pressed', String(slideshowPlaying));
			});

			var showAllPictures = function (showingAll) {
				/* Tiny Slider's destroy() replaces the container node, so any reference
				   held across it is detached. Re-query the container each time. */
				if (showingAll) {
					/* Stop the movement but keep the visitor's play/pause choice, so
					   returning to the slideshow carries on as they left it. */
					gallerySlider.pause();
					gallerySlider.destroy();
					document.querySelector('.rpai-media-gallery').classList.add('rpai-all-pictures');
				} else {
					document.querySelector('.rpai-media-gallery').classList.remove('rpai-all-pictures');
					gallerySlider = tns(galleryOptions());
					if (slideshowPlaying) gallerySlider.play();
					/* New container node: tell the page scripts to re-attach anything
					   they had bound to the old one. */
					document.dispatchEvent(new CustomEvent('rpai:gallery-rebuilt'));
				}

				/* Marks the carousel as showing every photo, which is what reveals
				   the opt-out bar. */
				carousel.classList.toggle('rpai-showing-all', showingAll);

				/* The grid is far taller than the carousel was, so the visitor's
				   scroll position can leave the exit just off screen. Bring it
				   back into view the moment they ask to see everything. */
				if (showingAll) optOutButton.scrollIntoView({ block: 'center' });

				/* While every photo is on the page the slide buttons have nothing to
				   act on, so they are dimmed and taken out of the tab order. */
				[previousButton, nextButton, toggleButton].forEach(function (button) {
					button.disabled = showingAll;
				});

				viewButton.textContent = showingAll ? 'Show slideshow' : 'Show all pictures';
				viewButton.setAttribute('aria-pressed', String(showingAll));
			};

			viewButton.addEventListener('click', function () {
				showAllPictures(!document.querySelector('.rpai-media-gallery')
					.classList.contains('rpai-all-pictures'));
			});

			/* The way out of the all-pictures view: at the top of the grid and
			   still on screen further down, so nobody has to scroll back up. */
			optOutButton.addEventListener('click', function () {
				showAllPictures(false);
				viewButton.focus();
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