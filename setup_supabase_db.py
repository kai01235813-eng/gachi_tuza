import os
import sys
import psycopg2

def setup_db(db_password: str):
    """
    Supabase PostgreSQL DB에 schema.sql 테이블과 초기 데이터를 1초 만에 생성합니다.
    """
    project_ref = "olanskglzsvskalkwzdc"
    # Direct database connection URL for Supabase
    db_url = f"postgresql://postgres:{db_password}@db.{project_ref}.supabase.co:5432/postgres"

    print(f"🚀 Supabase DB ({project_ref}) 테이블 자동 생성을 시작합니다...")

    schema_file = os.path.join(os.path.dirname(__file__), "supabase", "schema.sql")
    if not os.path.exists(schema_file):
        print(f"❌ '{schema_file}' 파일이 존재하지 않습니다.")
        return False

    with open(schema_file, "r", encoding="utf-8") as f:
        sql_script = f.read()

    try:
        conn = psycopg2.connect(db_url, connect_timeout=10)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("⚡ SQL 스키마 실행 중 (users, squads, trade_journals)...")
        cursor.execute(sql_script)
        
        print("🎉 [Supabase DB 생성 성공!] 모든 테이블과 샘플 데이터가 연동되었습니다!")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ DB 연결/실행 오류: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pwd = sys.argv[1]
        setup_db(pwd)
    else:
        print("사용법: python setup_supabase_db.py <YOUR_SUPABASE_DB_PASSWORD>")
