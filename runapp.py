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
import subprocess
import webbrowser
import pygame
import socket

AUDIO_FILE = "alert.wav"  # Ganti dengan path file audio kamu

server_process = None
DB_FILE = "locker_db.json"

# Inisialisasi pygame mixer sekali saat awal
pygame.mixer.init()
try:
    pygame.mixer.music.load(AUDIO_FILE)
except Exception as e:
    print(f"Gagal memuat audio: {e}")

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

def play_alert_sound():
    def _play():
        try:
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Gagal memutar audio: {e}")
    threading.Thread(target=_play, daemon=True).start()

def wait_for_server(host="localhost", port=5000, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except (ConnectionRefusedError, socket.timeout):
            time.sleep(0.2)
    return False

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
                play_alert_sound()  # 🔊 Tambahkan ini
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

# def on_list():
#     os.system("start listapp.exe")

# def on_add():
#     os.system("start addapp.exe")

def on_exit(icon, item):
    icon.stop()
    os._exit(0)

def start_web():
    global server_process
    if server_process is None:
        if getattr(sys, 'frozen', False):
            exe_path = os.path.join(os.path.dirname(sys.executable), "applocker_server.exe")
        else:
            exe_path = os.path.join(os.path.dirname(__file__), "applocker_server.exe")

        if not os.path.exists(exe_path):
            show_alert(f"applocker_server.exe tidak ditemukan di:\n{exe_path}")
            return

        server_process = subprocess.Popen(exe_path)
        print("Web server started!")


def stop_web():
    global server_process
    if server_process is not None:
        server_process.terminate()
        server_process = None
        print("Web server stopped!")

def open_web():
    webbrowser.open("http://localhost:5000")

def show_about():
    result = ctypes.windll.user32.MessageBoxW(
        0,
        "AppLocker v1.0\n\nWebsite:\nhttps://github.com/yourusername/AppLocker",
        "About AppLocker",
        0x40 | 0x1  # 0x40 = Information icon, 0x1 = OK button
    )
    if result == 1:  # OK
        webbrowser.open("https://github.com/yourusername/AppLocker")

def update_menu(icon):
    menu_items = []

    if server_process is None:
        menu_items.append(item('Start Web Interface', lambda: start_web_and_update(icon)))
    else:
        menu_items.append(item('Stop Web Interface', lambda: stop_web_and_update(icon)))
        menu_items.append(item('Open Web Interface', open_web))

    menu_items.append(item('About', lambda: show_about()))
    menu_items.append(item('Exit', lambda: on_exit(icon, None)))

    icon.menu = pystray.Menu(*menu_items)
    icon.update_menu()

def start_web_and_update(icon):
    start_web()
    if wait_for_server():
        update_menu(icon)
        open_web()  # 👈 Langsung buka browser jika server berhasil
    else:
        show_alert("Gagal menjalankan Web Interface. Pastikan applocker_server.exe dapat berjalan dengan benar.")

def stop_web_and_update(icon):
    stop_web()
    update_menu(icon)


def tray_icon():
    icon = pystray.Icon("AppLocker")
    icon.icon = create_icon()
    icon.title = "AppLocker Running"
    update_menu(icon)
    icon.run()


if __name__ == "__main__":
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"locked_apps": []}, f)

    threading.Thread(target=background_loop, daemon=True).start()
    tray_icon()
