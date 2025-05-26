import os
import subprocess
import signal

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# if running, kill & restart
try:
    result = subprocess.run(
        ["pgrep", "-f", "uvicorn main:API"], capture_output=True, text=True
    )
    if result.stdout.strip():
        pids = result.stdout.strip().split("\n")
        print(f"Killing existing API processes: {pids}")
        for pid in pids:
            try:
                os.kill(int(pid), signal.SIGTERM)
            except (ProcessLookupError, ValueError):
                pass
        print("Existing processes killed.")
except Exception as e:
    print(f"Error checking for existing processes: {e}")

print("Starting API server...")
os.system("nohup uvicorn main:API --proxy-headers > api.log 2>&1 &")
