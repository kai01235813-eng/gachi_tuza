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
    title="같이투자 (Gachi Tuza) - 오픈소스 가치투자 소셜 플랫폼",
    description="지인들과 함께 공유하고 진짜 가치에 투자하는 100% 오픈소스 플랫폼",
    version="1.0.0"
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

# Seed initial DB data helper
def seed_initial_data(db: Session):
    if db.query(models.User).count() == 0:
        u1 = models.User(
            email="gachi_leader@gachituza.com",
            nickname="김가치 (스쿼드 리더)",
            provider="kakao",
            profile_img="https://api.dicebear.com/7.x/bottts/svg?seed=KimGachi",
            level=4,
            xp=2450
        )
        u2 = models.User(
            email="park_bit@gachituza.com",
            nickname="박비트 (가치투자자)",
            provider="naver",
            profile_img="https://api.dicebear.com/7.x/bottts/svg?seed=ParkBit",
            level=3,
            xp=1980
        )
        u3 = models.User(
            email="choi_sola@gachituza.com",
            nickname="최솔라 (스쿼드 멤버)",
            provider="google",
            profile_img="https://api.dicebear.com/7.x/bottts/svg?seed=ChoiSola",
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

# Root page
@app.get("/")
def read_root():
    root_html = os.path.join(os.path.dirname(__file__), "index.html")
    template_html = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(root_html):
        return FileResponse(root_html)
    elif os.path.exists(template_html):
        return FileResponse(template_html)
    return JSONResponse({"message": "같이투자 (Gachi Tuza) 백엔드가 정상 동작 중입니다."})

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
            level=3,
            xp=1500
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return auth_res

# 2. 지인 가치투자 복기 피드 API (DB 기반)
@app.get("/api/feed")
def get_social_feed(db: Session = Depends(get_db)):
    seed_initial_data(db)
    journals = db.query(models.TradeJournal).order_by(models.TradeJournal.id.desc()).all()
    results = []
    for j in journals:
        author_name = j.author.nickname if j.author else "익명 가치투자자"
        avatar = j.author.profile_img if j.author and j.author.profile_img else "https://api.dicebear.com/7.x/bottts/svg?seed=Gachi"
        results.append({
            "id": j.id,
            "author": author_name,
            "avatar": avatar,
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

# 3. 새로운 복기 노트 작성 API (DB 저장)
@app.post("/api/journal")
def create_journal(item: JournalCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).first()
    user_id = user.id if user else 1
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
    return {"status": "success", "id": new_j.id, "message": "새 복기 노트가 Supabase DB에 저장되었습니다."}

# 4. 스쿼드 랭킹전 API (DB 기반)
@app.get("/api/squad/rankings")
def get_squad_rankings(db: Session = Depends(get_db)):
    seed_initial_data(db)
    users = db.query(models.User).order_by(models.User.xp.desc()).all()
    rankings = []
    badges = ["💎 다이아몬드 핸드", "🛡️ FOMO 방어막", "⚖️ 최저가 라우터", "🚀 가치 탐색기"]
    for idx, u in enumerate(users):
        rankings.append({
            "rank": idx + 1,
            "name": u.nickname,
            "return_pct": round(14.8 - (idx * 3.6), 1),
            "badge": badges[idx % len(badges)],
            "xp": u.xp
        })
    return rankings

# 5. 정량 청산 데이터 API
@app.get("/api/liquidation/{symbol}")
def get_liquidation(symbol: str = "BTC"):
    return LiquidationHeatmapEngine.get_quantitative_analysis(symbol)

# 6. 삼각 차익거래 & 빗썸 스캐너 API
@app.get("/api/triangular")
def get_triangular():
    return TriangularArbitrageEngine.calculate_triangular_arbitrage()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
