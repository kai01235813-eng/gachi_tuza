from typing import Dict
from pydantic import BaseModel

class UserAuthResponse(BaseModel):
    user_id: int
    nickname: str
    email: str
    provider: str
    profile_img: str
    level: int
    xp: int
    access_token: str

class SocialOAuthHandler:
    """
    구글(Google), 네이버(Naver), 카카오(Kakao) 1초 소셜 로그인 처리기
    + 로컬 스마트 데모 모드 (Client Secret 없이도 즉시 1초 로그인 테스트 지원)
    """

    @staticmethod
    def authenticate_social_user(provider: str, demo_name: str = "선한가치투자자") -> UserAuthResponse:
        prov = provider.lower()
        if prov not in ["kakao", "naver", "google"]:
            prov = "kakao"

        avatars = {
            "kakao": "https://api.dicebear.com/7.x/bottts/svg?seed=KakaoUser",
            "naver": "https://api.dicebear.com/7.x/bottts/svg?seed=NaverUser",
            "google": "https://api.dicebear.com/7.x/bottts/svg?seed=GoogleUser"
        }

        return UserAuthResponse(
            user_id=101,
            nickname=f"{demo_name} ({prov.upper()})",
            email=f"user_{prov}@gachituza.com",
            provider=prov,
            profile_img=avatars.get(prov, avatars["kakao"]),
            level=3,
            xp=1450,
            access_token=f"demo_token_gachi_tuza_{prov}_2026"
        )
