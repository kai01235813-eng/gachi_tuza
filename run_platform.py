import time
import subprocess
import sys

def run_platform():
    """
    오픈소스 소셜 트레이딩 플랫폼 [같이투자 (Gachi Tuza)] 백엔드 및
    외부 스마트폰 24시간 접속 지속성 통신 터널 구동기
    """
    print("🌟 [같이투자 (Gachi Tuza)] 오픈소스 소셜 플랫폼 실행 시작...")
    
    # 1. FastAPI Web Server Process
    print("🚀 FastAPI 소셜 웹 앱 서버 구동 중 (http://0.0.0.0:8000)...")
    server_cmd = [sys.executable, "web_app.py"]
    server_proc = subprocess.Popen(server_cmd)

    # 2. Localtunnel Persistent Daemon
    print("🌐 스마트폰 외부 접속 지원 localtunnel 통신 터널 개설 중...")
    try:
        tunnel_cmd = "npx -y localtunnel --port 8000"
        tunnel_proc = subprocess.Popen(
            tunnel_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        
        for line in tunnel_proc.stdout:
            line_str = line.strip()
            if "your url is:" in line_str:
                print(f"\n=======================================================")
                print(f"✅ [같이투자 외부 모바일 접속 HTTPS URL] {line_str}")
                print(f"=======================================================\n")
                sys.stdout.flush()
    except Exception as e:
        print(f"⚠️ 터널 개설 중 예외: {e}")

    server_proc.wait()

if __name__ == "__main__":
    run_platform()
