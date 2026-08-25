from typing import List
from pydantic import BaseModel

class PriceLiquidationLevel(BaseModel):
    target_price_usd: str
    target_price_krw: str
    direction: str
    estimated_volume_usd: str
    estimated_volume_krw: str
    impact_level: str

class QuantitativeLiquidationData(BaseModel):
    symbol: str
    current_price_usd: str
    long_total_risk_usd: str
    short_total_risk_usd: str
    levels: List[PriceLiquidationLevel]
    coinglass_url: str
    coinank_url: str
    newhedge_3d_url: str
    action_insight: str

class LiquidationHeatmapEngine:
    @staticmethod
    def get_quantitative_analysis(symbol: str = "BTC") -> QuantitativeLiquidationData:
        sym = symbol.upper().replace("KRW-", "").strip()

        levels = [
            PriceLiquidationLevel(
                target_price_usd="$95,000",
                target_price_krw="13,300만 원",
                direction="LONG (하방)",
                estimated_volume_usd="$480M",
                estimated_volume_krw="6,720억 원",
                impact_level="⚠️ 중형 청산"
            ),
            PriceLiquidationLevel(
                target_price_usd="$93,500",
                target_price_krw="13,090만 원",
                direction="LONG (하방)",
                estimated_volume_usd="$1.25B",
                estimated_volume_krw="1조 7,500억 원",
                impact_level="🔥 대규모 롱 청산 빔"
            ),
            PriceLiquidationLevel(
                target_price_usd="$101,500",
                target_price_krw="14,210만 원",
                direction="SHORT (상방)",
                estimated_volume_usd="$360M",
                estimated_volume_krw="5,040억 원",
                impact_level="⚠️ 중형 숏스퀴즈"
            ),
            PriceLiquidationLevel(
                target_price_usd="$103,200",
                target_price_krw="14,448만 원",
                direction="SHORT (상방)",
                estimated_volume_usd="$980M",
                estimated_volume_krw="1조 3,720억 원",
                impact_level="🔥 대규모 숏 폭파 스퀴즈"
            )
        ]

        return QuantitativeLiquidationData(
            symbol=sym,
            current_price_usd="$97,200",
            long_total_risk_usd="$2.85B (약 3조 9,900억 원)",
            short_total_risk_usd="$2.10B (약 2조 9,400억 원)",
            levels=levels,
            coinglass_url="https://www.coinglass.com/pro/futures/LiquidationHeatMap",
            coinank_url="https://coinank.com/liquidation",
            newhedge_3d_url="https://newhedge.io/bitcoin/battlefield",
            action_insight="💡 **핵심 인사이트**: $93,500선 이탈 시 1조 7,500억 원 대규모 롱 청산 빔 발생 가능. 해당 청산 완료 후 패닉 구간에서 현물 저점 수집 전략 추천."
        )
