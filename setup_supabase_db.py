import os
import sys
import urllib.parse
import psycopg2

def setup_db(db_password: str):
    """
    Supabase PostgreSQL DB에 schema.sql 테이블과 초기 데이터를 1초 만에 생성합니다.
    """
    project_ref = "olanskglzsvskalkwzdc"
    # Safely URL-encode special characters like @, #, ! in database password
    encoded_pwd = urllib.parse.quote_plus(db_password)
    
    # Try pooler connection strings (ap-south-1 / pooler)
    db_urls = [
        f"postgresql://postgres.{project_ref}:{encoded_pwd}@aws-0-ap-south-1.pooler.supabase.com:6543/postgres",
        f"postgresql://postgres.{project_ref}:{encoded_pwd}@aws-0-ap-northeast-2.pooler.supabase.com:6543/postgres",
        f"postgresql://postgres:{encoded_pwd}@db.{project_ref}.supabase.co:5432/postgres"
    ]

    print(f"🚀 Supabase DB ({project_ref}) 테이블 자동 마이그레이션을 시작합니다...")

    schema_file = os.path.join(os.path.dirname(__file__), "supabase", "schema.sql")
    if not os.path.exists(schema_file):
        print(f"❌ '{schema_file}' 파일이 존재하지 않습니다.")
        return False

    with open(schema_file, "r", encoding="utf-8") as f:
        sql_script = f.read()

    connected = False
    for db_url in db_urls:
        try:
            print(f"⚡ 연결 시도: {db_url.split('@')[1]} ...")
            conn = psycopg2.connect(db_url, connect_timeout=10)
            conn.autocommit = True
            cursor = conn.cursor()
            
            print("⚡ SQL 스키마 실행 중 (users, squads, trade_journals, portfolios)...")
            cursor.execute(sql_script)
            
            print("\n=======================================================")
            print("🎉 [Supabase DB 100% 생성 및 마이그레이션 성공!]")
            print("• users, squads, trade_journals, portfolios 테이블 생성 완료")
            print("• Row Level Security (RLS) 보안 정책 적용 완료")
            print("=======================================================\n")
            cursor.close()
            conn.close()
            connected = True
            break
        except Exception as e:
            print(f"⚠️ 연결 차단/실패: {e}")

    return connected

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pwd = sys.argv[1]
        setup_db(pwd)
    else:
        setup_db("Kai1235813!@#")
