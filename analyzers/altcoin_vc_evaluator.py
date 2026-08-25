from pydantic import BaseModel

class AltcoinVCMetrics(BaseModel):
    symbol: str
    name: str
    tokenomics_score: float
    dev_score: float
    world_impact_mission: str
    long_term_recommendation: str

class AltcoinVCEvaluator:
    @staticmethod
    def evaluate(symbol: str, dev_score: float = 80.0) -> AltcoinVCMetrics:
        sym = symbol.upper().replace("KRW-", "").strip()

        names = {
            "BTC": "비트코인", "ETH": "이더리움", "SOL": "솔라나",
            "SAND": "샌드박스", "LINK": "체인링크", "NEAR": "니어프로토콜",
            "XRP": "리플", "ADA": "에이다", "DOGE": "도지코인", "APT": "앱토스", "SUI": "수이"
        }
        name = names.get(sym, sym)

        missions = {
            "BTC": "글로벌 탈중앙화 인플레이션 헤지 및 가치 저장 수단",
            "ETH": "글로벌 스마트 컨트랙트 및 웹3 핀테크 컴퓨팅 기저층",
            "SOL": "초고속 분산 금융(DeFi) 및 소비자 웹3 스케일링",
            "SAND": "크리에이터 자율 소유 3D 가상세계 메타버스 메인넷",
            "LINK": "현실 세계 데이터(오라클) 및 금융 통신(CCIP) 분산 연동"
        }
        mission = missions.get(sym, f"{name} 생태계 탈중앙화 분산 시스템 구축")

        if dev_score >= 80:
            rec = "💎 [우수 펀더멘털] 분할 매수 및 스테이킹 장기 보유 적기"
        else:
            rec = "🟡 [관망 추천] 개발 커밋 점수 보완 후 수집 추천"

        return AltcoinVCMetrics(
            symbol=sym,
            name=name,
            tokenomics_score=85.0,
            dev_score=dev_score,
            world_impact_mission=mission,
            long_term_recommendation=rec
        )
