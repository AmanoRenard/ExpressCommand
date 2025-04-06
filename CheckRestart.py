import os
import subprocess
import sys
from pathlib import Path

def dump_env():
    exe_dir = Path(sys.argv[0]).resolve().parent
    dump_file = exe_dir / "env_dump.txt"
    with dump_file.open("w", encoding="utf-8") as f:
        f.write(f"CWD={os.getcwd()}\n")
        f.write(f"sys.executable={sys.executable}\n")
        f.write(f"sys.argv={sys.argv}\n\n")
        for k, v in os.environ.items():
            f.write(f"{k}={v}\n")
    print(f"环境已写入：{dump_file}")

def write_and_run_update_script():
    current_path = os.path.abspath(sys.argv[0])  # 当前 exe 路径
    exe_dir = os.path.dirname(current_path)
    exe_name = os.path.basename(current_path)

    # 确保路径双引号包住，防止空格或中文乱码
    download_url = "https://expresscommand.chamiko.com/ExpressCommand.exe"
    new_exe_path = os.path.join(exe_dir, "ExpressCommand_new.exe")

    bat_content = f"""@echo off
set "_PYI_APPLICATION_HOME_DIR="
set "_PYI_ARCHIVE_FILE="
set "_PYI_PARENT_PROCESS_LEVEL="
set "TCL_LIBRARY="
set "TK_LIBRARY="

chcp 65001 >nul
echo 正在准备更新...
timeout /t 2 >nul

echo 正在更新...
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('{download_url}', '{new_exe_path}')"

del /f /q "{current_path}"
rename "{new_exe_path}" "{exe_name}"

echo 更新完毕！重启中...
start "" "{current_path}"

exit
"""

    bat_path = os.path.join(r"C:\Program Files\LogData", "ExpressCommandUpdate.bat")
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(bat_content)

    # 运行 bat 并关闭自己
    subprocess.Popen(['cmd', '/c', str(bat_path)], shell=True)

def restart_script():
    current_path = os.path.abspath(sys.argv[0])  # 当前 exe 路径

    bat_content = f"""@echo off
set "_PYI_APPLICATION_HOME_DIR="
set "_PYI_ARCHIVE_FILE="
set "_PYI_PARENT_PROCESS_LEVEL="
set "TCL_LIBRARY="
set "TK_LIBRARY="

chcp 65001 >nul
timeout /t 3 >nul


start "" "{current_path}"

exit
"""

    bat_path = os.path.join(r"C:\Program Files\LogData", "ExpressCommandUpdate.bat")
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(bat_content)

    # 运行 bat 并关闭自己
    subprocess.Popen(['cmd', '/c', str(bat_path)], shell=True)
