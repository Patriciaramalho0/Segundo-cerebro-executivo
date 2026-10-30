-- Execute este script no SQL Editor do seu projeto Supabase.
-- O teste gratuito começa no primeiro acesso autenticado.
create extension if not exists pgcrypto;

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text,
  display_name text,
  trial_started_at timestamptz not null default now(),
  trial_ends_at timestamptz not null default (now() + interval '7 days'),
  trial_requests_used integer not null default 0 check (trial_requests_used >= 0),
  created_at timestamptz not null default now()
);

create table if not exists public.user_workspaces (
  user_id uuid primary key references auth.users(id) on delete cascade,
  payload jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

create table if not exists public.ai_usage (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  model text not null,
  prompt_tokens integer not null default 0,
  completion_tokens integer not null default 0,
  total_tokens integer not null default 0,
  created_at timestamptz not null default now()
);

alter table public.profiles enable row level security;
alter table public.user_workspaces enable row level security;
alter table public.ai_usage enable row level security;

drop policy if exists "profile owner can read own profile" on public.profiles;
create policy "profile owner can read own profile" on public.profiles
for select to authenticated using (auth.uid() = id);

-- Não concedemos UPDATE/INSERT direto em profiles ao cliente:
-- evita que o próprio usuário estenda o teste ou altere seu contador.
-- O trigger e a função SECURITY DEFINER fazem as alterações necessárias.

drop policy if exists "workspace owner access" on public.user_workspaces;
create policy "workspace owner access" on public.user_workspaces
for all to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "user can read own ai usage" on public.ai_usage;
create policy "user can read own ai usage" on public.ai_usage
for select to authenticated using (auth.uid() = user_id);

drop policy if exists "user can insert own ai usage" on public.ai_usage;
create policy "user can insert own ai usage" on public.ai_usage
for insert to authenticated with check (auth.uid() = user_id);

-- Incremento atômico: duas requisições simultâneas não ultrapassam o limite.
create or replace function public.consume_trial_request(p_limit integer)
returns boolean
language plpgsql
security definer
set search_path = public
as $$
declare
  updated_count integer;
begin
  update public.profiles
  set trial_requests_used = trial_requests_used + 1
  where id = auth.uid()
    and trial_ends_at > now()
    and trial_requests_used < p_limit
  returning trial_requests_used into updated_count;

  return updated_count is not null;
end;
$$;

revoke all on function public.consume_trial_request(integer) from public;
grant execute on function public.consume_trial_request(integer) to authenticated;

-- Cria perfil automaticamente no cadastro. O período de teste começa no cadastro.
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (id, email, display_name)
  values (new.id, new.email, coalesce(new.raw_user_meta_data->>'display_name', ''));
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
after insert on auth.users
for each row execute procedure public.handle_new_user();
