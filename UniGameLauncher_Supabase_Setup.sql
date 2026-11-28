-- UniGame Launcher v1.2 online schema
-- Run this entire script in Supabase Dashboard > SQL Editor.
-- Uses only the client publishable key + authenticated user JWTs.

create extension if not exists pgcrypto;

create table if not exists public.profiles (
    id uuid primary key references auth.users(id) on delete cascade,
    username text not null unique check (char_length(username) between 3 and 24),
    display_name text not null default '',
    bio text not null default '' check (char_length(bio) <= 280),
    avatar_url text not null default '',
    banner_url text not null default '',
    theme jsonb not null default '{"name":"Midnight"}'::jsonb,
    visibility text not null default 'public' check (visibility in ('public','friends','private')),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists public.friendships (
    id uuid primary key default gen_random_uuid(),
    requester_id uuid not null references auth.users(id) on delete cascade,
    addressee_id uuid not null references auth.users(id) on delete cascade,
    status text not null default 'pending' check (status in ('pending','accepted','rejected')),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    constraint friendships_not_self check (requester_id <> addressee_id),
    constraint friendships_unique_pair unique (requester_id, addressee_id)
);

create table if not exists public.game_stats (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id) on delete cascade,
    game_key text not null,
    game_title text not null,
    platform text not null default 'PC',
    play_seconds bigint not null default 0 check (play_seconds >= 0),
    launches bigint not null default 0 check (launches >= 0),
    last_played text,
    updated_at timestamptz not null default now(),
    constraint game_stats_unique_user_game unique (user_id, game_key)
);

create table if not exists public.user_presence (
    user_id uuid primary key references auth.users(id) on delete cascade,
    is_online boolean not null default false,
    last_seen timestamptz not null default now()
);

create unique index if not exists profiles_username_lower_unique on public.profiles (lower(username));
create index if not exists friendships_requester_idx on public.friendships (requester_id);
create index if not exists friendships_addressee_idx on public.friendships (addressee_id);
create index if not exists game_stats_user_idx on public.game_stats (user_id);

alter table public.profiles enable row level security;
alter table public.friendships enable row level security;
alter table public.game_stats enable row level security;
alter table public.user_presence enable row level security;

-- Public profiles can be discovered by username. Private/friends-only profiles
-- are visible only to their owner or accepted friends.
drop policy if exists "Profiles are visible to owners public users and friends" on public.profiles;
create policy "Profiles are visible to owners public users and friends"
on public.profiles for select to authenticated
using (
    id = auth.uid()
    or visibility = 'public'
    or (
        visibility = 'friends' and exists (
            select 1 from public.friendships f
            where f.status = 'accepted'
              and ((f.requester_id = auth.uid() and f.addressee_id = profiles.id)
                or (f.addressee_id = auth.uid() and f.requester_id = profiles.id))
        )
    )
);

drop policy if exists "Users create their own profile" on public.profiles;
create policy "Users create their own profile"
on public.profiles for insert to authenticated
with check (id = auth.uid());

drop policy if exists "Users update their own profile" on public.profiles;
create policy "Users update their own profile"
on public.profiles for update to authenticated
using (id = auth.uid()) with check (id = auth.uid());

-- Only participants can read a request. Only the sender can create it.
drop policy if exists "Friend requests visible to participants" on public.friendships;
create policy "Friend requests visible to participants"
on public.friendships for select to authenticated
using (requester_id = auth.uid() or addressee_id = auth.uid());

drop policy if exists "Users send friend requests" on public.friendships;
create policy "Users send friend requests"
on public.friendships for insert to authenticated
with check (requester_id = auth.uid() and status = 'pending');

-- The recipient may accept/reject. The requester may cancel a pending request.
drop policy if exists "Recipients respond to friend requests" on public.friendships;
create policy "Recipients respond to friend requests"
on public.friendships for update to authenticated
using (addressee_id = auth.uid() and status = 'pending')
with check (addressee_id = auth.uid() and status in ('accepted','rejected'));

drop policy if exists "Users delete their own friend requests" on public.friendships;
create policy "Users delete their own friend requests"
on public.friendships for delete to authenticated
using (requester_id = auth.uid() or addressee_id = auth.uid());

-- Game stats are visible to the owner and accepted friends.
drop policy if exists "Game stats visible to owner and friends" on public.game_stats;
create policy "Game stats visible to owner and friends"
on public.game_stats for select to authenticated
using (
    user_id = auth.uid()
    or exists (
        select 1 from public.friendships f
        where f.status = 'accepted'
          and ((f.requester_id = auth.uid() and f.addressee_id = game_stats.user_id)
            or (f.addressee_id = auth.uid() and f.requester_id = game_stats.user_id))
    )
);

drop policy if exists "Users insert their own game stats" on public.game_stats;
create policy "Users insert their own game stats"
on public.game_stats for insert to authenticated
with check (user_id = auth.uid());

drop policy if exists "Users update their own game stats" on public.game_stats;
create policy "Users update their own game stats"
on public.game_stats for update to authenticated
using (user_id = auth.uid()) with check (user_id = auth.uid());

drop policy if exists "Users delete their own game stats" on public.game_stats;
create policy "Users delete their own game stats"
on public.game_stats for delete to authenticated
using (user_id = auth.uid());

-- Presence is visible to the owner and accepted friends.
drop policy if exists "Presence visible to owner and friends" on public.user_presence;
create policy "Presence visible to owner and friends"
on public.user_presence for select to authenticated
using (
    user_id = auth.uid()
    or exists (
        select 1 from public.friendships f
        where f.status = 'accepted'
          and ((f.requester_id = auth.uid() and f.addressee_id = user_presence.user_id)
            or (f.addressee_id = auth.uid() and f.requester_id = user_presence.user_id))
    )
);

drop policy if exists "Users manage their own presence" on public.user_presence;
create policy "Users manage their own presence"
on public.user_presence for all to authenticated
using (user_id = auth.uid())
with check (user_id = auth.uid());

-- Prevent participants from changing the identity of a friend request.
create or replace function public.guard_friendship_update()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
    if new.requester_id is distinct from old.requester_id
       or new.addressee_id is distinct from old.addressee_id then
        raise exception 'Friend request participants cannot be changed';
    end if;
    if old.status <> 'pending' or new.status not in ('accepted','rejected') then
        raise exception 'Only pending requests can be accepted or rejected';
    end if;
    return new;
end;
$$;

drop trigger if exists friendships_guard_update on public.friendships;
create trigger friendships_guard_update
before update on public.friendships
for each row execute function public.guard_friendship_update();

-- Lets a signed-in user delete only their own Auth account. Cascades remove
-- their profile, friend links, stats and presence rows.
create or replace function public.delete_my_account()
returns void
language plpgsql
security definer
set search_path = ''
as $$
begin
    delete from auth.users where id = auth.uid();
end;
$$;
revoke all on function public.delete_my_account() from public;
grant execute on function public.delete_my_account() to authenticated;

-- Enable Realtime for presence and friend request updates if not already added.
do $$
begin
    if not exists (
        select 1 from pg_publication_tables
        where pubname = 'supabase_realtime'
          and schemaname = 'public'
          and tablename = 'user_presence'
    ) then
        alter publication supabase_realtime add table public.user_presence;
    end if;
    if not exists (
        select 1 from pg_publication_tables
        where pubname = 'supabase_realtime'
          and schemaname = 'public'
          and tablename = 'friendships'
    ) then
        alter publication supabase_realtime add table public.friendships;
    end if;
end $$;
