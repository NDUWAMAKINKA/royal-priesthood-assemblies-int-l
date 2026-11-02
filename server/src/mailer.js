import nodemailer from 'nodemailer';

import { config } from './config.js';
import { isHttpsUrl, jitsiRoomUrl, meetingUrl } from './conference-validation.js';

/**
 * Sends the meeting link. Two transports are supported:
 *
 *   RESEND_API_KEY  -> one HTTPS request to Resend (recommended on Render)
 *   SMTP_HOST       -> any mailbox, including Gmail with an app password
 *
 * Nothing here is exposed to a browser. When no transport is configured the
 * API reports it and refuses registrations, because collecting an address and
 * then failing to email it is worse than saying so up front.
 */

let transporter = null;

function smtpReady() {
  const smtp = config.mail.smtp;
  if (!smtp.host) return false;
  if (smtp.user || smtp.pass) return Boolean(smtp.user && smtp.pass);
  return true;
}

function mode() {
  if (config.mail.resendApiKey) return 'resend';
  if (smtpReady()) return 'smtp';
  return 'none';
}

export function mailStatus() {
  return {
    configured: mode() !== 'none',
    mode: mode(),
    from: config.mail.from,
  };
}

function getTransporter() {
  if (transporter) return transporter;

  const smtp = config.mail.smtp;
  const options = {
    host: smtp.host,
    port: smtp.port,
    secure: smtp.secure,
    connectionTimeout: 15_000,
    greetingTimeout: 15_000,
    socketTimeout: 20_000,
  };
  if (smtp.user || smtp.pass) {
    options.auth = { user: smtp.user, pass: smtp.pass };
  }

  transporter = nodemailer.createTransport(options);
  return transporter;
}

function escapeHtml(value) {
  return String(value == null ? '' : value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function safeSubject(value) {
  return String(value || '').replace(/[\r\n]+/g, ' ').trim();
}

function paragraphHtml(value) {
  return escapeHtml(value).replace(/\r?\n/g, '<br>');
}

function meetingLines(settings) {
  const lines = [];
  if (settings.schedule) lines.push(`When: ${settings.schedule}`);
  if (settings.hostName) lines.push(`Host: ${settings.hostName}`);
  if (settings.dialInNumber) lines.push(`Backup dial-in: ${settings.dialInNumber}`);
  if (settings.accessCode) lines.push(`Backup access code: ${settings.accessCode}`);
  return lines;
}

function linkLabel(settings) {
  return meetingUrl(settings) || 'The meeting room';
}

function roomDescription(settings) {
  return jitsiRoomUrl(settings.jitsiRoom)
    ? 'The room opens in your browser. No account or app is needed.'
    : 'Open the link on your phone or computer at the meeting time.';
}

function buildConferenceEmail({ name, settings }) {
  const greeting = name ? `Hello ${name},` : 'Hello,';
  const lines = meetingLines(settings);
  const paragraph = settings.description
    ? `\n${settings.description}\n`
    : '';

  const text = [
    greeting,
    '',
    `You asked for the link to join ${settings.title} with Royal Priesthood Assemblies International.`,
    '',
    `Join the meeting:\n${linkLabel(settings)}`,
    '',
    roomDescription(settings),
    '',
    ...lines,
    paragraph,
    'If you did not request this link, you can safely ignore this email.',
    '',
    'Royal Priesthood Assemblies International',
    'A place of love where everyone counts.',
    config.conference.publicSiteUrl,
  ]
    .filter((line) => line !== null && line !== undefined)
    .join('\n');

  const details = lines
    .map(
      (line) =>
        `<tr><td style="padding:6px 0;color:#59636e;font-size:14px;">${escapeHtml(
          line
        )}</td></tr>`
    )
    .join('');

  const description = settings.description
    ? `<p style="margin:18px 0 0;color:#3d4753;font-size:15px;line-height:1.7;">${paragraphHtml(
        settings.description
      )}</p>`
    : '';

  const html = `<!doctype html>
<html lang="en">
<body style="margin:0;padding:0;background:#f5f0e9;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f5f0e9;padding:24px 12px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;background:#ffffff;border-top:4px solid #d4af37;font-family:Arial,Helvetica,sans-serif;">
          <tr>
            <td style="padding:30px 32px 10px;">
              <p style="margin:0 0 8px;color:#806100;font-size:12px;font-weight:bold;letter-spacing:1.5px;text-transform:uppercase;">Royal Priesthood Assemblies International</p>
              <h1 style="margin:0;color:#0b2240;font-family:Georgia,'Times New Roman',serif;font-size:26px;line-height:1.25;">${escapeHtml(
                settings.title
              )}</h1>
              <p style="margin:14px 0 0;color:#3d4753;font-size:16px;line-height:1.6;">${escapeHtml(
                greeting
              )}<br>You asked for the link to join our online meeting. It is below.</p>
            </td>
          </tr>
          <tr>
            <td style="padding:18px 32px 0;">
              <a href="${escapeHtml(
                meetingUrl(settings)
              )}" style="display:inline-block;padding:15px 24px;background:#d4af37;color:#0b2240;font-size:16px;font-weight:bold;text-decoration:none;border-radius:4px;">Join the meeting</a>
              <p style="margin:12px 0 0;color:#59636e;font-size:13px;line-height:1.6;">${escapeHtml(
                roomDescription(settings)
              )}</p>
            </td>
          </tr>
          <tr>
            <td style="padding:8px 32px 0;word-break:break-all;">
              <p style="margin:10px 0 0;color:#59636e;font-size:13px;line-height:1.5;">${escapeHtml(
                linkLabel(settings)
              )}</p>
            </td>
          </tr>
          <tr>
            <td style="padding:16px 32px 0;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-top:1px solid #e3e0d8;">
                ${details}
              </table>
              ${description}
            </td>
          </tr>
          <tr>
            <td style="padding:24px 32px 30px;">
              <p style="margin:0;color:#59636e;font-size:13px;line-height:1.6;">If you did not request this link, you can safely ignore this email. For help, reply to this message or contact the church office.</p>
              <p style="margin:18px 0 0;color:#0b2240;font-size:14px;font-weight:bold;">Royal Priesthood Assemblies International</p>
              <p style="margin:4px 0 0;color:#806100;font-size:13px;">A place of love where everyone counts.</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>`;

  return {
    subject: safeSubject(`Your link to join ${settings.title}`),
    text,
    html,
  };
}

async function sendWithResend({ to, subject, text, html, replyTo }) {
  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${config.mail.resendApiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: config.mail.from,
      to: [to],
      subject,
      text,
      html,
      reply_to: replyTo,
    }),
    signal: AbortSignal.timeout(15_000),
  });

  if (!response.ok) {
    const detail = await response.text().catch(() => '');
    throw new Error(
      `Resend refused the message (HTTP ${response.status})${
        detail ? `: ${detail.slice(0, 200)}` : ''
      }`
    );
  }

  const body = await response.json().catch(() => ({}));
  return body.id || 'resend';
}

