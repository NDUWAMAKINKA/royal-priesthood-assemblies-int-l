(function () {
  'use strict';

  var TOKEN_KEY = 'rpai-conference-admin-token';
  var FALLBACK_PUBLIC_PAGE =
    'https://royal-priesthood-assemblies-int-l-1.onrender.com/video-conference.html';

  var state = {
    token: '',
    settings: null,
    mail: null,
    publicPageUrl: FALLBACK_PUBLIC_PAGE,
    registrations: []
  };

  function $(id) {
    return document.getElementById(id);
  }

  function setStatus(element, message, kind) {
    if (!element) return;
    element.textContent = message || '';
    element.className = 'form-status';
    if (kind === 'error') element.className += ' is-error';
    if (kind === 'success') element.className += ' is-success';
  }

  function setBusy(button, busy, busyLabel, normalLabel) {
    if (!button) return;
    if (busy) {
      button.dataset.normalLabel = normalLabel || button.textContent;
      button.textContent = busyLabel || 'Working...';
      button.disabled = true;
    } else {
      button.textContent = normalLabel || button.dataset.normalLabel || 'Save';
      button.disabled = false;
    }
  }

  function formatDate(value) {
    if (!value) return '—';
    var date = new Date(value);
    if (isNaN(date.getTime())) return value;
    try {
      return new Intl.DateTimeFormat(undefined, {
        dateStyle: 'medium',
        timeStyle: 'short'
      }).format(date);
    } catch (error) {
      return date.toISOString();
    }
  }

  function request(path, options) {
    options = options || {};
    var headers = options.headers || {};
    headers.Accept = 'application/json';
    if (options.body) headers['Content-Type'] = 'application/json';
    if (state.token) headers.Authorization = 'Bearer ' + state.token;

    return fetch('/api/admin' + path, {
      method: options.method || 'GET',
      headers: headers,
      body: options.body,
      cache: 'no-store'
    }).then(function (response) {
      return response
        .json()
        .catch(function () {
          return {};
        })
        .then(function (body) {
          if (response.status === 401) {
            signOut(true);
            throw new Error('Your session expired. Please sign in again.');
          }
          if (!response.ok) {
            var message =
              body.message ||
              (body.details && body.details[0] && body.details[0].message) ||
              'The request failed (' + response.status + ').';
            var error = new Error(message);
            error.status = response.status;
            throw error;
          }
          return body;
        });
    });
  }

  function showLogin() {
    $('login-view').hidden = false;
    $('app-view').hidden = true;
    $('logout-button').hidden = true;
    $('login-password').value = '';
  }

  function showApp() {
    $('login-view').hidden = true;
    $('app-view').hidden = false;
    $('logout-button').hidden = false;
  }

  function signOut(expired) {
    state.token = '';
    state.settings = null;
    state.mail = null;
    state.registrations = [];
    try {
      window.sessionStorage.removeItem(TOKEN_KEY);
    } catch (error) {
      /* private mode */
    }
    showLogin();
    setStatus(
      $('login-status'),
      expired ? 'Your session expired. Please sign in again.' : '',
      expired ? 'error' : ''
    );
  }

  function publicPageUrl() {
    return state.publicPageUrl || FALLBACK_PUBLIC_PAGE;
  }

  function updatePublicLink() {
    var link = $('public-page-link');
    if (link) link.href = publicPageUrl();
  }

  function updateWarnings() {
    var warning = $('setup-warning');
    if (!warning || !state.settings) return;

    var messages = [];
    if (!state.mail || !state.mail.configured) {
      messages.push(
        'Email delivery is not configured. People can still register and will see the room link on the page, but they will not receive an email. Add RESEND_API_KEY or the SMTP_* values on Render to enable email.'
      );
    }
    if (!state.settings.jitsiRoom && !state.settings.joinUrl) {
      messages.push(
        'Add a Jitsi room name (or a backup meeting link) below, then save. Until then the public page cannot offer registration.'
      );
    }
    if (!state.settings.registrationOpen) {
      messages.push(
        'Registration is switched off. Tick "Allow people to request the link by email" and save to open it.'
      );
    }

    warning.hidden = messages.length === 0;
    warning.textContent = messages.join(' ');
  }

  function fillMeeting(settings) {
    $('meeting-title').value = settings.title || '';
    $('meeting-host').value = settings.hostName || '';
    $('meeting-schedule').value = settings.schedule || '';
    $('meeting-jitsi-room').value = settings.jitsiRoom || '';
    $('meeting-join-url').value = settings.joinUrl || '';
    $('meeting-dial-in').value = settings.dialInNumber || '';
    $('meeting-access-code').value = settings.accessCode || '';
    $('meeting-description').value = settings.description || '';
    $('registration-open').checked = Boolean(settings.registrationOpen);
  }

  function generateJitsiRoom() {
    var suffix = '';
    try {
      var bytes = new Uint8Array(4);
      window.crypto.getRandomValues(bytes);
      suffix = Array.prototype.map
        .call(bytes, function (byte) {
          return ('0' + byte.toString(16)).slice(-2);
        })
        .join('')
        .toUpperCase();
    } catch (error) {
      suffix = Math.random().toString(16).slice(2, 10).toUpperCase();
    }
    $('meeting-jitsi-room').value = 'RPAI-Online-' + suffix;
    $('meeting-jitsi-room').focus();
  }

  function updateCount(count) {
    $('tab-count').textContent = String(count || 0);
    $('registrations-summary').textContent =
      count === 1
        ? '1 person has asked for the link. The link was emailed automatically.'
        : count + ' people have asked for the link. The links were emailed automatically.';
  }

  function statusBadge(registration) {
    var badge = document.createElement('span');
    badge.className = 'status-badge is-' + (registration.status || 'pending');
    badge.textContent = registration.status || 'pending';
    if (registration.status === 'failed' && registration.lastError) {
      badge.title = registration.lastError;
    }
    return badge;
  }

  function actionButton(label, action, id) {
    var button = document.createElement('button');
    button.type = 'button';
    button.textContent = label;
    button.dataset.action = action;
    button.dataset.id = String(id);
    return button;
  }

  function renderRegistrations(items) {
    var body = $('registrations-body');
    body.textContent = '';

    items.forEach(function (registration) {
      var row = document.createElement('tr');

      var requested = document.createElement('td');
      requested.textContent = formatDate(registration.requestedAt);
      row.appendChild(requested);

      var name = document.createElement('td');
      name.textContent = registration.name || '—';
      row.appendChild(name);

      var email = document.createElement('td');
      var emailLink = document.createElement('a');
      emailLink.href = 'mailto:' + registration.email;
      emailLink.textContent = registration.email;
      email.appendChild(emailLink);
      row.appendChild(email);

      var status = document.createElement('td');
      status.appendChild(statusBadge(registration));
      row.appendChild(status);

      var actions = document.createElement('td');
      var wrap = document.createElement('div');
      wrap.className = 'row-actions';
      wrap.appendChild(actionButton('Resend', 'resend', registration.id));
      wrap.appendChild(actionButton('Remove', 'delete', registration.id));
      actions.appendChild(wrap);
      row.appendChild(actions);

      body.appendChild(row);
    });

    $('registrations-empty').hidden = items.length > 0;
    updateCount(items.length);
  }

  function loadRegistrations() {
    setStatus($('registrations-status'), 'Loading...', '');
    return request('/registrations?limit=1000')
      .then(function (data) {
        state.registrations = data.items || [];
        renderRegistrations(state.registrations);
        setStatus($('registrations-status'), '', '');
      })
      .catch(function (error) {
        setStatus($('registrations-status'), error.message, 'error');
      });
  }

  function loadConference() {
    return request('/conference')
      .then(function (data) {
        state.settings = data.settings;
        state.mail = data.mail;
        state.publicPageUrl = data.publicPageUrl || FALLBACK_PUBLIC_PAGE;
        fillMeeting(data.settings);
        updatePublicLink();
        updateWarnings();
        updateCount(data.registrationsCount || 0);
        return loadRegistrations();
      })
      .catch(function (error) {
        if (error.status !== 401) {
          setStatus($('save-status'), error.message, 'error');
        }
      });
  }

  function saveMeeting(event) {
    event.preventDefault();
    var form = $('meeting-form');
    if (!form.reportValidity()) return;

    var payload = {
      title: $('meeting-title').value.trim(),
      hostName: $('meeting-host').value.trim(),
      schedule: $('meeting-schedule').value.trim(),
      jitsiRoom: $('meeting-jitsi-room').value.trim(),
      joinUrl: $('meeting-join-url').value.trim(),
      dialInNumber: $('meeting-dial-in').value.trim(),
      accessCode: $('meeting-access-code').value.trim(),
      description: $('meeting-description').value.trim(),
      registrationOpen: $('registration-open').checked
    };

    var button = $('save-button');
    setBusy(button, true, 'Saving...', 'Save meeting details');
    setStatus($('save-status'), '', '');

    request('/conference', {
      method: 'PUT',
      body: JSON.stringify(payload)
    })
      .then(function (data) {
        state.settings = data.settings;
        state.mail = data.mail;
        state.publicPageUrl = data.publicPageUrl || FALLBACK_PUBLIC_PAGE;
        fillMeeting(data.settings);
        updatePublicLink();
        updateWarnings();
        updateCount(data.registrationsCount || 0);
        setStatus($('save-status'), 'Saved. The public page now uses these details.', 'success');
      })
      .catch(function (error) {
        setStatus($('save-status'), error.message, 'error');
      })
      .then(function () {
        setBusy(button, false, '', 'Save meeting details');
      });
  }

  function resendRegistration(id) {
    var button = document.querySelector(
      '.row-actions button[data-action="resend"][data-id="' + id + '"]'
    );
    if (button) {
      button.disabled = true;
      button.textContent = 'Sending...';
    }
    setStatus($('registrations-status'), 'Sending the link...', '');

    request('/registrations/' + encodeURIComponent(id) + '/resend', {
      method: 'POST'
    })
      .then(function (data) {
        setStatus($('registrations-status'), data.message, 'success');
        return loadRegistrations();
      })
      .catch(function (error) {
        setStatus($('registrations-status'), error.message, 'error');
        if (button) {
          button.disabled = false;
          button.textContent = 'Resend';
        }
      });
  }

  function removeRegistration(id) {
    var registration = state.registrations.find(function (item) {
      return String(item.id) === String(id);
    });
    var label = registration ? registration.email : 'this registration';
    if (!window.confirm('Remove ' + label + ' from the list?')) return;

    setStatus($('registrations-status'), 'Removing...', '');
    request('/registrations/' + encodeURIComponent(id), { method: 'DELETE' })
      .then(function () {
        setStatus($('registrations-status'), 'Removed.', 'success');
        return loadRegistrations();
      })
      .catch(function (error) {
        setStatus($('registrations-status'), error.message, 'error');
      });
  }

  function csvCell(value) {
    var text = value == null ? '' : String(value);
    // Stop a submitted name or email from being treated as a spreadsheet
    // formula when the pastor opens the export in Excel.
    if (/^[=+\-@]/.test(text)) text = "'" + text;
    if (/[",\r\n]/.test(text)) {
      return '"' + text.replace(/"/g, '""') + '"';
    }
    return text;
  }

  function exportRegistrations() {
    if (!state.registrations.length) {
      setStatus($('registrations-status'), 'There is nothing to export yet.', 'error');
      return;
    }

    var rows = [
      ['Requested', 'Name', 'Email', 'Status', 'Sent at', 'Last error']
    ];
    state.registrations.forEach(function (item) {
      rows.push([
        formatDate(item.requestedAt),
        item.name || '',
        item.email,
        item.status,
        formatDate(item.sentAt),
        item.lastError || ''
      ]);
    });

    var csv = rows
      .map(function (row) {
        return row.map(csvCell).join(',');
      })
      .join('\r\n');

    var blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' });
    var url = URL.createObjectURL(blob);
    var link = document.createElement('a');
    link.href = url;
    link.download =
      'rpai-meeting-registrations-' +
      new Date().toISOString().slice(0, 10) +
      '.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    setStatus($('registrations-status'), 'CSV downloaded.', 'success');
  }

  function sendTestEmail(event) {
    event.preventDefault();
    var form = $('test-email-form');
    if (!form.reportValidity()) return;

    var button = $('test-email-button');
    setBusy(button, true, 'Sending...', 'Send test email');
    setStatus($('test-email-status'), '', '');

    request('/test-email', {
      method: 'POST',
      body: JSON.stringify({ email: $('test-email').value.trim() })
    })
      .then(function (data) {
        setStatus($('test-email-status'), data.message, 'success');
      })
      .catch(function (error) {
        setStatus($('test-email-status'), error.message, 'error');
      })
      .then(function () {
        setBusy(button, false, '', 'Send test email');
      });
  }

  function switchTab(name) {
    document.querySelectorAll('.tab').forEach(function (tab) {
      var active = tab.dataset.tab === name;
      tab.classList.toggle('is-active', active);
      tab.setAttribute('aria-selected', active ? 'true' : 'false');
    });
    ['meeting', 'registrations', 'help'].forEach(function (section) {
      $('tab-' + section).hidden = section !== name;
    });
    if (name === 'registrations') loadRegistrations();
  }

  function login(event) {
    event.preventDefault();
    var password = $('login-password').value;
    if (!password) {
      setStatus($('login-status'), 'Enter the admin password.', 'error');
      return;
    }

    var button = $('login-button');
    setBusy(button, true, 'Signing in...', 'Sign in');
    setStatus($('login-status'), '', '');

    fetch('/api/admin/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ password: password })
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
                body.message || 'Could not sign in (' + response.status + ').'
              );
            }
            return body;
          });
      })
      .then(function (body) {
        state.token = body.token;
        try {
          window.sessionStorage.setItem(TOKEN_KEY, body.token);
        } catch (error) {
          /* private mode */
        }
        $('login-password').value = '';
        showApp();
        return loadConference();
      })
      .catch(function (error) {
        setStatus($('login-status'), error.message, 'error');
      })
      .then(function () {
        setBusy(button, false, '', 'Sign in');
      });
  }

  function init() {
    try {
      state.token = window.sessionStorage.getItem(TOKEN_KEY) || '';
    } catch (error) {
      state.token = '';
    }

    $('login-form').addEventListener('submit', login);
    $('meeting-form').addEventListener('submit', saveMeeting);
    $('generate-jitsi-room').addEventListener('click', generateJitsiRoom);
    $('test-email-form').addEventListener('submit', sendTestEmail);
    $('logout-button').addEventListener('click', function () {
      signOut(false);
    });
    $('refresh-registrations').addEventListener('click', loadRegistrations);
    $('export-registrations').addEventListener('click', exportRegistrations);

    document.querySelectorAll('.tab').forEach(function (tab) {
      tab.addEventListener('click', function () {
        switchTab(tab.dataset.tab);
      });
    });

    $('registrations-body').addEventListener('click', function (event) {
      var button = event.target.closest('button[data-action]');
      if (!button) return;
      var id = button.dataset.id;
      if (button.dataset.action === 'resend') resendRegistration(id);
      if (button.dataset.action === 'delete') removeRegistration(id);
    });

    updatePublicLink();

    if (state.token) {
      showApp();
      loadConference();
    } else {
      showLogin();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
