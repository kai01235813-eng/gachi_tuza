import os
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

# Auto-create tables in DB (Supabase PostgreSQL / SQLite)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="같이투자 (Gachi Tuza) 3D 소셜 트레이딩 게임 플랫폼",
    description="지인들과 함께 3D 아레나에서 레이드하고 가치에 투자하는 100% 오픈소스 소셜 게임",
    version="2.0.0"
)

# Pydantic Schemas
class JournalCreate(BaseModel):
    user_id: Optional[int] = 1
    symbol: str
    side: str  # BUY or SELL
    amount_krw: float
    price: float
    ai_reasoning: str
    risk_review: Optional[str] = ""
    lesson: Optional[str] = ""

class ProfileUpdate(BaseModel):
    user_id: Optional[int] = 1
    nickname: str
    archetype: Optional[str] = "🛡️ 방어형 투자자"
    title: Optional[str] = "💎 가치 탐험가 Level 3"
    profile_img: Optional[str] = None

# Seed initial DB data helper
def seed_initial_data(db: Session):
    if db.query(models.User).count() == 0:
        u1 = models.User(
            email="gachi_leader@gachituza.com",
            nickname="김가치 (스쿼드 리더)",
            provider="kakao",
            profile_img="https://api.dicebear.com/7.x/bottts/svg?seed=KimGachi",
            archetype="💎 다이아몬드 홀더",
            title="⚔️ 가치투자 1기 스쿼드장 (Lv.4)",
            level=4,
            xp=2450
        )
        u2 = models.User(
            email="park_bit@gachituza.com",
            nickname="박비트 (가치투자자)",
            provider="naver",
            profile_img="https://api.dicebear.com/7.x/bottts/svg?seed=ParkBit",
            archetype="🛡️ FOMO 방어마스터",
            title="🛡️ 버핏급 펀더멘털 분석가 (Lv.3)",
            level=3,
            xp=1980
        )
        u3 = models.User(
            email="choi_sola@gachituza.com",
            nickname="최솔라 (스쿼드 멤버)",
            provider="google",
            profile_img="https://api.dicebear.com/7.x/bottts/svg?seed=ChoiSola",
            archetype="⚡ 스나이퍼 차익거래가",
            title="⚖️ 최저가 스캘퍼 (Lv.2)",
            level=2,
            xp=1620
        )
        db.add_all([u1, u2, u3])
        db.commit()

        j1 = models.TradeJournal(
            user_id=u1.id,
            symbol="SAND",
            side="BUY",
            amount_krw=10000,
            price=49.4,
            ai_reasoning="업비트 실질가 49.4원으로 빗썸 대비 5.35% 저렴한 최저가 라우팅 확인. GitHub 개발 펀더멘털 점수 81점.",
            risk_review="거래소 입출금 중단 유의 공지 확인됨. 추가 매수 금지 수칙 준수.",
            lesson="💡 소액 테스트 매수 완료. 유의 공지 해제 전까지 추가 매수를 금지하여 자산 보호.",
            likes_count=12
        )
        j2 = models.TradeJournal(
            user_id=u2.id,
            symbol="SOL",
            side="BUY",
            amount_krw=50000,
            price=245000,
            ai_reasoning="김치 프리미엄 +2.21% 안정이격 구간. 개발 커밋 92점으로 극상급 펀더멘털.",
            risk_review="솔라나 메인넷 검증인 스테이킹(Staking) 연 6.5% 이자 중복 창출 시작.",
            lesson="💎 현물 저점 매수 후 스테이킹 복리 이자 모으기 완수.",
            likes_count=19
        )
        db.add_all([j1, j2])
        db.commit()

        s1 = models.Squad(
            name="가치투자 1기 챔피언십 스쿼드",
            code="GACHI001",
            created_by=u1.id,
            raid_title="🔥 비트코인 1억 구간 김프 스캘핑 & 스테이킹 보스 레이드",
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
    return JSONResponse({"message": "같이투자 3D 트레이딩 게임 백엔드가 정상 동작 중입니다."})

# 1. 3대 1초 소셜 로그인 API
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
            archetype="🛡️ 방어형 투자자",
            title="💎 초보 가치탐험가 (Lv.3)",
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

# 2. 프로필 및 게이머 닉네임 변경 API (DB 저장)
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
        if profile.profile_img:
            user.profile_img = profile.profile_img
        db.commit()
        db.refresh(user)
        return {
            "status": "success",
            "message": f"🎉 게이머 닉네임이 '{user.nickname}'(으)로 변경되어 Supabase DB에 저장되었습니다!",
            "user": {
                "id": user.id,
                "nickname": user.nickname,
                "archetype": user.archetype,
                "title": user.title,
                "profile_img": user.profile_img,
                "xp": user.xp,
                "level": user.level
            }
        }
    raise HTTPException(status_code=404, detail="User not found")

# 3. 게이머 정보 조회 API
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
            "archetype": user.archetype or "🛡️ 방어형 투자자",
            "title": user.title or "💎 가치 탐험가 Level 3",
            "level": user.level,
            "xp": user.xp
        }
    return {}

