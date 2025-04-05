from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime, timedelta
import sys

def base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def data_path(filename):
    return os.path.join(base_dir(), filename)

app = Flask(__name__, template_folder=data_path("templates"))


# Contoh pakai
DB_FILE = data_path("locker_db.json")
# ICON_FILE = resource_path("AppLock_icon.ico")

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    data = load_db()
    return render_template("index.html", apps=data["locked_apps"])
@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    sort = request.args.get("sort", "desc")

    data = load_db()
    apps = data["locked_apps"]

    # Filter berdasarkan query
    if query:
        apps = [app for app in apps if query in app["path"].lower()]

    # Sort berdasarkan expire_time
    apps.sort(key=lambda x: datetime.strptime(x["expire_time"], "%Y-%m-%d %H:%M:%S"), reverse=(sort == "desc"))

    return render_template("index.html", apps=apps, query=query, sort=sort)


@app.route("/add", methods=["POST"])
def add_app():
    data = load_db()
    path = request.form["path"].replace("/", "\\")
    # jika ada " di path, hapus
    path = path.replace('"', '')
    # Jika bukan merupakan path .exe, maka tampilkan alert
    if not path.endswith(".exe"):
        return render_template("index.html", apps=data["locked_apps"], alert="Please enter a valid .exe file path.")
    # Jika path tidak ada, maka tampilkan alert
    if not os.path.exists(path):
        return render_template("index.html", apps=data["locked_apps"], alert="The specified path does not exist.")
    # Jika path bukan merupakan file, maka tampilkan alert
    if not os.path.isfile(path):
        return render_template("index.html", apps=data["locked_apps"], alert="The specified path is not a file.")
    # Cek jika path .exe ini sudah ada di database, maka tampilkan alert sudah ada
    for app in data["locked_apps"]:
        if app["path"] == path:
            return render_template("index.html", apps=data["locked_apps"], alert="Application already exists in the database.")
    days = int(request.form.get("days", 0))
    hours = int(request.form.get("hours", 0))
    minutes = int(request.form.get("minutes", 0))
    # Jika total waktu (days, hours, minutes) = 0, maka tampilkan alert
    if days <= 0 and hours <= 0 and minutes <= 0:
        return render_template("index.html", apps=data["locked_apps"], alert1="Please enter a valid time duration.")

    expire_time = datetime.now() + timedelta(days=days, hours=hours, minutes=minutes)

    data = load_db()
    data["locked_apps"].append({
        "path": path,
        "expire_time": expire_time.strftime("%Y-%m-%d %H:%M:%S")
    })
    save_db(data)
    return redirect("/")

@app.route("/delete/<int:index>", methods=["POST"])
def delete_app(index):
    data = load_db()
    if 0 <= index < len(data["locked_apps"]):
        data["locked_apps"].pop(index)
        save_db(data)
    return redirect("/")

if __name__ == "__main__":
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"locked_apps": []}, f)
    app.run(debug=True, port=5000)