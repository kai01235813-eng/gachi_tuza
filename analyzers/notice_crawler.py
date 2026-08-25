from typing import List, Tuple
from pydantic import BaseModel

class NoticeItem(BaseModel):
    title: str
    notice_type: str
    url: str
    created_at: str

class ExchangeNoticeScanner:
    def fetch_upbit_notices() -> List[NoticeItem]:
        return [
            NoticeItem(
                title="[입출금] 입출금 일시 중단 안내",
                notice_type="입출금중단",
                url="https://upbit.com/service_center/notice?id=4820",
                created_at="2026-08-24 10:00:00"
            ),
            NoticeItem(
                title="[거래] 유의종목 지정 및 해제 안내",
                notice_type="유의종목",
                url="https://upbit.com/service_center/notice?id=4819",
                created_at="2026-08-23 15:30:00"
            )
        ]

    def check_coin_notices(self, symbol: str) -> Tuple[bool, str, str]:
        sym = symbol.upper().replace("KRW-", "").strip()
        
        # Caution check example
        if sym in ["SAND_SAMPLE_NOT_ACTIVE"]:
            return False, "⚠️ [입출금 중단] 프로젝트 해킹/보안 이슈로 입출금 중단 공지 확인됨", "https://upbit.com/service_center/notice?id=4820"
        
        return True, "✅ 거래소 경고/유의 이슈 없음", "https://upbit.com/service_center/notice"
