import time
import json
import psutil
import schedule
import threading
import ctypes
import os
import sys
import subprocess
import webbrowser
from datetime import datetime
from PIL import Image
import pystray
from pystray import MenuItem as item

# =====================[ Konstanta & Global Variable ]=====================

def base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def data_path(filename):
    return os.path.join(base_dir(), filename)

# Contoh pakai
DB_FILE = data_path("locker_db.json")
ICON_FILE = data_path("AppLock_icon.ico")

server_process = None

# =====================[ Fungsi Utilitas Database ]=====================

def init_db():
    """Inisialisasi file database jika belum ada."""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"locked_apps": []}, f)

def load_db():
    """Memuat data dari database JSON."""
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    """Menyimpan data ke database JSON."""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# =====================[ Fungsi Pemantauan dan Pemblokiran Aplikasi ]=====================

def clean_expired():
    """Menghapus aplikasi yang masa kuncinya sudah habis."""
    data = load_db()
    now = datetime.now()
    data["locked_apps"] = [
        app for app in data["locked_apps"]
        if datetime.strptime(app["expire_time"], "%Y-%m-%d %H:%M:%S") > now
    ]
    save_db(data)

def monitor_processes():
    try:
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
    except Exception as e:
        print(f"[ERROR] monitor_processes failed: {e}")


def background_loop():
    schedule.every(5).seconds.do(lambda: server_status_wrapper())
    schedule.every(5).seconds.do(monitor_processes)
    schedule.every(30).seconds.do(clean_expired)
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            print(f"[ERROR] Background loop crash: {e}")
        time.sleep(1)

def server_status_wrapper():
    try:
        cek_server_status()
    except Exception as e:
        print(f"[ERROR] cek_server_status failed: {e}")


# =====================[ Fungsi Tampilan & Interaksi Pengguna ]=====================

def show_alert(message):
    """Menampilkan pop-up alert Windows."""
    ctypes.windll.user32.MessageBoxW(0, message, "AppLocker Alert", 0x40 | 0x00001000)  # 0x10 = Stop icon, Close button only

def show_about():
    """Menampilkan informasi tentang aplikasi dan link Github."""
    with open(data_path("version.json"), "r") as version_file:
        version_info = json.load(version_file)
    result = ctypes.windll.user32.MessageBoxW(
        0,
        f"AppLocker {version_info['version']}\n\nGitHub [{version_info['license']}]\nGo to GitHub for more information.",
        "About AppLocker",
        0x40 | 0x1  # 0x40 = Information icon, 0x1 = OK button
    )
    if result == 1:  # Jika OK diklik
        webbrowser.open(f"{version_info['github']}")

def create_icon():
    """Membuat ikon untuk system tray."""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # Untuk PyInstaller
    else:
        base_path = os.path.dirname(__file__)

    icon_path = ICON_FILE  # Sudah full path dari atas

    if not os.path.exists(icon_path):
        raise FileNotFoundError(f"Icon file not found: {icon_path}")

    icon = Image.open(icon_path)
    icon = icon.resize((64, 64), Image.Resampling.LANCZOS)
    return icon

# =====================[ Fungsi Web Server ]=====================

def start_web():
    """Menjalankan server Flask jika belum berjalan."""
    global server_process
    # Cek apakah server sudah berjalan
    server_process = cek_server_status()
    if server_process is not None:
        show_alert("Web interface sudah berjalan!")
        return
    # Jika server belum berjalan, jalankan server
    else:
        exe_path = data_path("applocker_server.exe")

        if not os.path.exists(exe_path):
            show_alert(f"applocker_server.exe tidak ditemukan di:\n{exe_path}")
            return

        server_process = subprocess.Popen(exe_path)
        show_alert("Web interface berhasil dijalankan di http://localhost:5000")

def stop_web():
    global server_process
    # Melakukan looping stop untuk memastikan server berhenti, dengan kondisi cek_server_status
    
    max_retry = 5
    retry = 0
    while cek_server_status() is not None and retry < max_retry:
        retry += 1
        time.sleep(1)
        if server_process:
            try:
                server_process.terminate()
                print("Web server stopped!")
            except Exception as e:
                print(f"❌ Gagal menghentikan server: {e}")
            finally:
                server_process = cek_server_status()



def open_web():
    """Membuka antarmuka web di browser default."""
    webbrowser.open("http://localhost:5000")

# def cek_server_status():
#     """Mengembalikan objek proses server jika sedang berjalan, jika tidak return None."""
#     for proc in psutil.process_iter(attrs=["pid", "name"]):
#         if proc.info["name"] == "applocker_server.exe":
#             return proc
#     return None

def cek_server_status():
    """Mengembalikan objek proses server jika sedang berjalan, jika tidak return None."""
    expected_path = os.path.normcase(os.path.abspath(data_path("applocker_server.exe")))

    for proc in psutil.process_iter(attrs=["pid", "name", "exe"]):
        try:
            exe_path = proc.info.get("exe")
            if exe_path:
                exe_path = os.path.normcase(os.path.abspath(exe_path))
                if exe_path == expected_path:
                    return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        except Exception as e:
            print(f"[WARN] cek_server_status: {e}")
            continue
    return None



# =====================[ Fungsi Menu Dinamis System Tray ]=====================

def on_exit(icon, item):
    """Keluar dari aplikasi AppLocker."""
    stop_web()
    icon.stop()
    os._exit(0)

def update_menu(icon):
    """Memperbarui menu system tray sesuai status server."""
    menu_items = []

    # Cek status server
    global server_process
    if cek_server_status() is None:
        server_process = None
    else:
        server_process = cek_server_status()

    if server_process is None:
        menu_items.append(item('Start Web Interface', lambda: start_web_and_update(icon)))
    else:
        menu_items.append(item('Stop Web Interface', lambda: stop_web_and_update(icon)))
        menu_items.append(item('Open Web Interface', open_web))

    menu_items.append(item('About', show_about))
    menu_items.append(item('Exit', lambda: on_exit(icon, None)))

    icon.menu = pystray.Menu(*menu_items)
    icon.update_menu()

def start_web_and_update(icon):
    """Start server dan perbarui menu tray."""
    start_web()
    time.sleep(1)
    update_menu(icon)

def stop_web_and_update(icon):
    """Stop server dan perbarui menu tray."""
    stop_web()
    update_menu(icon)

# =====================[ Main System Tray Logic ]=====================

def tray_icon():
    """Menampilkan icon di system tray dengan menu dinamis."""
    icon = pystray.Icon("AppLocker")
    icon.icon = create_icon()
    icon.title = "AppLocker Running"
    update_menu(icon)
    icon.run()

# =====================[ Entry Point ]=====================

if __name__ == "__main__":
    init_db()
    threading.Thread(target=background_loop, daemon=True).start()
    tray_icon()
