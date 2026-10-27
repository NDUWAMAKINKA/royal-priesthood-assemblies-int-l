-- RPAI giving API schema for Supabase Postgres.
-- Apply with: npm run db:migrate
--
-- The Node API connects with the database owner (the Supabase pooler
-- connection string). Row level security is enabled so the browser-safe
-- Supabase anon/publishable key cannot read or write these tables directly.

create table if not exists public.payments (
  reference text primary key,
  method text not null check (method in ('mobile_money', 'bank_transfer')),
  provider text,
  email text,
  amount numeric(14, 2) not null check (amount > 0),
  currency text not null default 'ZMW',
  status text not null default 'pending',
  authorization_url text,
  provider_reference text,
  paid_at timestamptz,
  channel text,
  provider_response jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists payments_status_idx
  on public.payments (status);
create index if not exists payments_created_at_idx
  on public.payments (created_at desc);
create index if not exists payments_email_idx
  on public.payments (email);

create table if not exists public.idempotency_keys (
  key text primary key,
  response jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  expires_at timestamptz not null
);

create index if not exists idempotency_keys_expires_at_idx
  on public.idempotency_keys (expires_at);

create table if not exists public.webhook_events (
  id bigserial primary key,
  provider text not null default 'paystack',
  event_id text,
  event_type text,
  reference text,
  payload_hash text not null,
  payload jsonb not null,
  signature_valid boolean not null default false,
  received_at timestamptz not null default now(),
  processed_at timestamptz,
  status text not null default 'received',
  unique (provider, payload_hash)
);

create index if not exists webhook_events_reference_idx
  on public.webhook_events (reference);

create or replace function public.rpai_set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists payments_set_updated_at on public.payments;
create trigger payments_set_updated_at
before update on public.payments
for each row execute function public.rpai_set_updated_at();

-- The API connects as the table owner and is unaffected by RLS. The
-- publishable/anon key used by a browser has no policy here, so it cannot
-- read donation records or idempotency responses.
alter table public.payments enable row level security;
alter table public.idempotency_keys enable row level security;
alter table public.webhook_events enable row level security;

comment on table public.payments is
  'Payment attempts and their current provider state.';
comment on table public.idempotency_keys is
  'Short-lived request replay protection for POST /api/charge.';
comment on table public.webhook_events is
  'Audit copy of signed Paystack webhooks, deduplicated by payload hash.';
