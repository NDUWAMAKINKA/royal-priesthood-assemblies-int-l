import { query } from './db.js';

/**
 * Persistence for the online meeting.
 *
 * All access to the two conference tables lives here, so the route modules
 * stay readable and no SQL is assembled from request field names.
 */

function mapSettings(row) {
  if (!row) {
    return {
      title: 'RPAI Online Meeting',
      hostName: 'Royal Priesthood Assemblies International',
      schedule: 'Sundays at 9:00 AM CAT',
      description: '',
      jitsiRoom: null,
      joinUrl: null,
      dialInNumber: null,
      accessCode: null,
      registrationOpen: true,
      updatedAt: null,
    };
  }

  return {
    title: row.title,
    hostName: row.host_name,
    schedule: row.schedule,
    description: row.description,
    jitsiRoom: row.jitsi_room || null,
    joinUrl: row.join_url,
    dialInNumber: row.dial_in_number,
    accessCode: row.access_code,
    registrationOpen: row.registration_open,
    updatedAt: row.updated_at ? new Date(row.updated_at).toISOString() : null,
  };
}

function mapRegistration(row) {
  if (!row) return null;
  return {
    id: Number(row.id),
    name: row.name || '',
    email: row.email,
    status: row.status,
    lastError: row.last_error || '',
    requestedAt: row.requested_at
      ? new Date(row.requested_at).toISOString()
      : null,
    sentAt: row.sent_at ? new Date(row.sent_at).toISOString() : null,
    createdAt: row.created_at ? new Date(row.created_at).toISOString() : null,
  };
}

export async function getConferenceSettings() {
  // The table is constrained to one row. A plain select without a where is
  // used because it keeps the row shape stable across database versions.
  const { rows } = await query(
    'select * from public.conference_settings limit 1'
  );
  return mapSettings(rows[0]);
}

export async function updateConferenceSettings(settings) {
  const { rows } = await query(
    `insert into public.conference_settings
       (id, title, host_name, schedule, description, jitsi_room, join_url,
        dial_in_number, access_code, registration_open)
     values (true, $1, $2, $3, $4, $5, $6, $7, $8, $9)
     on conflict (id) do update
       set title = excluded.title,
           host_name = excluded.host_name,
           schedule = excluded.schedule,
           description = excluded.description,
           jitsi_room = excluded.jitsi_room,
           join_url = excluded.join_url,
           dial_in_number = excluded.dial_in_number,
           access_code = excluded.access_code,
           registration_open = excluded.registration_open
     returning *`,
    [
      settings.title,
      settings.hostName || '',
      settings.schedule || '',
      settings.description || '',
      settings.jitsiRoom || null,
      settings.joinUrl || null,
      settings.dialInNumber || null,
      settings.accessCode || null,
      Boolean(settings.registrationOpen),
    ]
  );
  return mapSettings(rows[0]);
}

/**
 * One row per email. Registering again refreshes the request time but keeps
 * the original sent_at until the new email actually goes out, which lets the
 * route avoid sending the same link twice in a row.
 */
export async function upsertConferenceRegistration({ name, email }) {
  const { rows } = await query(
    `insert into public.conference_registrations (name, email, status)
     values ($1, $2, 'pending')
     on conflict (email) do update
       set name = excluded.name,
           status = 'pending',
           last_error = null,
           requested_at = now()
     returning *`,
    [name || null, email]
  );
  return mapRegistration(rows[0]);
}

export async function markRegistrationEmail(id, { status, error = null }) {
  const sentAt = status === 'sent' ? new Date().toISOString() : null;
  const { rows } = await query(
    `update public.conference_registrations
        set status = $2,
            last_error = $3,
            sent_at = coalesce($4, sent_at)
      where id = $1
      returning *`,
    [id, status, error, sentAt]
  );
  return mapRegistration(rows[0]);
}

/** Restore the status label without pretending a second email was sent. */
export async function setRegistrationStatus(id, status) {
  const { rows } = await query(
    `update public.conference_registrations
        set status = $2
      where id = $1
      returning *`,
    [id, status]
  );
  return mapRegistration(rows[0]);
}

export async function listConferenceRegistrations(limit = 500) {
  const safeLimit = Math.min(Math.max(Number(limit) || 500, 1), 1000);
  const { rows } = await query(
    `select * from public.conference_registrations
      order by requested_at desc
      limit $1`,
    [safeLimit]
  );
  return rows.map(mapRegistration);
}

export async function getConferenceRegistration(id) {
  const { rows } = await query(
    'select * from public.conference_registrations where id = $1',
    [id]
  );
  return mapRegistration(rows[0]);
}

export async function deleteConferenceRegistration(id) {
  const { rows } = await query(
    'delete from public.conference_registrations where id = $1 returning id',
    [id]
  );
  return Boolean(rows[0]);
}

export async function countConferenceRegistrations() {
  const { rows } = await query(
    'select count(*)::int as total from public.conference_registrations'
  );
  return rows[0]?.total ?? 0;
}
