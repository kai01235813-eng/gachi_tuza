import os
import re
import random
import string
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, Base, get_db
import models
from auth.oauth import SocialOAuthHandler
from analyzers import (
    GitHubAnalyzer,
    KoreanPsychologyAnalyzer,
    ExchangeNoticeScanner,
    LiquidationHeatmapEngine,
    SmartTradingAssistantEngine,
    TriangularArbitrageEngine
)

# Auto-create tables in DB
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="같이투자 - 소셜 트레이딩 게임 플랫폼 (Zero UI)",
    description="간편 소셜 로그인, 모임 생성/참여, 주식/코인 투자군 선택, 투자 전략 수립, 트레이딩 손익률 기록 지원",
    version="5.0.0"
)

# Pydantic Schemas
class PromptRequest(BaseModel):
    user_id: Optional[int] = 1
    prompt: str

class ProfileUpdate(BaseModel):
    user_id: Optional[int] = 1
    nickname: str
    archetype: Optional[str] = "💎 기업 실질가치 투자자"
    title: Optional[str] = "💎 가치 탐험가 (3단계)"

class GroupCreateRequest(BaseModel):
    user_id: Optional[int] = 1
    group_name: str
    goal_krw: float

class GroupJoinRequest(BaseModel):
    user_id: Optional[int] = 1
    invite_code: str

class TradeJournalCreate(BaseModel):
    user_id: Optional[int] = 1
    asset_type: str = "🪙 코인"  # 📈 주식 or 🪙 코인
    symbol: str
    side: str  # BUY or SELL
    amount_krw: float
    price: float
    pnl_rate: Optional[float] = 0.0
    strategy: Optional[str] = "💎 가치분석 기반 분할매수 전략"
    ai_reasoning: str
    lesson: Optional[str] = ""

# Helper to generate random 6-char invite code
def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Seed initial DB data helper
def seed_initial_data(db: Session):
    if db.query(models.User).count() == 0:
        u1 = models.User(
            email="gachi_leader@gachituza.com",
            nickname="김가치 (모임장)",
            provider="kakao",
            profile_img="https://api.dicebear.com/7.x/bottts/svg?seed=KimGachi",
            archetype="💎 기업 실질가치 투자자",
            title="👑 가치투자 1기 모임장 (4단계)",
            level=4,
            xp=2450
        )
        u2 = models.User(
            email="park_bit@gachituza.com",
            nickname="박비트 (가치투자가)",
            provider="naver",
            profile_img="https://api.dicebear.com/7.x/bottts/svg?seed=ParkBit",
            archetype="🛡️ 위험 방어 수호자",
            title="🛡️ 장기 현물 투자 대가 (3단계)",
            level=3,
            xp=1980
        )
        db.add_all([u1, u2])
        db.commit()

        j1 = models.TradeJournal(
            user_id=u1.id,
            asset_type="📈 주식",
            symbol="삼성전자",
            side="BUY",
            amount_krw=1000000,
            price=72000,
            pnl_rate=8.5,
            strategy="💎 실적 개선 펀더멘털 저점 매수 전략",
            ai_reasoning="영업이익 반등 기대감 및 외국인 순매수 지속 수급 분석 완료.",
            lesson="💡 반도체 업황 회복 기대감 반영 장기 매수 완수.",
            likes_count=12
        )
        j2 = models.TradeJournal(
            user_id=u2.id,
            asset_type="🪙 코인",
            symbol="BTC",
            side="BUY",
            amount_krw=500000,
            price=135000000,
            pnl_rate=12.4,
            strategy="⚡ 국내외 가격차이 김프 0.04% 스캘핑 전략",
            ai_reasoning="업비트 프리미엄 2.1% 회복 및 현물 ETF 유입세 확인.",
            lesson="💎 현물 저점 분할 매수 모으기 완료.",
            likes_count=19
        )
        db.add_all([j1, j2])
        db.commit()

        s1 = models.Squad(
            name="같이투자 1기 챔피언 모임",
            code="GACHI7",
            created_by=u1.id,
            raid_title="🚀 모임 공동 목표: 1,000만원 달성",
            raid_goal=10000000.0,
            raid_progress=7450000.0
        )
        db.add(s1)
        db.commit()

# Root page
@app.get("/")
def read_root():
    root_html = os.path.join(os.path.dirname(__file__), "index.html")
    template_html = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(root_html):
        return FileResponse(root_html)
    elif os.path.exists(template_html):
        return FileResponse(template_html)
    return JSONResponse({"message": "같이투자 소셜 트레이딩 게임 백엔드가 정상 동작 중입니다."})

