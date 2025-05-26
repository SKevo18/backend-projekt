"""Script to kill the API server on a shared hosting server (Namecheap)"""
import os
import subprocess
import signal


def kill_api_server():
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
            return True
        else:
            print("No running API processes found.")
            return False
    except Exception as e:
        print(f"Error checking for existing processes: {e}")
        return False


if __name__ == "__main__":
    kill_api_server()