# 4. 소셜 피드 & 복기 노트 API (DB 기반)
@app.get("/api/feed")
def get_social_feed(db: Session = Depends(get_db)):
    seed_initial_data(db)
    journals = db.query(models.TradeJournal).order_by(models.TradeJournal.id.desc()).all()
    results = []
    for j in journals:
        author_name = j.author.nickname if j.author else "익명 가치투자가"
        avatar = j.author.profile_img if j.author and j.author.profile_img else "https://api.dicebear.com/7.x/bottts/svg?seed=Gachi"
        archetype = j.author.archetype if j.author else "🛡️ 방어형 투자자"
        title = j.author.title if j.author else "가치 탐험가"
        results.append({
            "id": j.id,
            "author": author_name,
            "avatar": avatar,
            "archetype": archetype,
            "title": title,
            "symbol": j.symbol,
            "side": j.side,
            "amount_krw": j.amount_krw,
            "price": j.price,
            "time": j.created_at.strftime("%Y-%m-%d %H:%M") if j.created_at else "방금 전",
            "ai_reasoning": j.ai_reasoning,
            "risk_review": j.risk_review or "",
            "lesson": j.lesson or "",
            "likes": j.likes_count
        })
    return results

# 5. 새로운 복기 노트 작성 API (스킬 캐스팅 + XP 증동)
@app.post("/api/journal")
def create_journal(item: JournalCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).first()
    user_id = user.id if user else 1
    if user:
        user.xp += 150  # 획득 XP +150
        if user.xp >= 2000 and user.level < 5:
            user.level += 1
            user.title = "💎 마스터 가치투자 수호자 (Lv.5)"
        db.commit()

    new_j = models.TradeJournal(
        user_id=user_id,
        symbol=item.symbol.upper(),
        side=item.side.upper(),
        amount_krw=item.amount_krw,
        price=item.price,
        ai_reasoning=item.ai_reasoning,
        risk_review=item.risk_review,
        lesson=item.lesson,
        likes_count=0
    )
    db.add(new_j)
    db.commit()
    db.refresh(new_j)
    return {
        "status": "success",
        "id": new_j.id,
        "message": "⚡ 스킬 캐스팅 성공! 새 복기 노트가 Supabase DB에 저장되고 +150 EXP를 획득했습니다!",
        "new_xp": user.xp if user else 1600
    }

# 6. 스쿼드 랭킹전 API (DB 기반)
@app.get("/api/squad/rankings")
def get_squad_rankings(db: Session = Depends(get_db)):
    seed_initial_data(db)
    users = db.query(models.User).order_by(models.User.xp.desc()).all()
    rankings = []
    badges = ["💎 다이아몬드 핸드", "🛡️ FOMO 방어막", "⚖️ 최저가 라우터", "🚀 가치 스나이퍼"]
    for idx, u in enumerate(users):
        rankings.append({
            "rank": idx + 1,
            "name": u.nickname,
            "archetype": u.archetype or "🛡️ 방어형",
            "title": u.title or "가치 탐험가",
            "return_pct": round(14.8 - (idx * 3.6), 1),
            "badge": badges[idx % len(badges)],
            "xp": u.xp,
            "avatar": u.profile_img
        })
    return rankings

# 7. 공동 트레이딩 레이드 (Co-op Squad Raids) API
@app.get("/api/squad/raids")
def get_squad_raids(db: Session = Depends(get_db)):
    seed_initial_data(db)
    squad = db.query(models.Squad).first()
    return {
        "squad_name": squad.name if squad else "가치투자 1기 챔피언십 스쿼드",
        "raid_title": squad.raid_title if squad else "🔥 비트코인 1억 구간 김프 스캘핑 보스 레이드",
        "raid_goal_krw": squad.raid_goal if squad else 10000000.0,
        "raid_progress_krw": squad.raid_progress if squad else 7450000.0,
        "progress_pct": round(((squad.raid_progress / squad.raid_goal) * 100) if squad else 74.5, 1),
        "buff": "⚡ 스쿼드 전원 복기 작성 시 EXP 2배 버프 발동 중!",
        "participants": [
            {"name": "김가치", "contribution": "3,500,000원", "role": "🛡️ 탱크/리더"},
            {"name": "박비트", "contribution": "2,450,000원", "role": "💎 버프 딜러"},
            {"name": "최솔라", "contribution": "1,500,000원", "role": "⚡ 차익 스나이퍼"}
        ]
    }

# 8. 정량 청산 데이터 API
@app.get("/api/liquidation/{symbol}")
def get_liquidation(symbol: str = "BTC"):
    return LiquidationHeatmapEngine.get_quantitative_analysis(symbol)

# 9. 삼각 차익거래 & 빗썸 스캐너 API
@app.get("/api/triangular")
def get_triangular():
    return TriangularArbitrageEngine.calculate_triangular_arbitrage()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
