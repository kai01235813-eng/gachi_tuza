-- =========================================================
-- 같이투자 (Gachi Tuza) Supabase PostgreSQL Schema & Security Policies
-- =========================================================

-- Enable UUID Extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. USERS TABLE (Linked to Supabase Auth)
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    nickname TEXT NOT NULL,
    provider TEXT NOT NULL DEFAULT 'kakao', -- 'kakao', 'naver', 'google'
    avatar_url TEXT,
    level INT DEFAULT 3,
    xp INT DEFAULT 1450,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. SQUADS TABLE (지인 모임/스쿼드)
CREATE TABLE IF NOT EXISTS public.squads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    created_by UUID REFERENCES public.users(id) ON DELETE CASCADE,
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

-- 4. TRADE JOURNALS TABLE (지인 공유 AI 복기 노트)
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

-- Sample Data Seeding
INSERT INTO public.users (id, email, nickname, provider, avatar_url, level, xp)
VALUES 
    ('11111111-1111-1111-1111-111111111111', 'gachi_leader@gachituza.com', '김가치 (스쿼드 리더)', 'kakao', 'https://api.dicebear.com/7.x/bottts/svg?seed=KimGachi', 4, 2450),
    ('22222222-2222-2222-2222-222222222222', 'park_bit@gachituza.com', '박비트 (가치투자자)', 'naver', 'https://api.dicebear.com/7.x/bottts/svg?seed=ParkBit', 3, 1980)
ON CONFLICT DO NOTHING;

INSERT INTO public.trade_journals (user_id, symbol, side, amount_krw, price, ai_reasoning, risk_review, lesson, likes_count)
VALUES 
    ('11111111-1111-1111-1111-111111111111', 'SAND', 'BUY', 10000, 49.4, '업비트 실질 매수가 49.4원으로 빗썸 대비 5.35% 저렴한 최저가 라우팅 확인. GitHub 개발 펀더멘털 점수 81점.', '거래소 입출금 중단 유의 공지 확인됨. 추가 매수 금지 수칙 준수.', '💡 소액 테스트 매수 완료. 유의 공지 해제 전까지 추가 매수를 금지하여 자산 보호.', 12),
    ('22222222-2222-2222-2222-222222222222', 'SOL', 'BUY', 50000, 245000, '김치 프리미엄 +2.21% 안정이격 구간. 개발 커밋 92점으로 극상급 펀더멘털.', '솔라나 메인넷 검증인 스테이킹(Staking) 연 6.5% 이자 중복 창출 시작.', '💎 현물 저점 매수 후 스테이킹 복리 이자 모으기 완수.', 19)
ON CONFLICT DO NOTHING;