export async function sendConferenceLinkEmail({ to, name, settings }) {
  const roomUrl = meetingUrl(settings);
  if (!roomUrl) {
    throw new Error('The meeting room has not been published yet');
  }

  if (!isHttpsUrl(roomUrl)) {
    throw new Error('The meeting room address is not a valid https:// address');
  }

  const message = buildConferenceEmail({ name, settings });
  const transport = mode();

  if (transport === 'resend') {
    return sendWithResend({
      to,
      ...message,
      replyTo: config.mail.replyTo,
    });
  }

  if (transport === 'smtp') {
    const info = await getTransporter().sendMail({
      from: config.mail.from,
      to,
      replyTo: config.mail.replyTo,
      ...message,
    });
    return info.messageId || 'smtp';
  }

  throw new Error('Email delivery is not configured on the server');
}

export async function sendTestEmail(to) {
  const transport = mode();
  if (transport === 'none') {
    throw new Error('Email delivery is not configured on the server');
  }

  const subject = safeSubject('RPAI email delivery test');
  const text = [
    'This is a test message from the Royal Priesthood Assemblies International website.',
    '',
    'If you received it, the online meeting registration emails will work.',
    '',
    config.conference.publicSiteUrl,
  ].join('\n');
  const html = `<p>This is a test message from the Royal Priesthood Assemblies International website.</p><p>If you received it, the online meeting registration emails will work.</p><p><a href="${escapeHtml(
    config.conference.publicSiteUrl
  )}">${escapeHtml(config.conference.publicSiteUrl)}</a></p>`;

  if (transport === 'resend') {
    return sendWithResend({ to, subject, text, html, replyTo: config.mail.replyTo });
  }

  const info = await getTransporter().sendMail({
    from: config.mail.from,
    to,
    replyTo: config.mail.replyTo,
    subject,
    text,
    html,
  });
  return info.messageId || 'smtp';
}
