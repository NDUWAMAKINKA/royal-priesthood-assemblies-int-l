import { z } from 'zod';

/**
 * Input shapes for the online-meeting endpoints.
 *
 * The public endpoint accepts only what a visitor may send. The admin schema
 * accepts the settings the pastor edits: a safe Jitsi room name and an optional
 * https:// backup link.
 */

const optionalText = (max) =>
  z
    .string()
    .trim()
    .max(max)
    .optional()
    .default('');

export const conferenceSettingsSchema = z.object({
  title: z
    .string()
    .trim()
    .min(1, 'Give the meeting a title')
    .max(120, 'Keep the title under 120 characters'),
  hostName: optionalText(120),
  schedule: optionalText(160),
  description: optionalText(2000),
  jitsiRoom: z
    .string()
    .trim()
    .max(80)
    .optional()
    .default('')
    .refine(
      (value) => !value || /^[A-Za-z0-9_-]{3,80}$/.test(value),
      'Use 3-80 letters, numbers, hyphens or underscores'
    ),
  joinUrl: z
    .string()
    .trim()
    .max(500)
    .optional()
    .default('')
    .refine(
      (value) => !value || /^https:\/\/[^\s]+$/i.test(value),
      'Paste the full https:// meeting link'
    ),
  dialInNumber: optionalText(40),
  accessCode: optionalText(40),
  registrationOpen: z.boolean().default(true),
});

export const conferenceRegisterSchema = z.object({
  name: optionalText(120),
  email: z
    .string()
    .trim()
    .email('Enter a valid email address')
    .max(254)
    .transform((value) => value.toLowerCase()),
  consent: z.boolean().refine((value) => value === true, {
    message: 'Please agree to receive the meeting link by email',
  }),
  // A hidden field. Real visitors never see it; bots usually fill it in.
  website: z.string().trim().max(200).optional().default(''),
});

export const adminLoginSchema = z.object({
  password: z.string().min(1, 'Enter the admin password').max(200),
});

export const testEmailSchema = z.object({
  email: z.string().trim().email('Enter a valid email address').max(254),
});

/** An empty optional field is stored as null, not an empty string. */
export function nullIfBlank(value) {
  const text = typeof value === 'string' ? value.trim() : '';
  return text ? text : null;
}

/** Jitsi room names are restricted to characters that are safe in a URL. */
export function jitsiRoomUrl(room) {
  const name = typeof room === 'string' ? room.trim() : '';
  if (!/^[A-Za-z0-9_-]{3,80}$/.test(name)) return null;
  return `https://meet.jit.si/${encodeURIComponent(name)}`;
}

export function isHttpsUrl(value) {
  if (!value || typeof value !== 'string') return false;
  try {
    return new URL(value).protocol === 'https:';
  } catch {
    return false;
  }
}

/**
 * Jitsi is the room people are sent to. The FreeConferenceCall link is only a
 * fallback for large services or when the pastor has not set a Jitsi room.
 */
export function meetingUrl(settings) {
  const jitsi = jitsiRoomUrl(settings?.jitsiRoom);
  if (jitsi) return jitsi;
  return isHttpsUrl(settings?.joinUrl) ? settings.joinUrl : null;
}

export function meetingReady(settings) {
  return Boolean(meetingUrl(settings));
}
