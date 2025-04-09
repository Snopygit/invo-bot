import json
import psutil
import threading
import time
import subprocess
from datetime import timedelta

# Startzeit für die Uptime
start_time = time.time()

# Systeminfos sammeln und speichern
def get_system_info():
    now = time.time()
    uptime = str(timedelta(seconds=int(now - start_time)))
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent

    data = {
        "uptime": uptime,
        "cpu": f"{cpu:.1f}%",
        "ram": f"{ram:.1f}%"
    }

    with open("system.json", "w") as f:
        json.dump(data, f, indent=2)

# Datei zu GitHub pushen
def git_push():
    try:
        subprocess.run(["git", "add", "system.json"], check=True)
        subprocess.run(["git", "commit", "-m", "update system info"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ system.json erfolgreich gepusht.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git-Fehler: {e}")

# Endlosschleife im Hintergrund
def start_system_writer():
    def write_loop():
        while True:
            get_system_info()
            git_push()
            time.sleep(120)  # alle 2 Minuten

    threading.Thread(target=write_loop, daemon=True).start()

# Diese Funktion rufst du beim Start deines Bots auf:
# start_system_writer()
