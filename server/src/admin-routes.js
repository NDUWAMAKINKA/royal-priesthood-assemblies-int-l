import { Router } from 'express';

import { config } from './config.js';
import {
  adminConfigured,
  issueAdminToken,
  passwordMatches,
  requireAdmin,
} from './admin-auth.js';
import {
  adminLoginSchema,
  conferenceSettingsSchema,
  meetingReady,
  nullIfBlank,
  testEmailSchema,
} from './conference-validation.js';
import {
  countConferenceRegistrations,
  deleteConferenceRegistration,
  getConferenceRegistration,
  getConferenceSettings,
  listConferenceRegistrations,
  markRegistrationEmail,
  updateConferenceSettings,
} from './conference-store.js';
import {
  mailStatus,
  sendConferenceLinkEmail,
  sendTestEmail,
} from './mailer.js';

const router = Router();

router.use((_req, res, next) => {
  res.set('Cache-Control', 'no-store');
  next();
});

/* Login is rate limited separately from the other admin calls. An attacker
   who finds the URL gets only a handful of guesses per quarter hour. */
const LOGIN_WINDOW_MS = 15 * 60 * 1000;
const LOGIN_MAX = 10;
const loginAttempts = new Map();

function loginKey(req) {
  return req.ip || 'unknown';
}

function loginAllowed(req) {
  const key = loginKey(req);
  const now = Date.now();
  const entry = loginAttempts.get(key);

  if (!entry || now - entry.start > LOGIN_WINDOW_MS) {
    loginAttempts.set(key, { start: now, count: 1 });
    if (loginAttempts.size > 500) {
      for (const [storedKey, stored] of loginAttempts) {
        if (now - stored.start > LOGIN_WINDOW_MS) loginAttempts.delete(storedKey);
      }
    }
    return { ok: true, retryAfter: 0 };
  }
  if (entry.count >= LOGIN_MAX) {
    return {
      ok: false,
      retryAfter: Math.ceil((LOGIN_WINDOW_MS - (now - entry.start)) / 1000),
    };
  }
  entry.count += 1;
  return { ok: true, retryAfter: 0 };
}

function publicPageUrl() {
  return `${String(config.conference.publicSiteUrl).replace(/\/+$/, '')}/video-conference.html`;
}

function registrationId(value) {
  const id = String(value || '');
  return /^\d+$/.test(id) ? id : null;
}

function adminState(settings, extra = {}) {
  return {
    settings,
    mail: mailStatus(),
    publicPageUrl: publicPageUrl(),
    ...extra,
  };
}

/* -----------------------------------------------------------------------
   POST /api/admin/login
   ----------------------------------------------------------------------- */
router.post('/login', (req, res) => {
  if (!adminConfigured()) {
    return res.status(503).json({
      error: 'admin_not_configured',
      message:
        'The admin page is not configured yet. Set CONFERENCE_ADMIN_PASSWORD on the server.',
    });
  }

  const limit = loginAllowed(req);
  if (!limit.ok) {
    res.set('Retry-After', String(limit.retryAfter));
    return res.status(429).json({
      error: 'too_many_attempts',
      message: 'Too many attempts. Please wait a few minutes and try again.',
    });
  }

  const parsed = adminLoginSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({
      error: 'validation_failed',
      message: 'Enter the admin password.',
    });
  }

  if (!passwordMatches(parsed.data.password)) {
    return res.status(401).json({
      error: 'invalid_password',
      message: 'That password is not correct.',
    });
  }

  loginAttempts.delete(loginKey(req));
  return res.json(issueAdminToken());
});

/* -----------------------------------------------------------------------
   GET /api/admin/conference
   ----------------------------------------------------------------------- */
router.get('/conference', requireAdmin, async (_req, res, next) => {
  try {
    const settings = await getConferenceSettings();
    const count = await countConferenceRegistrations();
    return res.json(adminState(settings, { registrationsCount: count }));
  } catch (err) {
    return next(err);
  }
});

/* -----------------------------------------------------------------------
   PUT /api/admin/conference
   ----------------------------------------------------------------------- */
