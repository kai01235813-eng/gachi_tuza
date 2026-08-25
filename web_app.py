import os
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from auth.oauth import SocialOAuthHandler
from analyzers import (
    GitHubAnalyzer,
    KoreanPsychologyAnalyzer,
    ExchangeNoticeScanner,
    LiquidationHeatmapEngine,
    SmartTradingAssistantEngine,
    TriangularArbitrageEngine
)

app = FastAPI(
    title="같이투자 (Gachi Tuza) - 오픈소스 가치투자 소셜 플랫폼",
    description="지인들과 함께 공유하고 진짜 가치에 투자하는 100% 오픈소스 플랫폼",
    version="1.0.0"
)

# Serves main responsive single-page web app
@app.get("/")
def read_root():
    html_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return JSONResponse({"message": "같이투자 (Gachi Tuza) 백엔드가 정상 동작 중입니다."})

# 1. 3대 1초 소셜 로그인 API (Google, Naver, Kakao)
@app.post("/api/auth/login/{provider}")
def social_login(provider: str):
    auth_res = SocialOAuthHandler.authenticate_social_user(provider)
    return auth_res

# 2. 지인 가치투자 복기 피드 API (Social Strategy Feed)
@app.get("/api/feed")
def get_social_feed():
    return [
        {
            "id": 1,
            "author": "김가치 (스쿼드 리더)",
            "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=KimGachi",
            "symbol": "SAND",
            "side": "BUY",
            "amount_krw": 10000,
            "time": "10분 전",
            "ai_reasoning": "업비트 실질가 49.4원으로 빗썸 대비 5.35% 저렴한 최저가 라우팅 확인. GitHub 개발 펀더멘털 점수 81점.",
            "risk_review": "거래소 입출금 중단 유의 공지 확인됨. 추가 매수 금지 수칙 준수.",
            "lesson": "💡 소액 테스트 매수 완료. 유의 공지 해제 전까지 추가 매수를 금지하여 자산 보호.",
            "likes": 12
        },
        {
            "id": 2,
            "author": "박비트 (선한가치투자자)",
            "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=ParkBit",
            "symbol": "SOL",
            "side": "BUY",
            "amount_krw": 50000,
            "time": "1시간 전",
            "ai_reasoning": "김치 프리미엄 +2.21% 안정이격 구간. 개발 커밋 92점으로 극상급 펀더멘털.",
            "risk_review": "솔라나 메인넷 검증인 스테이킹(Staking) 연 6.5% 이자 중복 창출 시작.",
            "lesson": "💎 현물 저점 매수 후 스테이킹 복리 이자 모으기 완수.",
            "likes": 19
        }
    ]

# 3. 스쿼드 랭킹전 API (Squad Leaderboard)
@app.get("/api/squad/rankings")
def get_squad_rankings():
    return [
        {"rank": 1, "name": "김가치 (스쿼드 리더)", "return_pct": 14.8, "badge": "💎 다이아몬드 핸드", "xp": 2450},
        {"rank": 2, "name": "박비트 (가치투자자)", "return_pct": 11.2, "badge": "🛡️ FOMO 방어막", "xp": 1980},
        {"rank": 3, "name": "최솔라 (스쿼드 멤버)", "return_pct": 8.5, "badge": "⚖️ 최저가 라우터", "xp": 1620}
    ]

# 4. 정량 청산 데이터 API
@app.get("/api/liquidation/{symbol}")
def get_liquidation(symbol: str = "BTC"):
    return LiquidationHeatmapEngine.get_quantitative_analysis(symbol)

# 5. 삼각 차익거래 & 빗썸 0.04% 스캐너 API
@app.get("/api/triangular")
def get_triangular():
    return TriangularArbitrageEngine.calculate_triangular_arbitrage()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
