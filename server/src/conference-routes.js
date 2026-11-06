import { Router } from 'express';

import {
  getConferenceSettings,
  upsertConferenceRegistration,
  markRegistrationEmail,
  setRegistrationStatus,
} from './conference-store.js';
import { conferenceRegisterSchema, isHttpsUrl, jitsiRoomUrl, meetingReady } from './conference-validation.js';
import { mailStatus, sendConferenceLinkEmail } from './mailer.js';

const router = Router();

/* A small, in-process limiter. The global /api limiter already caps a single
   address at 20 requests a minute; this one is deliberately tighter because
   each accepted request may send an email. */
const WINDOW_MS = 10 * 60 * 1000;
const MAX_REQUESTS = 5;
const recent = new Map();

function allowRegistration(req) {
  const key = req.ip || 'unknown';
  const now = Date.now();
  const entry = recent.get(key);

  if (!entry || now - entry.start > WINDOW_MS) {
    recent.set(key, { start: now, count: 1 });
    cleanup();
    return { ok: true, retryAfter: 0 };
  }

  if (entry.count >= MAX_REQUESTS) {
    return {
      ok: false,
      retryAfter: Math.ceil((WINDOW_MS - (now - entry.start)) / 1000),
    };
  }

  entry.count += 1;
  return { ok: true, retryAfter: 0 };
}

function cleanup() {
  if (recent.size < 500) return;
  const now = Date.now();
  for (const [key, entry] of recent) {
    if (now - entry.start > WINDOW_MS) recent.delete(key);
  }
}

function publicSettings(settings) {
  const mail = mailStatus();
  const jitsiUrl = jitsiRoomUrl(settings.jitsiRoom);
  const backupUrl = isHttpsUrl(settings.joinUrl) ? settings.joinUrl : null;
  const ready = Boolean(jitsiUrl || backupUrl);

  return {
    title: settings.title,
    hostName: settings.hostName,
    schedule: settings.schedule,
    description: settings.description,
    jitsiRoom: settings.jitsiRoom || null,
    jitsiUrl,
    joinUrl: backupUrl,
    dialInNumber: settings.dialInNumber,
    accessCode: settings.accessCode,
    meetingReady: ready,
    emailConfigured: mail.configured,
    // The page treats registration as open when there is a room to join. If
    // email is not configured yet, the page shows the room link after the
    // visitor registers instead of sending it.
    registrationOpen:
      Boolean(settings.registrationOpen) && ready,
    updatedAt: settings.updatedAt,
  };
}

/* -----------------------------------------------------------------------
   GET /api/conference
   Everything a visitor needs to render the meeting card. No registrant
   information and no admin fields.
   ----------------------------------------------------------------------- */
router.get('/', async (_req, res) => {
  try {
    const settings = await getConferenceSettings();
    res.set('Cache-Control', 'public, max-age=30');
    return res.json(publicSettings(settings));
  } catch (err) {
    console.error('[conference] could not load settings:', err.message);
    return res.status(503).json({
      error: 'conference_unavailable',
      message:
        'The meeting details are temporarily unavailable. Please try again shortly.',
    });
  }
});

/* -----------------------------------------------------------------------
   POST /api/conference/register
   Emails the current join link to the address supplied. The response never
   reveals whether an address was already on the list.
   ----------------------------------------------------------------------- */
router.post('/register', async (req, res) => {
  try {
    const parsed = conferenceRegisterSchema.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({
        error: 'validation_failed',
        details: parsed.error.issues.map((issue) => ({
          field: issue.path.join('.'),
          message: issue.message,
        })),
      });
    }

    const input = parsed.data;

    // A hidden field that only a bot fills in. Pretend it worked so the bot
    // does not learn how to get past the check.
    if (input.website) {
      return res.status(202).json({
        ok: true,
        message: 'Check your inbox for the meeting link.',
      });
    }

    const limit = allowRegistration(req);
    if (!limit.ok) {
      res.set('Retry-After', String(limit.retryAfter));
      return res.status(429).json({
        error: 'too_many_requests',
        message:
          'Too many requests from this connection. Please wait a few minutes and try again.',
      });
    }

    const settings = await getConferenceSettings();

    if (!settings.registrationOpen) {
      return res.status(403).json({
        error: 'registration_closed',
        message:
          'Registration is closed at the moment. Please contact the church office for the meeting link.',
      });
    }

    if (!meetingReady(settings)) {
      return res.status(409).json({
        error: 'meeting_not_ready',
        message:
          'The meeting room has not been published yet. Please check back shortly.',
      });
    }

    const registration = await upsertConferenceRegistration({
      name: input.name,
      email: input.email,
    });

    const publicInfo = publicSettings(settings);
    const roomUrl = publicInfo.jitsiUrl || publicInfo.joinUrl;
    const mail = mailStatus();

    // No email provider yet: keep the registration and show the room link on
    // the page so the visitor can still join today.
    if (!mail.configured) {
      await markRegistrationEmail(registration.id, {
        status: 'pending',
        error: 'email_not_configured',
      });
      return res.json({
        ok: true,
        emailSent: false,
        joinUrl: roomUrl,
        message:
          'You are registered. Email delivery is not set up yet, so use the button below to join now.',
      });
    }

    // If the same person just asked, do not send the same email twice.
    if (registration.sentAt) {
      const sentAt = new Date(registration.sentAt).getTime();
      if (Number.isFinite(sentAt) && Date.now() - sentAt < 2 * 60 * 1000) {
        await setRegistrationStatus(registration.id, 'sent');
        return res.json({
          ok: true,
          emailSent: true,
          alreadySent: true,
          message:
            'That link was just sent. Check your inbox and your spam folder.',
        });
      }
    }

    try {
      await sendConferenceLinkEmail({
        to: input.email,
        name: input.name,
        settings,
      });
      await markRegistrationEmail(registration.id, { status: 'sent' });

      return res.json({
        ok: true,
        emailSent: true,
        message: 'Check your inbox for the meeting link.',
      });
    } catch (err) {
      console.error('[conference] could not send meeting link:', err.message);
      await markRegistrationEmail(registration.id, {
        status: 'failed',
        error: String(err.message || 'send failed').slice(0, 500),
      });
      return res.status(502).json({
        error: 'email_failed',
        message:
          'We could not send the email just now. Please try again in a few minutes, or contact the church office.',
      });
    }
  } catch (err) {
    console.error('[conference] registration failed:', err.message);
    return res.status(500).json({
      error: 'registration_failed',
      message:
        'The request could not be completed just now. Please try again shortly.',
    });
  }
});

export default router;
