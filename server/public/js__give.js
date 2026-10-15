/**
 * Give-page payment controller.
 *
 * Talks ONLY to the giving API. The Paystack secret key never reaches this
 * file, and the browser must never hold one.
 */
(function () {
  'use strict';

  var API = window.RPAI_API_BASE || 'http://127.0.0.1:3000';
  var POLL_INTERVAL_MS = 3000;
  var POLL_TIMEOUT_MS = 5 * 60 * 1000;

  var form = document.querySelector('[data-give-form]');
  if (!form) return;

  var statusEl = document.querySelector('[data-give-status]');
  var loaderEl = document.querySelector('[data-give-loader]');
  var loaderText = document.querySelector('[data-give-loader-text]');
  var methodInputs = form.querySelectorAll('input[name="method"]');
  var mmFields = document.querySelector('[data-give-mm]');
  var bankCard = document.querySelector('[data-give-bank-card]');

  // --- provider shown only when Mobile Money is chosen ---------------------
  function syncMethod() {
    var method = form.querySelector('input[name="method"]:checked');
    var isMM = !method || method.value === 'mobile_money';
    if (mmFields) mmFields.hidden = !isMM;
    if (bankCard) bankCard.hidden = isMM;
    var phone = form.querySelector('#give-phone');
    var provider = form.querySelector('#give-provider');
    if (phone) phone.required = isMM;
    if (provider) provider.required = isMM;
  }

  methodInputs.forEach(function (input) {
    input.addEventListener('change', syncMethod);
  });
  syncMethod();

  // --- small helpers -------------------------------------------------------
  function setStatus(kind, message) {
    if (!statusEl) return;
    statusEl.className = 'rpai-give-status rpai-give-status-' + kind;
    statusEl.textContent = message;
    statusEl.hidden = false;
  }

  function setBusy(busy) {
    form.querySelectorAll('input, select, button').forEach(function (el) {
      el.disabled = busy;
    });
    if (loaderEl) loaderEl.hidden = !busy;
  }

  function showLoader(text) {
    if (loaderText) loaderText.textContent = text;
    setBusy(true);
  }

  function hideLoader() {
    setBusy(false);
  }

  function newIdempotencyKey() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return 'k-' + Date.now() + '-' + Math.random().toString(16).slice(2);
  }

  // --- polling -------------------------------------------------------------
  function stopPolling(timer) {
    if (timer) window.clearInterval(timer);
  }

  function pollUntilSettled(reference) {
    return new Promise(function (resolve) {
      var started = Date.now();
      var timer = window.setInterval(function () {
        if (Date.now() - started > POLL_TIMEOUT_MS) {
          stopPolling(timer);
          resolve({ status: 'timeout' });
          return;
        }
        fetch(API + '/api/payments/' + encodeURIComponent(reference))
          .then(function (r) { return r.ok ? r.json() : null; })
          .then(function (data) {
            if (!data) return;
            if (data.status === 'success') {
              stopPolling(timer);
              resolve(data);
            } else if (data.status === 'failed' || data.status === 'reversed') {
              stopPolling(timer);
              resolve(data);
            }
          })
          .catch(function () { /* keep polling until the deadline */ });
      }, POLL_INTERVAL_MS);
    });
  }

  // --- submit --------------------------------------------------------------
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    if (!form.reportValidity()) return;

    var data = Object.fromEntries(new FormData(form).entries());
    var method = data.method || 'mobile_money';

    var payload = {
      email: data.email,
      amount: Number(data.amount),
      currency: data.currency || 'ZMW',
      method: method,
    };

    if (method === 'mobile_money') {
      payload.mobile_money = {
        phone: data.phone,
        provider: data.provider,
      };
    }

    showLoader(
      method === 'mobile_money'
        ? 'Please check your mobile phone for a prompt to enter your Password/PIN to verify this transaction.'
        : 'Preparing your bank transfer details.'
    );
    setStatus('pending', 'Contacting your payment provider...');

    fetch(API + '/api/charge', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Idempotency-Key': newIdempotencyKey(),
      },
      body: JSON.stringify(payload),
    })
      .then(function (res) {
        return res.json().then(function (body) {
          return { ok: res.ok, body: body };
        });
      })
      .then(function (result) {
        if (!result.ok) {
          hideLoader();
          setStatus('error', result.body.message || 'The payment could not be started.');
          return;
        }

        var data2 = result.body;

        // Bank transfer fallback: nothing is charged, just print the details.
        if (data2.method === 'bank_transfer') {
          hideLoader();
          setStatus('info', 'Bank transfer selected. Reference ' + data2.reference);
          renderBankDetails(data2.instructions, data2.reference);
          return;
        }

        /**
         * Paystack requires the customer to open the authorization URL to enter
         * their PIN. There is no silent push, so we open it in a new tab and
         * poll for the webhook to confirm.
         */
        setStatus('pending', 'Enter your PIN on the payment page, then return here.');
        if (data2.authorizationUrl) {
          window.open(data2.authorizationUrl, '_blank', 'noopener');
        }

        pollUntilSettled(data2.reference).then(function (result3) {
          hideLoader();
          if (result3.status === 'success') {
            setStatus('success', 'Thank you. Your giving of ' + result3.currency + ' ' + result3.amount + ' was received.');
          } else if (result3.status === 'timeout') {
            setStatus('info', 'Still waiting for confirmation. If you completed the PIN prompt, your gift will be recorded shortly. Reference ' + data2.reference);
          } else {
            setStatus('error', 'The payment was not completed. Reference ' + data2.reference);
          }
        });
      })
      .catch(function () {
        hideLoader();
        setStatus('error', 'Could not reach the giving service. Please try again shortly.');
      });
  });

  // --- bank transfer card ---------------------------------------------------
  function renderBankDetails(instructions, reference) {
    if (!bankCard) return;
    var fields = [
      ['Bank name', instructions.bank.name],
      ['Account name', instructions.bank.accountName],
      ['Account number', instructions.bank.accountNumber],
      ['SWIFT / BIC', instructions.bank.swift],
      ['Branch', instructions.bank.branch],
      ['Reference to quote', reference],
    ];
    bankCard.innerHTML =
      '<div class="rpai-bank-details">' +
      fields
        .map(function (f) {
          return '<div><dt>' + f[0] + '</dt><dd></dd></div>';
        })
        .join('') +
      '</div>' +
      '<p class="rpai-payment-hidden">' + instructions.warning + '</p>';

    var dds = bankCard.querySelectorAll('dd');
    fields.forEach(function (f, i) { dds[i].textContent = f[1]; });
    bankCard.hidden = false;
  }

  // Load the bank details up front so the fallback card is never empty.
  fetch(API + '/api/bank-transfer')
    .then(function (r) { return r.json(); })
    .then(function (data) {
      if (data && data.available) {
        var pre = document.querySelector('[data-give-bank-details]');
        if (pre) {
          pre.innerHTML =
            '<dl class="rpai-bank-details">' +
            [
              ['Bank name', data.bank.name],
              ['Account name', data.bank.accountName],
              ['Account number', data.bank.accountNumber],
              ['SWIFT / BIC', data.bank.swift],
            ]
              .map(function (f) { return '<div><dt>' + f[0] + '</dt><dd></dd></div>'; })
              .join('') +
            '</dl><p class="rpai-payment-hidden">' + data.warning + '</p>';
          var cells = pre.querySelectorAll('dd');
          [
            data.bank.name,
            data.bank.accountName,
            data.bank.accountNumber,
            data.bank.swift,
          ].forEach(function (v, i) { cells[i].textContent = v; });
        }
      }
    })
    .catch(function () { /* fallback card simply stays hidden */ });
})();