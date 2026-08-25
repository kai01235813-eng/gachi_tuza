-- =========================================================
-- 같이투자 (Gachi Tuza) 3D Social Trading Game Supabase Schema
-- =========================================================

-- Enable UUID Extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. USERS TABLE (Linked to Supabase Auth & Gaming Profile)
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    nickname TEXT NOT NULL,
    provider TEXT NOT NULL DEFAULT 'kakao', -- 'kakao', 'naver', 'google'
    avatar_url TEXT,
    archetype TEXT DEFAULT '🛡️ 방어형 투자자',
    title TEXT DEFAULT '💎 가치 탐험가 Level 3',
    level INT DEFAULT 3,
    xp INT DEFAULT 1450,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. SQUADS TABLE (지인 스쿼드 & Co-op 레이드)
CREATE TABLE IF NOT EXISTS public.squads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    created_by UUID REFERENCES public.users(id) ON DELETE CASCADE,
    raid_title TEXT DEFAULT '🔥 비트코인 1억 구간 김프 스캘핑 보스 레이드',
    raid_goal NUMERIC DEFAULT 10000000.0,
    raid_progress NUMERIC DEFAULT 7450000.0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. SQUAD MEMBERS TABLE
CREATE TABLE IF NOT EXISTS public.squad_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    squad_id UUID REFERENCES public.squads(id) ON DELETE CASCADE,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(squad_id, user_id)
);

-- 4. TRADE JOURNALS TABLE (지인 공유 AI 복기 노트 / 스킬 캐스팅)
CREATE TABLE IF NOT EXISTS public.trade_journals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    symbol TEXT NOT NULL,
    side TEXT NOT NULL, -- 'BUY' or 'SELL'
    amount_krw NUMERIC NOT NULL,
    price NUMERIC NOT NULL,
    ai_reasoning TEXT NOT NULL,
    risk_review TEXT,
    lesson TEXT,
    likes_count INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. PORTFOLIOS TABLE (Read-Only API Sync)
CREATE TABLE IF NOT EXISTS public.portfolios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    symbol TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    avg_buy_price NUMERIC NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Row Level Security (RLS) Enable
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.squads ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.squad_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.trade_journals ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.portfolios ENABLE ROW LEVEL SECURITY;

-- Public Read Policies
CREATE POLICY "Allow Public Read Access on Trade Journals" ON public.trade_journals FOR SELECT USING (true);
CREATE POLICY "Allow Public Read Access on Users" ON public.users FOR SELECT USING (true);
CREATE POLICY "Allow Public Read Access on Squads" ON public.squads FOR SELECT USING (true);
