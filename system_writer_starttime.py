import json
import psutil
import time
import threading
import subprocess
import os

# Beim ersten Start Startzeit setzen (Unix Timestamp)
START_TIME = int(time.time())

def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent

    return {
        "start": START_TIME,
        "cpu": f"{cpu_usage:.1f}%",
        "ram": f"{ram_usage:.1f}%"
    }

def write_system_json():
    data = get_system_info()
    with open("system.json", "w") as f:
        json.dump(data, f, indent=2)

def git_push():
    try:
        subprocess.run(["git", "add", "system.json"], check=True)
        subprocess.run(["git", "commit", "-m", "update system uptime"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ system.json gepusht")
    except subprocess.CalledProcessError as e:
        print("❌ Git-Fehler:", e)

def loop_writer():
    while True:
        write_system_json()
        git_push()
        time.sleep(60)  # jede Minute

def start_system_writer():
    threading.Thread(target=loop_writer, daemon=True).start()

# Aufruf in deinem Bot:
# from system_writer_starttime import start_system_writer
# start_system_writer()
