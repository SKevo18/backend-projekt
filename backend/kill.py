"""Script to kill the API server on a shared hosting server (Namecheap)"""

import os
import subprocess
import signal


def get_api_server_pids():
    try:
        result = subprocess.check_output(["pgrep", "-f", "uvicorn main:API"], text=True)
        if result.strip():
            pids = result.strip().split("\n")
            return pids
    except Exception:
        pass

    return []


def kill_api_server():
    pids = get_api_server_pids()
    if pids:
        for pid in pids:
            try:
                os.kill(int(pid), signal.SIGTERM)
            except (ProcessLookupError, ValueError):
                pass
        print("killed")
        return True

    return False


if __name__ == "__main__":
    kill_api_server()
