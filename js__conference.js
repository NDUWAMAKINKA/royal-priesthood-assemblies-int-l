/*
 * Public Video Conference page.
 *
 * The meeting details come from the church API, which the pastor edits at
 * /admin. Jitsi is the main room and opens inside this page; the
 * FreeConferenceCall link is an optional backup. Nothing secret is stored in
 * this file: the API exposes only the meeting card and a registration endpoint
 * that emails the room link.
 */
(function () {
  'use strict';

  var isLocal = /^(localhost|127\.0\.0\.1|\[::1\])$/.test(window.location.hostname);
  var API = String(
    window.RPAI_API_BASE ||
      (isLocal ? '' : 'https://royal-priesthood-assemblies-int-l.onrender.com')
  ).replace(/\/+$/, '');
  var TIMEOUT_MS = 12000;
  var JITSI_DOMAIN = 'meet.jit.si';

  var page = document.querySelector('[data-conference-page]');
  if (!page) return;

  var statusEl = page.querySelector('[data-conference-status]');
  var titleEl = page.querySelector('[data-conference-title]');
  var scheduleEl = page.querySelector('[data-conference-schedule]');
  var descriptionEl = page.querySelector('[data-conference-description]');
  var hostEl = page.querySelector('[data-conference-host]');
  var dialInWrap = page.querySelector('[data-conference-dialin]');
  var phoneEl = page.querySelector('[data-conference-phone]');
  var codeWrap = page.querySelector('[data-conference-code]');
  var codeEl = page.querySelector('[data-conference-code-value]');
  var joinEl = page.querySelector('[data-conference-join]');
  var poweredEl = page.querySelector('[data-conference-powered]');
  var backupWrap = page.querySelector('[data-conference-backup-wrap]');
  var backupEl = page.querySelector('[data-conference-backup]');
  var roomSection = page.querySelector('[data-conference-room]');
  var embedEl = page.querySelector('[data-conference-embed]');
  var roomStatus = page.querySelector('[data-conference-room-status]');
  var roomOpenLink = page.querySelector('[data-conference-room-open]');
  var leaveButton = page.querySelector('[data-conference-leave]');
  var form = page.querySelector('[data-conference-form]');
  var submitButton = form ? form.querySelector('button[type="submit"]') : null;
  var formStatus = page.querySelector('[data-conference-form-status]');

  var currentMeeting = null;
  var jitsiApi = null;
  var jitsiScriptPromise = null;
  var formEnabled = false;

  function setStatus(label, kind) {
    if (!statusEl) return;
    statusEl.textContent = label;
    statusEl.className = 'rpai-conference-status';
    if (kind) statusEl.className += ' is-' + kind;
  }

  function setFormStatus(message, kind) {
    if (!formStatus) return;
    formStatus.textContent = message || '';
    formStatus.className = 'rpai-form-status';
    if (kind === 'error') formStatus.className += ' is-error';
    if (kind === 'success') formStatus.className += ' is-success';
  }

  function setRoomStatus(message, kind) {
    if (!roomStatus) return;
    roomStatus.textContent = message || '';
    roomStatus.className = 'rpai-conference-room-status';
    if (kind === 'error') roomStatus.className += ' is-error';
    if (kind === 'success') roomStatus.className += ' is-success';
  }

  function setFormEnabled(enabled) {
    formEnabled = enabled;
    if (!form) return;
    Array.prototype.forEach.call(
      form.querySelectorAll('input, select, textarea, button'),
      function (control) {
        control.disabled = !enabled;
      }
    );
  }

  function safeHttpUrl(value) {
    if (!value || typeof value !== 'string') return null;
    try {
      var url = new URL(value, window.location.href);
      if (url.protocol !== 'https:' && url.protocol !== 'http:') return null;
      return url.href;
    } catch (error) {
      return null;
    }
  }

  function applyJoinLink(data) {
    if (!joinEl) return;

    currentMeeting = data;
    var jitsiUrl = safeHttpUrl(data.jitsiUrl);
    var backupUrl = safeHttpUrl(data.joinUrl);

    if (jitsiUrl) {
      joinEl.href = jitsiUrl;
      joinEl.textContent = 'Join the meeting';
      joinEl.removeAttribute('aria-disabled');
      joinEl.classList.remove('is-disabled');
      joinEl.removeAttribute('target');
    } else if (backupUrl) {
      joinEl.href = backupUrl;
      joinEl.textContent = 'Join the meeting';
      joinEl.removeAttribute('aria-disabled');
      joinEl.classList.remove('is-disabled');
      joinEl.setAttribute('target', '_blank');
      joinEl.setAttribute('rel', 'noopener noreferrer');
    } else {
      joinEl.href = '#register';
      joinEl.textContent = 'Request the link';
      joinEl.setAttribute('aria-disabled', 'true');
      joinEl.classList.add('is-disabled');
      joinEl.removeAttribute('target');
    }

    if (backupWrap && backupEl) {
      var showBackup = Boolean(jitsiUrl && backupUrl);
      backupWrap.hidden = !showBackup;
      if (showBackup) backupEl.href = backupUrl;
    }

    if (poweredEl) {
      if (jitsiUrl) {
        poweredEl.textContent =
          'The room opens in your browser through Jitsi Meet — no account or app needed.';
      } else if (backupUrl) {
        poweredEl.textContent =
          'Opens the backup meeting link in a new tab.';
      } else {
        poweredEl.textContent = 'The meeting room is being prepared.';
      }
    }
  }

  function applyDialIn(data) {
    if (!dialInWrap) return;
    var number = (data.dialInNumber || '').trim();
    if (!number) {
      dialInWrap.hidden = true;
      return;
    }

    dialInWrap.hidden = false;
    if (phoneEl) {
      var dialable = number.replace(/[^\d+]/g, '');
      phoneEl.textContent = number;
      phoneEl.href = dialable ? 'tel:' + dialable : '#register';
    }
  }

  function applyAccessCode(data) {
    if (!codeWrap) return;
    var code = (data.accessCode || '').trim();
    codeWrap.hidden = !code;
    if (code && codeEl) codeEl.textContent = code;
  }

  function applyMeeting(data) {
    if (titleEl && data.title) titleEl.textContent = data.title;
    if (scheduleEl && data.schedule) scheduleEl.textContent = data.schedule;
    if (descriptionEl && data.description) {
      descriptionEl.textContent = data.description;
    }
    if (hostEl) {
      hostEl.textContent = data.hostName || 'Royal Priesthood Assemblies International';
    }

    applyJoinLink(data);
    applyDialIn(data);
    applyAccessCode(data);
    page.setAttribute('data-conference-state', 'live');

    if (data.registrationOpen) {
      setStatus('Registration open', 'open');
      setFormEnabled(true);
      setFormStatus(
        'Enter your email and the meeting room link will be sent to you automatically.'
      );
      return;
    }

    setFormEnabled(false);

    if (!data.meetingReady) {
      setStatus('Meeting room coming soon', 'closed');
      setFormStatus(
        'The pastor is preparing the meeting room. Please check back soon, or contact the church office.',
        'error'
      );
      return;
    }

    if (!data.emailConfigured) {
      setStatus('Registration opening soon', 'closed');
      setFormStatus(
        'Email delivery is being prepared. Please contact the church office for the room link.',
        'error'
      );
      return;
    }

    setStatus('Registration closed', 'closed');
    setFormStatus(
      'Registration is closed at the moment. Please contact the church office for the meeting room link.',
      'error'
    );
  }

  function showOffline() {
    currentMeeting = null;
    page.setAttribute('data-conference-state', 'offline');
    setStatus('Meeting details unavailable', 'error');
    setFormEnabled(false);
    setFormStatus(
      'We could not load the meeting details. Please check your connection, then refresh the page, or contact the church on WhatsApp.',
      'error'
    );
    if (backupWrap) backupWrap.hidden = true;
    if (roomSection) roomSection.hidden = true;
    if (poweredEl) {
      poweredEl.textContent = 'Meeting details are unavailable right now.';
    }
    if (joinEl) {
      joinEl.href = 'contact.html';
      joinEl.textContent = 'Contact the church';
      joinEl.classList.remove('is-disabled');
      joinEl.removeAttribute('aria-disabled');
    }
  }

  function loadMeeting() {
    if (typeof window.fetch !== 'function') {
      showOffline();
      return;
    }

    var controller = typeof window.AbortController === 'function'
      ? new window.AbortController()
      : null;
    var timer = window.setTimeout(function () {
      if (controller) controller.abort();
    }, TIMEOUT_MS);

    window
      .fetch(API + '/api/conference', {
        cache: 'no-store',
        headers: { Accept: 'application/json' },
        signal: controller ? controller.signal : undefined
      })
      .then(function (response) {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.json();
      })
      .then(function (data) {
        applyMeeting(data || {});
      })
      .catch(function (error) {
        if (window.console && typeof window.console.warn === 'function') {
          window.console.warn('[RPAI] Could not load the meeting details.', error);
        }
        showOffline();
      })
      .then(function () {
        window.clearTimeout(timer);
      });
  }

  function loadJitsiScript() {
    if (window.JitsiMeetExternalAPI) return Promise.resolve();
    if (jitsiScriptPromise) return jitsiScriptPromise;

    jitsiScriptPromise = new Promise(function (resolve, reject) {
      var script = document.createElement('script');
      script.src = 'https://' + JITSI_DOMAIN + '/external_api.js';
      script.async = true;
      script.onload = resolve;
      script.onerror = function () {
        jitsiScriptPromise = null;
        reject(new Error('The meeting room script could not load.'));
      };
      document.head.appendChild(script);
    });

    return jitsiScriptPromise;
  }

  function openMeetingRoom() {
    if (!currentMeeting) return;
    var jitsiUrl = safeHttpUrl(currentMeeting.jitsiUrl);
    if (!jitsiUrl) return;

    if (!roomSection || !embedEl) return;

    roomSection.hidden = false;
    if (roomOpenLink) roomOpenLink.href = jitsiUrl;
    setRoomStatus('Loading the meeting room...');
    if (typeof roomSection.scrollIntoView === 'function') {
      roomSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    loadJitsiScript()
      .then(function () {
        if (jitsiApi) return;

        var height = Math.max(520, Math.min(760, window.innerHeight - 160));
        jitsiApi = new window.JitsiMeetExternalAPI(JITSI_DOMAIN, {
          roomName: currentMeeting.jitsiRoom,
          parentNode: embedEl,
          width: '100%',
          height: height,
          configOverwrite: {
            prejoinPageEnabled: true,
            disableDeepLinking: true,
            startWithAudioMuted: false,
            startWithVideoMuted: false
          },
          interfaceConfigOverwrite: {
            DEFAULT_BACKGROUND: '#0b2240'
          }
        });
        setRoomStatus('');
      })
      .catch(function (error) {
        if (window.console && typeof window.console.warn === 'function') {
          window.console.warn('[RPAI] Could not open the meeting room.', error);
        }
        setRoomStatus(
          'The room could not load here. Use "open it in a new tab" below.',
          'error'
        );
      });
  }

  function leaveMeetingRoom() {
    if (jitsiApi && typeof jitsiApi.dispose === 'function') {
      jitsiApi.dispose();
    }
    jitsiApi = null;
    if (embedEl) embedEl.textContent = '';
    if (roomSection) roomSection.hidden = true;
    setRoomStatus('');
  }

  function submitRegistration(event) {
    event.preventDefault();
    if (!formEnabled || !form) return;
    if (!form.reportValidity()) return;

    var consent = form.querySelector('input[name="consent"]');
    if (consent && !consent.checked) {
      setFormStatus('Please agree to receive the meeting link by email.', 'error');
      consent.focus();
      return;
    }

    var payload = {
      name: (form.querySelector('input[name="name"]') || {}).value || '',
      email: (form.querySelector('input[name="email"]') || {}).value || '',
      consent: Boolean(consent && consent.checked),
      website: (form.querySelector('input[name="website"]') || {}).value || ''
    };

    var email = payload.email.trim();
    if (submitButton) {
      submitButton.disabled = true;
      submitButton.textContent = 'Sending...';
    }
    setFormStatus('Sending the meeting room link...');

    window
      .fetch(API + '/api/conference/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(payload)
      })
      .then(function (response) {
        return response
          .json()
          .catch(function () {
            return {};
          })
          .then(function (body) {
            if (!response.ok) {
              throw new Error(
                body.message || 'The request could not be completed. Please try again.'
              );
            }
            return body;
          });
      })
      .then(function () {
        form.reset();
        setFormStatus(
          'The room link is on its way to ' +
            email +
            '. Check your inbox and your spam folder. You can close this page.',
          'success'
        );
      })
      .catch(function (error) {
        setFormStatus(error.message, 'error');
      })
      .then(function () {
        if (submitButton) {
          submitButton.disabled = false;
          submitButton.textContent = 'Email me the link';
        }
      });
  }

  if (form) {
    form.addEventListener('submit', submitRegistration);
  }

  if (joinEl) {
    joinEl.addEventListener('click', function (event) {
      if (!currentMeeting || !safeHttpUrl(currentMeeting.jitsiUrl)) return;
      // Let Ctrl/Cmd/Shift-click and middle-click open the room in a new tab.
      if (
        event.metaKey ||
        event.ctrlKey ||
        event.shiftKey ||
        event.altKey ||
        event.button !== 0
      ) {
        return;
      }
      event.preventDefault();
      openMeetingRoom();
    });
  }

  if (leaveButton) {
    leaveButton.addEventListener('click', leaveMeetingRoom);
  }

  setFormEnabled(false);
  setStatus('Loading meeting details', 'loading');
  setFormStatus('Please wait while the meeting details load.');

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadMeeting);
  } else {
    loadMeeting();
  }
})();
