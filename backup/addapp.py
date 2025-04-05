import json
import os
import sys
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

DB_FILE = "locker_db.json"

# def get_base_dir():
#     if getattr(sys, 'frozen', False):
#         return os.path.dirname(sys.executable)
#     else:
#         return os.path.dirname(os.path.abspath(__file__))

# BASE_DIR = get_base_dir()
# DB_FILE = os.path.join(BASE_DIR, "locker_db.json")

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

def browse_file():
    filepath = filedialog.askopenfilename(
        title="Pilih aplikasi (.exe)",
        filetypes=[("Executable files", "*.exe")]
    )
    if filepath:
        exe_path_var.set(filepath)

def block_app():
    path = exe_path_var.get()
    # Jika path "/" ubah jadi "\\"
    path = path.replace("/", "\\")
    try:
        days = int(days_var.get())
        hours = int(hours_var.get())
        minutes = int(minutes_var.get())
    except ValueError:
        messagebox.showerror("Input Error", "Masukkan angka valid untuk durasi!")
        return

    if not path or not os.path.isfile(path):
        messagebox.showerror("File Error", "Pilih file aplikasi (.exe) yang valid!")
        return

    expire_time = datetime.now() + timedelta(days=days, hours=hours, minutes=minutes)

    try:
        data = load_db()
    except:
        data = {"locked_apps": []}

    data["locked_apps"].append({
        "path": path,
        "expire_time": expire_time.strftime("%Y-%m-%d %H:%M:%S")
    })
    save_db(data)

    messagebox.showinfo("Sukses", f"✅ Aplikasi dikunci hingga {expire_time.strftime('%Y-%m-%d %H:%M:%S')}")
    root.destroy()

# Pastikan DB ada
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({"locked_apps": []}, f)

# GUI
root = tk.Tk()
root.title("Tambah Aplikasi ke Lock List")
root.geometry("500x250")
root.resizable(False, False)

exe_path_var = tk.StringVar()
days_var = tk.StringVar(value="0")
hours_var = tk.StringVar(value="0")
minutes_var = tk.StringVar(value="0")

tk.Label(root, text="Pilih file .exe aplikasi yang ingin dikunci:").pack(pady=5)
frame_path = tk.Frame(root)
frame_path.pack(padx=10, fill="x")

entry_path = tk.Entry(frame_path, textvariable=exe_path_var, width=55)
entry_path.pack(side="left", fill="x", expand=True)
tk.Button(frame_path, text="Browse", command=browse_file).pack(side="left", padx=5)

frame_time = tk.Frame(root)
frame_time.pack(pady=10)

tk.Label(frame_time, text="Hari:").grid(row=0, column=0)
tk.Entry(frame_time, width=5, textvariable=days_var).grid(row=0, column=1)

tk.Label(frame_time, text="Jam:").grid(row=0, column=2, padx=(10, 0))
tk.Entry(frame_time, width=5, textvariable=hours_var).grid(row=0, column=3)

tk.Label(frame_time, text="Menit:").grid(row=0, column=4, padx=(10, 0))
tk.Entry(frame_time, width=5, textvariable=minutes_var).grid(row=0, column=5)

tk.Button(root, text="🔒 Block App", command=block_app, width=20, bg="#cc0000", fg="white").pack(pady=20)

root.mainloop()
