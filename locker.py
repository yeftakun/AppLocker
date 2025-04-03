import os
import sys
import json
import time
import psutil
import schedule
from datetime import datetime, timedelta
import ctypes  # Untuk menampilkan MessageBox

DB_FILE = "locker_db.json"

# Pastikan file database ada jika belum dibuat
def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"locked_apps": []}, f)

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Menambahkan aplikasi ke daftar kuncian
def add_lock(path, days, hours, minutes):
    expire_time = datetime.now() + timedelta(days=days, hours=hours, minutes=minutes)
    data = load_db()
    data["locked_apps"].append({
        "path": path,
        "expire_time": expire_time.strftime("%Y-%m-%d %H:%M:%S")
    })
    save_db(data)
    print(f"✅ {path} dikunci hingga {expire_time}")

# Menampilkan daftar aplikasi yang dikunci
def list_locks():
    data = load_db()
    if not data["locked_apps"]:
        print("Tidak ada aplikasi yang dikunci.")
        return
    
    print("Daftar aplikasi yang dikunci:")
    for idx, app in enumerate(data["locked_apps"], 1):
        print(f"{idx}. {app['path']} - Hingga {app['expire_time']}")

# Menghapus aplikasi dari daftar berdasarkan ID
def delete_lock(idx):
    data = load_db()
    try:
        removed = data["locked_apps"].pop(idx - 1)
        save_db(data)
        print(f"✅ {removed['path']} telah dihapus dari daftar kuncian.")
    except IndexError:
        print("❌ ID tidak valid!")

# Mengecek apakah ada aplikasi yang sudah tidak perlu dikunci
def clean_expired():
    data = load_db()
    now = datetime.now()
    data["locked_apps"] = [app for app in data["locked_apps"] if datetime.strptime(app["expire_time"], "%Y-%m-%d %H:%M:%S") > now]
    save_db(data)

# Menampilkan alert window di Windows
def show_alert(message):
    ctypes.windll.user32.MessageBoxW(0, message, "AppLocker Alert", 0x40 | 0x1)  # 0x40 = Information icon, 0x1 = OK button

# Mengecek proses yang berjalan dan memblokir aplikasi yang ada di daftar
def monitor_processes():
    data = load_db()
    locked_paths = {app["path"] for app in data["locked_apps"]}
    for proc in psutil.process_iter(attrs=["pid", "exe"]):
        try:
            if proc.info["exe"] and proc.info["exe"] in locked_paths:
                proc.terminate()
                print(f"🔒 {proc.info['exe']} dihentikan!")
                show_alert(f"Di kunci AppLocker, '{proc.info['exe']}' tidak dapat dijalankan. Gunakan 'applocker list' untuk melihat daftar aplikasi.")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

# Looping background untuk pengecekan otomatis
def background_loop():
    schedule.every(5).seconds.do(monitor_processes)
    schedule.every(30).seconds.do(clean_expired)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Menjalankan CLI
if __name__ == "__main__":
    init_db()
    
    if len(sys.argv) < 2:
        print("Gunakan: applocker [list | del ID | -p path -d hari -h jam -m menit]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        list_locks()
    elif command == "del":
        if len(sys.argv) < 3:
            print("Gunakan: applocker del list_num")
            sys.exit(1)
        delete_lock(int(sys.argv[2]))
    elif command == "-p":
        if len(sys.argv) < 8:
            print("Gunakan: applocker -p path -d hari -h jam -m menit")
            sys.exit(1)
        path = sys.argv[2]
        days = int(sys.argv[4])
        hours = int(sys.argv[6])
        minutes = int(sys.argv[8])
        add_lock(path, days, hours, minutes)
    elif command == "run":
        print("🔄 Monitoring aplikasi berjalan...")
        background_loop()
    else:
        print("Perintah tidak dikenal.")