router.put('/conference', requireAdmin, async (req, res, next) => {
  try {
    const parsed = conferenceSettingsSchema.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({
        error: 'validation_failed',
        details: parsed.error.issues.map((issue) => ({
          field: issue.path.join('.'),
          message: issue.message,
        })),
      });
    }

    const settings = await updateConferenceSettings({
      ...parsed.data,
      hostName: nullIfBlank(parsed.data.hostName) || '',
      schedule: nullIfBlank(parsed.data.schedule) || '',
      description: nullIfBlank(parsed.data.description) || '',
      joinUrl: nullIfBlank(parsed.data.joinUrl),
      jitsiRoom: nullIfBlank(parsed.data.jitsiRoom),
      dialInNumber: nullIfBlank(parsed.data.dialInNumber),
      accessCode: nullIfBlank(parsed.data.accessCode),
    });

    return res.json(
      adminState(settings, {
        registrationsCount: await countConferenceRegistrations(),
        message: 'Meeting details saved.',
      })
    );
  } catch (err) {
    return next(err);
  }
});

/* -----------------------------------------------------------------------
   GET /api/admin/registrations
   ----------------------------------------------------------------------- */
router.get('/registrations', requireAdmin, async (req, res, next) => {
  try {
    const items = await listConferenceRegistrations(req.query.limit);
    return res.json({ items, count: items.length });
  } catch (err) {
    return next(err);
  }
});

/* -----------------------------------------------------------------------
   POST /api/admin/registrations/:id/resend
   ----------------------------------------------------------------------- */
router.post(
  '/registrations/:id/resend',
  requireAdmin,
  async (req, res, next) => {
    try {
      const id = registrationId(req.params.id);
      if (!id) {
        return res.status(400).json({
          error: 'invalid_id',
          message: 'That registration id is not valid.',
        });
      }

      if (!mailStatus().configured) {
        return res.status(503).json({
          error: 'email_not_configured',
          message:
            'Email delivery is not configured. Add SMTP_* or RESEND_API_KEY first.',
        });
      }

      const registration = await getConferenceRegistration(id);
      if (!registration) {
        return res.status(404).json({
          error: 'not_found',
          message: 'That registration no longer exists.',
        });
      }

      const settings = await getConferenceSettings();
      if (!meetingReady(settings)) {
        return res.status(409).json({
          error: 'meeting_not_ready',
          message:
            'Add the Jitsi room or the backup meeting link before resending invitations.',
        });
      }

      try {
        await sendConferenceLinkEmail({
          to: registration.email,
          name: registration.name,
          settings,
        });
        const updated = await markRegistrationEmail(registration.id, {
          status: 'sent',
        });
        return res.json({
          ok: true,
          message: `Link sent to ${registration.email}.`,
          registration: updated,
        });
      } catch (err) {
        console.error('[admin] resend failed:', err.message);
        await markRegistrationEmail(registration.id, {
          status: 'failed',
          error: String(err.message || 'send failed').slice(0, 500),
        });
        return res.status(502).json({
          error: 'email_failed',
          message: `The email could not be sent: ${String(err.message || '').slice(
            0,
            200
          )}`,
        });
      }
    } catch (err) {
      return next(err);
    }
  }
);

/* -----------------------------------------------------------------------
   DELETE /api/admin/registrations/:id
   ----------------------------------------------------------------------- */
router.delete('/registrations/:id', requireAdmin, async (req, res, next) => {
  try {
    const id = registrationId(req.params.id);
    if (!id) {
      return res.status(400).json({
        error: 'invalid_id',
        message: 'That registration id is not valid.',
      });
    }

    const removed = await deleteConferenceRegistration(id);
    if (!removed) {
      return res.status(404).json({
        error: 'not_found',
        message: 'That registration no longer exists.',
      });
    }
    return res.json({ ok: true });
  } catch (err) {
    return next(err);
  }
});

/* -----------------------------------------------------------------------
   POST /api/admin/test-email
   ----------------------------------------------------------------------- */
router.post('/test-email', requireAdmin, async (req, res, next) => {
  try {
    if (!mailStatus().configured) {
      return res.status(503).json({
        error: 'email_not_configured',
        message:
          'Email delivery is not configured. Add SMTP_* or RESEND_API_KEY first.',
      });
    }

    const parsed = testEmailSchema.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({
        error: 'validation_failed',
        message: 'Enter a valid email address.',
      });
    }

    try {
      await sendTestEmail(parsed.data.email);
      return res.json({
        ok: true,
        message: `Test email sent to ${parsed.data.email}.`,
      });
    } catch (err) {
      console.error('[admin] test email failed:', err.message);
      return res.status(502).json({
        error: 'email_failed',
        message: `The test email could not be sent: ${String(
          err.message || ''
        ).slice(0, 200)}`,
      });
    }
  } catch (err) {
    return next(err);
  }
});

export default router;
