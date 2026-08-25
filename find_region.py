import psycopg2
import urllib.parse
import sys

pwd = urllib.parse.quote_plus("Kai1235813!@#")
project_ref = "olanskglzsvskalkwzdc"

regions = [
    "ap-northeast-2", # Seoul
    "ap-northeast-1", # Tokyo
    "ap-southeast-1", # Singapore
    "us-east-1",      # N. Virginia
    "us-west-1",      # N. California
    "eu-central-1",   # Frankfurt
    "eu-west-1",      # Ireland
    "eu-west-2",      # London
    "ca-central-1",   # Canada
    "sa-east-1",      # Sao Paulo
    "ap-south-1"      # Mumbai
]

print(f"🚀 Supabase DB ({project_ref}) 자동 연결 시도 시작...")
sys.stdout.flush()

connected = False
for r in regions:
    for port in [6543, 5432]:
        host = f"aws-0-{r}.pooler.supabase.com"
        user = f"postgres.{project_ref}"
        dsn = f"postgresql://{user}:{pwd}@{host}:{port}/postgres"
        try:
            conn = psycopg2.connect(dsn, connect_timeout=3)
            conn.autocommit = True
            print(f"\n🎉 [성공!] 리전: {r}, Port: {port}")
            print(f"⚡ 스키마 실행 시작...")
            
            with open("supabase/schema.sql", "r", encoding="utf-8") as f:
                sql = f.read()
            
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.close()
            conn.close()
            print("=======================================================")
            print("🎉 [Supabase DB 100% 생성을 완벽하게 완료했습니다!]")
            print("• users, squads, trade_journals, portfolios 테이블 마이그레이션 성공")
            print("=======================================================\n")
            connected = True
            break
        except Exception as e:
            err = str(e)
            if "password authentication failed" in err:
                print(f"🔑 리전 {r} 발견되었으나 비밀번호 오타 가능성: {err}")
                connected = True
                break
            elif "tenant/user" not in err:
                print(f"💡 {r}:{port} -> {err}")

    if connected:
        break

if not connected:
    print("❌ 스캔 완료: Direct Host 연결 재시도...")
