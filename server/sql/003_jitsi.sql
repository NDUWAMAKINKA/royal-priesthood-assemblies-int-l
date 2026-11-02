-- Jitsi is the main meeting room. FreeConferenceCall stays as an optional
-- backup link for large or long services.
--
-- The column default gives the existing settings row a starting room the first
-- time this migration runs. If the pastor later clears the room to use only the
-- backup link, rerunning the migration does not put it back.

alter table public.conference_settings
  add column if not exists jitsi_room text
  default ('RPAI-Online-' || upper(substr(md5(random()::text), 1, 8)));

-- Make sure the single settings row exists even if it was removed by hand.
insert into public.conference_settings (id)
values (true)
on conflict (id) do nothing;

comment on column public.conference_settings.jitsi_room is
  'Jitsi Meet room name used by the embedded meeting room.';
