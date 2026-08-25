from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="같이투자 (Gachi Tuza) Vercel Serverless API")

@app.get("/api/health")
def health_check():
    return JSONResponse({"status": "ok", "platform": "Vercel Serverless + Supabase", "version": "1.0.0"})

@app.get("/api/liquidation/{symbol}")
def get_liquidation(symbol: str = "BTC"):
    return {
        "symbol": symbol.upper(),
        "current_price_usd": "$97,200",
        "long_total_risk_usd": "$2.85B (약 3조 9,900억 원)",
        "short_total_risk_usd": "$2.10B (약 2조 9,400억 원)",
        "levels": [
            {"target_price_usd": "$95,000", "target_price_krw": "13,300만 원", "direction": "LONG (하방)", "estimated_volume_usd": "$480M", "estimated_volume_krw": "6,720억 원", "impact_level": "⚠️ 중형 청산"},
            {"target_price_usd": "$93,500", "target_price_krw": "13,090만 원", "direction": "LONG (하방)", "estimated_volume_usd": "$1.25B", "estimated_volume_krw": "1조 7,500억 원", "impact_level": "🔥 대규모 롱 청산 빔"}
        ]
    }
