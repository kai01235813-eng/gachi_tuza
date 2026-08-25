from pydantic import BaseModel

class KoreanMarketPsychology(BaseModel):
    upbit_btc_price: float
    binance_btc_usdt: float
    estimated_usd_krw_rate: float
    kimchi_premium_pct: float
    korean_fomo_level: str
    contrarian_action_advice: str

class KoreanPsychologyAnalyzer:
    @staticmethod
    def analyze(upbit_btc_krw: float = 107000000.0, binance_btc_usdt: float = 76500.0) -> KoreanMarketPsychology:
        usd_krw = 1410.0
        binance_krw = binance_btc_usdt * usd_krw
        kimp_pct = ((upbit_btc_krw - binance_krw) / binance_krw) * 100.0

        if kimp_pct > 7.0:
            level = "🚨 [과열 경고] 대중 과열 분노 매수 (FOMO Peak)"
            advice = "🛑 신규 매수 전면 자제. 현금 비중 확충 및 부분 익절 구간."
        elif kimp_pct < 1.0:
            level = "🟢 [패닉 역발상] 대중 공포 투매 (Panic Dump Zone)"
            advice = "💎 최고의 역발상 분할 매수 수집 구간!"
        else:
            level = "🟢 [안정적] 적정 프리미엄 유지 중"
            advice = "💎 펀더멘털 기반 우수 알트코인 분할 매수 적기"

        return KoreanMarketPsychology(
            upbit_btc_price=upbit_btc_krw,
            binance_btc_usdt=binance_btc_usdt,
            estimated_usd_krw_rate=usd_krw,
            kimchi_premium_pct=round(kimp_pct, 2),
            korean_fomo_level=level,
            contrarian_action_advice=advice
        )
