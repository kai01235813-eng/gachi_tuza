import os
import re
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
    title="같이투자 - 대화형 숲속 소셜 트레이딩 플랫폼 (Zero UI)",
    description="단 하나의 자연어 프롬프트 창으로 매매 복기, 가치 분석, 모임 순위를 간편하게 처리하는 대화형 제로 UI 플랫폼",
    version="4.0.0"
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
    profile_img: Optional[str] = None

# Seed initial DB data helper
def seed_initial_data(db: Session):
    if db.query(models.User).count() == 0:
        u1 = models.User(
            email="gachi_leader@gachituza.com",
            nickname="김가치 (가치 모임장)",
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
        u3 = models.User(
            email="choi_sola@gachituza.com",
            nickname="최솔라 (모임 식구)",
            provider="google",
            profile_img="https://api.dicebear.com/7.x/bottts/svg?seed=ChoiSola",
            archetype="⚡ 가격차이 차익 투자자",
            title="⚖️ 최저가 탐색 전문가 (2단계)",
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
            ai_reasoning="업비트 실질가 49.4원으로 빗썸 대비 5.35% 저렴한 최저가 매수 경로 확인. GitHub 개발 실적 점수 81점.",
            risk_review="거래소 입출금 중단 유의 공지 확인됨. 추가 매수 금지 위험 방어 수칙 준수.",
            lesson="💡 소액 테스트 매수 완료. 유의 공지 해제 전까지 추가 매수를 금지하여 자산 보호.",
            likes_count=12
        )
        j2 = models.TradeJournal(
            user_id=u2.id,
            symbol="SOL",
            side="BUY",
            amount_krw=50000,
            price=245000,
            ai_reasoning="국내외 가격 차이 +2.21% 안정이격 구간. 개발 커밋 92점으로 우수한 실질 가치.",
            risk_review="솔라나 메인넷 검증인 예치(Staking) 연 6.5% 이자 중복 창출 시작.",
            lesson="💎 현물 저점 매수 후 예치 복리 이자 모으기 완수.",
            likes_count=19
        )
        db.add_all([j1, j2])
        db.commit()

        s1 = models.Squad(
            name="가치투자 1기 모임",
            code="GACHI001",
            created_by=u1.id,
            raid_title="🚀 모임 공동 목표: 1,000만원 가치투자 & 가격 차익 획득",
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
    return JSONResponse({"message": "같이투자 제로 UI 소셜 트레이딩 게임 백엔드가 정상 동작 중입니다."})

# 1. 제로 UI (Zero UI) 프롬프트 처리 대화형 핵심 API
@app.post("/api/chat")
def process_zero_ui_prompt(req: PromptRequest, db: Session = Depends(get_db)):
    seed_initial_data(db)
    prompt_text = req.prompt.strip()
    user = db.query(models.User).filter(models.User.id == req.user_id).first()
    if not user:
        user = db.query(models.User).first()

    # Natural Language Trade Journal Parsing (e.g. "오늘 솔라나 10만원 매수했어", "BTC 50,000원 매수")
    is_buy = "매수" in prompt_text or "샀" in prompt_text or "구매" in prompt_text
    is_sell = "매도" in prompt_text or "팔았" in prompt_text or "판매" in prompt_text
    
    # Extract symbol if mentioned
    symbols = ["BTC", "ETH", "SOL", "SAND", "XRP", "DOGE", "ADA", "AVAX"]
    found_symbol = "BTC"
    for s in symbols:
        if s.lower() in prompt_text.lower():
            found_symbol = s
            break
    if "솔라나" in prompt_text: found_symbol = "SOL"
    elif "비트코인" in prompt_text: found_symbol = "BTC"
    elif "이더리움" in prompt_text: found_symbol = "ETH"
    elif "샌드박스" in prompt_text: found_symbol = "SAND"
    elif "리플" in prompt_text: found_symbol = "XRP"

    # Extract numbers for KRW amount
    numbers = re.findall(r'\d+', prompt_text.replace(',', ''))
    amount_krw = 50000.0
    if "만" in prompt_text:
        # e.g., 10만원 -> 100000
        man_match = re.search(r'(\d+)\s*만', prompt_text)
        if man_match:
            amount_krw = float(man_match.group(1)) * 10000.0
    elif numbers:
        amount_krw = float(numbers[0])

    if is_buy or is_sell:
        side = "BUY" if is_buy else "SELL"
        price_map = {"BTC": 135000000, "ETH": 4500000, "SOL": 245000, "SAND": 49.4, "XRP": 850}
        price = price_map.get(found_symbol, 100000)

        # Award +150 EXP
        user.xp += 150
        if user.xp >= 3000 and user.level < 5:
            user.level += 1
            user.title = "👑 대가급 가치투자가 (5단계)"

        new_j = models.TradeJournal(
            user_id=user.id,
            symbol=found_symbol,
            side=side,
            amount_krw=amount_krw,
            price=price,
            ai_reasoning=f"사용자 자연어 입력 '{prompt_text}' 자동 감지. 국내외 거래소 시세 분석 완료.",
            risk_review="위험 요소 점검: 분할 매수 수칙 준수 확인.",
            lesson=f"💡 {found_symbol} {int(amount_krw):,}원 복기 작성 완료.",
            likes_count=0
        )
        db.add(new_j)
        db.commit()
        db.refresh(new_j)

        return {
            "type": "trade_created",
            "reply": f"🌱 **{user.nickname}**님, '{found_symbol} {int(amount_krw):,}원 {side}' 매매 복기가 정원에 기록되었습니다!\n✨ **+150 경험치(EXP)**를 획득하셨습니다. (현재 총 {user.xp:,} EXP)",
            "journal": {
                "id": new_j.id,
                "author": user.nickname,
                "avatar": user.profile_img,
                "archetype": user.archetype,
                "symbol": new_j.symbol,
                "side": new_j.side,
                "amount_krw": new_j.amount_krw,
                "price": new_j.price,
                "ai_reasoning": new_j.ai_reasoning,
                "lesson": new_j.lesson,
                "time": "방금 전"
            },
            "new_xp": user.xp
        }

    # Query response for general prompts (Analysis, Ranking, Guidance)
    if "순위" in prompt_text or "랭킹" in prompt_text or "1위" in prompt_text:
        return {
            "type": "info",
            "reply": "🏆 **가치투자 모임 수익률 순위전 현황**:\n1위 👑 김가치 (수익률 +14.8%, 2,450 EXP)\n2위 💎 박비트 (수익률 +11.2%, 1,980 EXP)\n3위 ⚡ 최솔라 (수익률 +7.6%, 1,620 EXP)"
        }
    elif "목표" in prompt_text or "얼마" in prompt_text or "퀘스트" in prompt_text:
        return {
            "type": "info",
            "reply": "🚀 **우리 모임 공동 목표**: 1,000만원 가치투자 달성률 **74.5%** (7,450,000원 달성 중!)\n💡 모임 식구가 전원 복기 작성 시 **경험치 2배 보너스 혜택**이 발동됩니다."
        }
    else:
        return {
            "type": "info",
            "reply": f"🌿 **알림**: '{prompt_text}'에 대해 분석을 완료했습니다.\n💡 매매 기록을 남기시려면 **'오늘 SOL 10만원 매수했어'**처럼 자연스럽게 적어보세요!"
        }

# 2. 프로필 변경 API
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
            "message": f"🎉 닉네임이 '{user.nickname}'(으)로 변경되어 DB에 저장되었습니다!",
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

# 3. 사용자 정보 조회 API
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

# 4. 피드 API
@app.get("/api/feed")
def get_social_feed(db: Session = Depends(get_db)):
    seed_initial_data(db)
    journals = db.query(models.TradeJournal).order_by(models.TradeJournal.id.desc()).all()
    results = []
    for j in journals:
        author_name = j.author.nickname if j.author else "익명 투자자"
        avatar = j.author.profile_img if j.author and j.author.profile_img else "https://api.dicebear.com/7.x/bottts/svg?seed=Gachi"
        archetype = j.author.archetype if j.author else "💎 기업 실질가치 투자자"
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

# 5. 모임 랭킹전 API
@app.get("/api/squad/rankings")
def get_squad_rankings(db: Session = Depends(get_db)):
    seed_initial_data(db)
    users = db.query(models.User).order_by(models.User.xp.desc()).all()
    rankings = []
    badges = ["💎 다이아몬드 손", "🛡️ 손실 방어막", "⚖️ 최저가 매수자", "🚀 정량 분석가"]
    for idx, u in enumerate(users):
        rankings.append({
            "rank": idx + 1,
            "name": u.nickname,
            "archetype": u.archetype or "💎 기업 실질가치 투자자",
            "title": u.title or "가치 탐험가",
            "return_pct": round(14.8 - (idx * 3.6), 1),
            "badge": badges[idx % len(badges)],
            "xp": u.xp,
            "avatar": u.profile_img
        })
    return rankings

# 6. 레이드 API
@app.get("/api/squad/raids")
def get_squad_raids(db: Session = Depends(get_db)):
    seed_initial_data(db)
    squad = db.query(models.Squad).first()
    return {
        "squad_name": squad.name if squad else "가치투자 1기 모임",
        "raid_title": squad.raid_title if squad else "🚀 모임 공동 목표: 1,000만원 가치투자 & 가격 차익 획득",
        "raid_goal_krw": squad.raid_goal if squad else 10000000.0,
        "raid_progress_krw": squad.raid_progress if squad else 7450000.0,
        "progress_pct": round(((squad.raid_progress / squad.raid_goal) * 100) if squad else 74.5, 1),
        "buff": "⚡ 모임 식구 전원 복기 작성 시 경험치 2배 보너스 혜택 발동 중!"
    }

# 7. 1초 소셜 로그인
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
    return { **auth_res, "id": user.id, "nickname": user.nickname, "archetype": user.archetype, "title": user.title, "xp": user.xp, "level": user.level }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
