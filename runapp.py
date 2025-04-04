import time
import json
import psutil
import schedule
import threading
import ctypes
import os
from datetime import datetime, timedelta
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import sys

DB_FILE = "locker_db.json"

# def get_base_dir():
#     # Gunakan path asli saat dikompilasi dengan PyInstaller
#     if getattr(sys, 'frozen', False):
#         return os.path.dirname(sys.executable)
#     else:
#         return os.path.dirname(os.path.abspath(__file__))

# BASE_DIR = get_base_dir()
# DB_FILE = os.path.join(BASE_DIR, "locker_db.json")

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

def clean_expired():
    data = load_db()
    now = datetime.now()
    data["locked_apps"] = [app for app in data["locked_apps"]
                           if datetime.strptime(app["expire_time"], "%Y-%m-%d %H:%M:%S") > now]
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def show_alert(message):
    ctypes.windll.user32.MessageBoxW(0, message, "AppLocker Alert", 0x40 | 0x1)

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
                show_alert(f"Di kunci AppLocker, '{proc.info['exe']}' tidak dapat dijalankan.")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

def background_loop():
    schedule.every(5).seconds.do(monitor_processes)
    schedule.every(30).seconds.do(clean_expired)
    while True:
        schedule.run_pending()
        time.sleep(1)


# def create_icon():
#     image = Image.new("RGB", (64, 64), "red")
#     d = ImageDraw.Draw(image)
#     d.rectangle([16, 16, 48, 48], fill="white")
#     return image

from PIL import Image, ImageDraw  # Hapus ImageResampling jika tidak diperlukan

def create_icon():
    # Cek apakah aplikasi berjalan dalam mode PyInstaller
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # Direktori sementara PyInstaller
    else:
        base_path = os.path.dirname(__file__)  # Direktori script

    icon_path = os.path.join(base_path, "AppLock_icon.ico")
    if not os.path.exists(icon_path):
        raise FileNotFoundError(f"Icon file not found: {icon_path}")

    icon = Image.open(icon_path)
    icon = icon.resize((64, 64), Image.Resampling.LANCZOS)  # Gunakan LANCZOS
    return icon

def on_list():
    os.system("start listapp.exe")

def on_add():
    os.system("start addapp.exe")

def on_exit(icon, item):
    icon.stop()
    os._exit(0)

def tray_icon():
    icon = pystray.Icon("AppLocker")
    icon.icon = create_icon()
    icon.title = "AppLocker Running"
    icon.menu = (
        item("New Block", on_add),
        item("Blocked App", on_list),
        item("Stop", on_exit)
    )
    icon.run()

if __name__ == "__main__":
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"locked_apps": []}, f)

    threading.Thread(target=background_loop, daemon=True).start()
    tray_icon()
