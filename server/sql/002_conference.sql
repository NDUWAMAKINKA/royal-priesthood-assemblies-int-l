-- RPAI online meeting: settings the pastor can edit, and the people who
-- asked for the join link by email.
--
-- The website never talks to FreeConferenceCall.com. The pastor pastes the
-- meeting link into the admin page once; the API stores it here and emails it
-- to everyone who registers. That is what lets the pastor distribute the link
-- without sending it by hand.

create table if not exists public.conference_settings (
  id boolean primary key default true check (id),
  title text not null default 'RPAI Online Meeting',
  host_name text not null default 'Royal Priesthood Assemblies International',
  schedule text not null default 'Sundays at 9:00 AM CAT',
  description text not null default '',
  join_url text,
  dial_in_number text,
  access_code text,
  registration_open boolean not null default true,
  updated_at timestamptz not null default now()
);

-- Exactly one settings row. It is created here so the public page has something
-- sensible to read before the pastor has opened the admin screen.
insert into public.conference_settings (id)
values (true)
on conflict (id) do nothing;

drop trigger if exists conference_settings_set_updated_at on public.conference_settings;
create trigger conference_settings_set_updated_at
before update on public.conference_settings
for each row execute function public.rpai_set_updated_at();

create table if not exists public.conference_registrations (
  id bigserial primary key,
  name text,
  email text not null unique,
  status text not null default 'pending'
    check (status in ('pending', 'sent', 'failed')),
  last_error text,
  requested_at timestamptz not null default now(),
  sent_at timestamptz,
  created_at timestamptz not null default now()
);

create index if not exists conference_registrations_requested_at_idx
  on public.conference_registrations (requested_at desc);

-- Same rule as the payment tables: the API connects as the owner, while the
-- browser-safe Supabase key has no policy and therefore cannot read the list of
-- people who registered.
alter table public.conference_settings enable row level security;
alter table public.conference_registrations enable row level security;

comment on table public.conference_settings is
  'The current online meeting details, edited by the pastor through /admin.';
comment on table public.conference_registrations is
  'People who asked for the meeting link by email. Admin-only.';
