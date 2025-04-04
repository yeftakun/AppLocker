import tkinter as tk
from tkinter import messagebox
import json
import os

DB_FILE = "locker_db.json"

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def delete_item(index):
    data = load_db()
    removed = data["locked_apps"].pop(index)
    save_db(data)
    refresh_list()
    messagebox.showinfo("Info", f"{removed['path']} berhasil dihapus.")

def refresh_list():
    for widget in frame.winfo_children():
        widget.destroy()

    data = load_db()
    if not data["locked_apps"]:
        tk.Label(frame, text="Tidak ada aplikasi yang dikunci.").pack()
        return

    for idx, app in enumerate(data["locked_apps"]):
        row = tk.Frame(frame)
        row.pack(fill="x", padx=5, pady=2)
        tk.Label(row, text=f"{idx+1}. {app['path']} - hingga {app['expire_time']}", anchor="w", width=80).pack(side="left")
        tk.Button(row, text="Hapus", command=lambda i=idx: delete_item(i)).pack(side="right")

if __name__ == "__main__":
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"locked_apps": []}, f)

    root = tk.Tk()
    root.title("Daftar Aplikasi yang Dikunci")
    root.geometry("700x400")

    # Tombol Refresh di bagian atas
    top_frame = tk.Frame(root)
    top_frame.pack(fill="x", padx=10, pady=5)
    tk.Button(top_frame, text="🔄 Refresh", command=refresh_list, bg="#0099cc", fg="white").pack(side="right")

    # Frame untuk list aplikasi
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    refresh_list()
    root.mainloop()
