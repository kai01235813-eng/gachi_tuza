import os
import urllib.parse
import psycopg2

def try_connect_and_run():
    raw_pwd = "Kai1235813!@#"
    enc_pwd = urllib.parse.quote_plus(raw_pwd)
    project_ref = "olanskglzsvskalkwzdc"

    schema_file = os.path.join(os.path.dirname(__file__), "supabase", "schema.sql")
    with open(schema_file, "r", encoding="utf-8") as f:
        sql_script = f.read()

    configs = [
        # (host, port, user, password)
        (f"aws-0-ap-south-1.pooler.supabase.com", 6543, f"postgres.{project_ref}", enc_pwd),
        (f"aws-0-ap-south-1.pooler.supabase.com", 6543, f"postgres.{project_ref}", raw_pwd),
        (f"aws-0-ap-south-1.pooler.supabase.com", 5432, f"postgres.{project_ref}", enc_pwd),
        (f"aws-0-ap-south-1.pooler.supabase.com", 5432, f"postgres.{project_ref}", raw_pwd),
        (f"aws-0-ap-northeast-2.pooler.supabase.com", 6543, f"postgres.{project_ref}", enc_pwd),
        (f"aws-0-ap-northeast-2.pooler.supabase.com", 5432, f"postgres.{project_ref}", enc_pwd),
        (f"aws-0-ap-southeast-1.pooler.supabase.com", 6543, f"postgres.{project_ref}", enc_pwd),
        (f"aws-0-us-east-1.pooler.supabase.com", 6543, f"postgres.{project_ref}", enc_pwd),
        (f"db.{project_ref}.supabase.co", 5432, "postgres", enc_pwd),
        (f"db.{project_ref}.supabase.co", 5432, "postgres", raw_pwd),
    ]

    print("🚀 Supabase DB 자동 연결 및 스키마 생성을 진행합니다...")

    for host, port, user, pwd in configs:
        dsn = f"postgresql://{user}:{pwd}@{host}:{port}/postgres"
        try:
            print(f"⚡ 시도 중: {user}@{host}:{port} ...")
            conn = psycopg2.connect(dsn, connect_timeout=5)
            conn.autocommit = True
            cursor = conn.cursor()
            print("📜 SQL 스키마 (users, squads, trade_journals, portfolios) 실행 중...")
            cursor.execute(sql_script)
            print("\n=======================================================")
            print("🎉 [Supabase DB 테이블 및 RLS 보안 세팅 100% 자동 연결 성공!]")
            print("=======================================================\n")
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 실패 ({host}:{port}): {e}")

    return False

if __name__ == "__main__":
    try_connect_and_run()