# 1. 1초 소셜 로그인 API
@app.post("/api/auth/login/{provider}")
def social_login(provider: str, db: Session = Depends(get_db)):
    auth_res = SocialOAuthHandler.authenticate_social_user(provider)
    user = db.query(models.User).filter(models.User.email == auth_res["email"]).first()
    if not user:
        user = models.User(
            email=auth_res["email"],
            nickname=auth_res["nickname"],
            provider=auth_res["provider"],
            profile_img=auth_res["profile_img"],
            archetype="💎 기업 실질가치 투자자",
            title="💎 가치 탐험가 (3단계)",
            level=3,
            xp=1500
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return {
        **auth_res,
        "id": user.id,
        "nickname": user.nickname,
        "archetype": user.archetype,
        "title": user.title,
        "xp": user.xp,
        "level": user.level
    }

# 2. 투자 그룹/모임 생성하기 API
@app.post("/api/squad/create")
def create_trading_group(req: GroupCreateRequest, db: Session = Depends(get_db)):
    seed_initial_data(db)
    code = generate_invite_code()
    new_squad = models.Squad(
        name=req.group_name,
        code=code,
        created_by=req.user_id,
        raid_title=f"🚀 {req.group_name} 공동 목표",
        raid_goal=req.goal_krw,
        raid_progress=0.0
    )
    db.add(new_squad)
    db.commit()
    db.refresh(new_squad)
    return {
        "status": "success",
        "message": f"🎉 '{req.group_name}' 모임이 생성되었습니다! 초대 코드: [{code}]",
        "group": {
            "id": new_squad.id,
            "name": new_squad.name,
            "code": new_squad.code,
            "goal_krw": new_squad.raid_goal
        }
    }

# 3. 투자 그룹/모임 참여하기 API
@app.post("/api/squad/join")
def join_trading_group(req: GroupJoinRequest, db: Session = Depends(get_db)):
    seed_initial_data(db)
    code_upper = req.invite_code.strip().upper()
    squad = db.query(models.Squad).filter(models.Squad.code == code_upper).first()
    if not squad:
        raise HTTPException(status_code=404, detail="존재하지 않는 초대 코드입니다.")
    
    # Check existing membership
    existing = db.query(models.SquadMember).filter(
        models.SquadMember.squad_id == squad.id,
        models.SquadMember.user_id == req.user_id
    ).first()
    if not existing:
        member = models.SquadMember(squad_id=squad.id, user_id=req.user_id)
        db.add(member)
        db.commit()

    return {
        "status": "success",
        "message": f"🤝 '{squad.name}' 모임에 성공적으로 참여하셨습니다!",
        "squad_name": squad.name
    }

# 4. 트레이딩 기록 작성 API (주식/코인, 투자전략, 손익률 %)
@app.post("/api/journal")
def create_journal(item: TradeJournalCreate, db: Session = Depends(get_db)):
    seed_initial_data(db)
    user = db.query(models.User).filter(models.User.id == item.user_id).first()
    if not user:
        user = db.query(models.User).first()

    if user:
        user.xp += 150
        if user.xp >= 3000 and user.level < 5:
            user.level += 1
            user.title = "👑 대가급 가치투자가 (5단계)"
        db.commit()

    new_j = models.TradeJournal(
        user_id=user.id if user else 1,
        asset_type=item.asset_type,
        symbol=item.symbol.upper(),
        side=item.side.upper(),
        amount_krw=item.amount_krw,
        price=item.price,
        pnl_rate=item.pnl_rate or 0.0,
        strategy=item.strategy or "💎 가치분석 기반 분할매수 전략",
        ai_reasoning=item.ai_reasoning,
        lesson=item.lesson,
        likes_count=0
    )
    db.add(new_j)
    db.commit()
    db.refresh(new_j)

    return {
        "status": "success",
        "message": f"⚡ [{item.asset_type}] {item.symbol} 트레이딩 복기 작성 완료! +150 EXP 획득!",
        "new_xp": user.xp if user else 1600
    }

# 5. 대화형 제로 UI 프롬프트 처리 API (/api/chat)
@app.post("/api/chat")
def process_zero_ui_prompt(req: PromptRequest, db: Session = Depends(get_db)):
    seed_initial_data(db)
    prompt_text = req.prompt.strip()
    user = db.query(models.User).filter(models.User.id == req.user_id).first()
    if not user:
        user = db.query(models.User).first()

    is_buy = "매수" in prompt_text or "샀" in prompt_text
    is_sell = "매도" in prompt_text or "팔았" in prompt_text
    
    asset_type = "📈 주식" if ("주식" in prompt_text or "삼성" in prompt_text or "엔비디아" in prompt_text) else "🪙 코인"

    symbols = ["BTC", "ETH", "SOL", "SAND", "XRP", "삼성전자", "엔비디아", "TSMC"]
    found_symbol = "BTC"
    for s in symbols:
        if s.lower() in prompt_text.lower():
            found_symbol = s
            break

    if is_buy or is_sell:
        side = "BUY" if is_buy else "SELL"
        user.xp += 150
        db.commit()

        new_j = models.TradeJournal(
            user_id=user.id,
            asset_type=asset_type,
            symbol=found_symbol,
            side=side,
            amount_krw=100000.0,
            price=100000.0,
            pnl_rate=5.2,
            strategy="💎 대화형 입력 자동 전략 감지",
            ai_reasoning=f"자연어 입력 '{prompt_text}' 감지 및 AI 시세 분석 완료.",
            lesson=f"💡 {found_symbol} {side} 기록 완료.",
            likes_count=0
        )
        db.add(new_j)
        db.commit()

        return {
            "type": "trade_created",
            "reply": f"🌱 **{user.nickname}**님, [{asset_type}] '{found_symbol} {side}' 매매 복기가 성공적으로 기록되었습니다!\n✨ **+150 경험치(EXP)** 획득 (현재 {user.xp:,} EXP)",
            "new_xp": user.xp
        }

    if "순위" in prompt_text or "랭킹" in prompt_text:
        return {
            "type": "info",
            "reply": "🏆 **모임 실전 수익률 순위**:\n1위 👑 김가치 (+14.8%, 2,450 EXP)\n2위 💎 박비트 (+11.2%, 1,980 EXP)"
        }
    return {
        "type": "info",
        "reply": f"🌿 '{prompt_text}' 분석을 완료했습니다.\n💡 매매 기록은 **'오늘 삼성전자 10만원 매수했어'**처럼 자연스럽게 말해보세요!"
    }

# 6. 사용자 정보 조회 API
@app.get("/api/user/me")
def get_current_user(db: Session = Depends(get_db)):
    seed_initial_data(db)
    user = db.query(models.User).first()
    if user:
        return {
            "id": user.id,
            "nickname": user.nickname,
            "provider": user.provider,
            "profile_img": user.profile_img,
            "archetype": user.archetype or "💎 기업 실질가치 투자자",
            "title": user.title or "👑 가치투자 1기 모임장 (4단계)",
            "level": user.level,
            "xp": user.xp
        }
    return {}

# 7. 프로필 변경 API
@app.post("/api/user/profile")
def update_user_profile(profile: ProfileUpdate, db: Session = Depends(get_db)):
    seed_initial_data(db)
    user = db.query(models.User).filter(models.User.id == profile.user_id).first()
    if not user:
        user = db.query(models.User).first()
    if user:
        user.nickname = profile.nickname
        if profile.archetype:
            user.archetype = profile.archetype
        if profile.title:
            user.title = profile.title
        db.commit()
        return {"status": "success", "message": f"🎉 닉네임이 '{user.nickname}'(으)로 변경되어 DB에 저장되었습니다!"}
    raise HTTPException(status_code=404, detail="User not found")

# 8. 소셜 피드 조회 API
@app.get("/api/feed")
def get_social_feed(db: Session = Depends(get_db)):
    seed_initial_data(db)
    journals = db.query(models.TradeJournal).order_by(models.TradeJournal.id.desc()).all()
    results = []
    for j in journals:
        results.append({
            "id": j.id,
            "author": j.author.nickname if j.author else "익명 투자자",
            "avatar": j.author.profile_img if j.author and j.author.profile_img else "https://api.dicebear.com/7.x/bottts/svg?seed=Gachi",
            "archetype": j.author.archetype if j.author else "💎 기업 실질가치 투자자",
            "asset_type": j.asset_type or "🪙 코인",
            "symbol": j.symbol,
            "side": j.side,
            "amount_krw": j.amount_krw,
            "price": j.price,
            "pnl_rate": j.pnl_rate or 0.0,
            "strategy": j.strategy or "💎 가치분석 전략",
            "time": j.created_at.strftime("%Y-%m-%d %H:%M") if j.created_at else "방금 전",
            "ai_reasoning": j.ai_reasoning,
            "lesson": j.lesson or "",
            "likes": j.likes_count
        })
    return results

# 9. 모임 랭킹 API
@app.get("/api/squad/rankings")
def get_squad_rankings(db: Session = Depends(get_db)):
    seed_initial_data(db)
    users = db.query(models.User).order_by(models.User.xp.desc()).all()
    rankings = []
    for idx, u in enumerate(users):
        rankings.append({
            "rank": idx + 1,
            "name": u.nickname,
            "archetype": u.archetype or "💎 기업 실질가치 투자자",
            "return_pct": round(14.8 - (idx * 3.6), 1),
            "xp": u.xp
        })
    return rankings

# 10. 스쿼드/모임 정보 API
@app.get("/api/squad/raids")
def get_squad_raids(db: Session = Depends(get_db)):
    seed_initial_data(db)
    squad = db.query(models.Squad).first()
    return {
        "squad_name": squad.name if squad else "같이투자 1기 모임",
        "invite_code": squad.code if squad else "GACHI7",
        "raid_title": squad.raid_title if squad else "🚀 모임 공동 목표: 1,000만원 가치투자 달성",
        "raid_goal_krw": squad.raid_goal if squad else 10000000.0,
        "raid_progress_krw": squad.raid_progress if squad else 7450000.0,
        "progress_pct": round(((squad.raid_progress / squad.raid_goal) * 100) if squad else 74.5, 1)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
