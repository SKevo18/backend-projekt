"""Script to start the API server on a shared hosting server (Namecheap)"""
import os
from pathlib import Path
from backend.kill import kill_api_server


def find_and_activate_venv():
    home_dir = Path.home()
    venv_base_dir = home_dir / "virtualenv"

    if not venv_base_dir.exists():
        print(f"venv dir not found ({venv_base_dir})")
        return False

    activate_scripts = list(venv_base_dir.glob("*/*/bin/activate"))
    if not activate_scripts:
        activate_scripts = list(venv_base_dir.glob("*/bin/activate"))

    if not activate_scripts:
        print(f"no venvs found in {venv_base_dir}")
        return False

    activate_script = activate_scripts[0]
    venv_path = activate_script.parent.parent

    os.environ["VIRTUAL_ENV"] = str(venv_path)
    os.environ["PATH"] = f"{venv_path}/bin:{os.environ.get('PATH', '')}"

    if "PYTHONHOME" in os.environ:
        del os.environ["PYTHONHOME"]

    return True


if __name__ == "__main__":
    if not find_and_activate_venv():
        print("failed to activate venv")
        exit(1)

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    kill_api_server()
    print("Starting API server...")
    os.system("nohup uvicorn main:API > api.log 2>&1 &")
