import json
import psutil
import threading
import time
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

# Endlosschleife im Hintergrund

def start_system_writer():
    def write_loop():
        while True:
            get_system_info()
            time.sleep(60)

    threading.Thread(target=write_loop, daemon=True).start()

# Diese Funktion rufst du beim Start deines Bots auf:
# start_system_writer()

# Beispielintegration in deinen Bot-Code:
# from system_writer import start_system_writer
# start_system_writer()
