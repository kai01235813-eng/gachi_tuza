from pydantic import BaseModel
from .github_activity import GitHubAnalyzer
from .notice_crawler import ExchangeNoticeScanner

class TradingAssistantRecommendation(BaseModel):
    symbol: str
    action: str
    recommended_exchange: str
    upbit_net_price: str
    bithumb_net_price: str
    dev_score: float
    is_safe: bool
    caution_reason: str
    target_buy_range: str
    target_sell_range: str
    summary_advice: str
    upbit_app_link: str
    bithumb_app_link: str

class SmartTradingAssistantEngine:
    def __init__(self):
        self.github = GitHubAnalyzer()
        self.notice_scanner = ExchangeNoticeScanner()

    def evaluate_trading_decision(self, symbol: str, current_upbit_price: float = 0.0) -> TradingAssistantRecommendation:
        sym = symbol.upper().replace("KRW-", "").strip()
        is_safe, notice_reason, notice_url = self.notice_scanner.check_coin_notices(sym)
        dev_info = self.github.analyze_repository(sym)
        dev_score = dev_info.dev_activity_score

        upbit_link = f"https://upbit.com/exchange?code=CASA.KRW-{sym}"
        bithumb_link = f"https://m.bithumb.com/trade/order/KRW-{sym}"

        if not is_safe:
            return TradingAssistantRecommendation(
                symbol=sym,
                action="BLOCK (매수 절대 차단)",
                recommended_exchange="NONE",
                upbit_net_price="N/A",
                bithumb_net_price="N/A",
                dev_score=dev_score,
                is_safe=False,
                caution_reason=notice_reason,
                target_buy_range="매수 금지",
                target_sell_range="공식 발표 관망 후 정리",
                summary_advice=f"⛔ **매수 차단**: 거래소 유의종목/보안 이슈 발생. 자산 보호를 위해 현 시점 매수를 절대 금지합니다.\n공식 공지: {notice_url}",
                upbit_app_link=upbit_link,
                bithumb_app_link=bithumb_link
            )

        action = "BUY (분할 매수 적기)" if dev_score >= 75 else "HOLD (관망)"
        advice = f"🟢 **매수 적기**: 펀더멘털 점수 {dev_score:.0f}점으로 우수하며 안전합니다." if dev_score >= 75 else "🟡 **관망 조언**: 눌림목 조정을 기다리는 것이 유리합니다."

        return TradingAssistantRecommendation(
            symbol=sym,
            action=action,
            recommended_exchange="UPBIT (수수료 0.05%)",
            upbit_net_price=f"{current_upbit_price:,.1f} 원" if current_upbit_price > 0 else "실시간 확인",
            bithumb_net_price="실시간 확인",
            dev_score=dev_score,
            is_safe=True,
            caution_reason="✅ 거래소 경고 없음",
            target_buy_range="현재가 기준 3단계 분할 매수",
            target_sell_range="수익률 +15% ~ +30% 1차 익절",
            summary_advice=advice,
            upbit_app_link=upbit_link,
            bithumb_app_link=bithumb_link
        )
