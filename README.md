# 🌟 같이투자 (Gachi Tuza) - 오픈소스 소셜 트레이딩 플랫폼

[![Deploy with Vercel](https.vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fgachi-tuza%2Fgachi-tuza)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **"지인들과 같이(Together) 공유하고, 진짜 가치(Value)에 투자한다!"**
> 대한민국 대표 100% 오픈소스(Vercel + Supabase) 소셜 트레이딩 & 가치투자 플랫폼

---

## 🏛️ Vercel + Supabase 오픈소스 아키텍처

- **웹 호스팅 & 배포**: **Vercel** (Edge Network CDN & Git Push 1초 자동 배포)
- **백엔드 & DB**: **Supabase (PostgreSQL + Auth + Realtime)**
- **1초 소셜 로그인**: 카카오(Kakao), 네이버(Naver), 구글(Google) OAuth 2.0
- **라이선스**: **MIT License** (누구나 포크하고 배포 가능)

---

## 🚀 1분 원클릭 Vercel 배포 가이드

1. **상단의 `Deploy with Vercel` 버튼을 클릭**하여 본인 GitHub 계정으로 포크(Fork)합니다.
2. **Supabase 프로젝트 무료 생성** 후 `supabase/schema.sql`을 실행합니다.
3. Vercel 환경변수에 `VITE_SUPABASE_URL` 및 `VITE_SUPABASE_ANON_KEY`를 등록하면 **365일 무료 무중단 플랫폼 구동 시작!**

---

## 🛡️ 보안 & 오픈소스 커뮤니티

- 개인 API 키나 세션 비밀번호는 `.gitignore`로 깃허브 유출 100% 차단
- 유저 자산에 손댈 수 없는 **`Read-Only (조회 전용) API`**로 안심 랭킹전 참여
