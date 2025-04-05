import sys
import os
import subprocess
import psutil
import json

def base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def data_path(filename):
    return os.path.join(base_dir(), filename)

VERSION_FILE = data_path("version.json")

def main():
    if len(sys.argv) < 2:
        subprocess.Popen(["applocker_run.exe"])
        return

    command = sys.argv[1]

    if command == "server":
        subprocess.Popen(["applocker_server.exe"])
    elif command == "status":
        an_proc = False
        # Check the status of applocker_run and applocker_server
        for proc in psutil.process_iter(['name']):
            if proc.info["name"] == "applocker_run.exe":
                print("AppLocker Monitoring is running.")
                an_proc = True
            if proc.info["name"] == "applocker_server.exe":
                print("AppLocker Server is running.")
                an_proc = True
        if not an_proc:
            print("AppLocker is not running.")
    elif command == "help" or command == "-h":
        print("Usage: python locker.py [command]")
        print("Perintah: python locker.py [perintah]")
        print("Commands:")
        print("  server   Start the AppLocker server.")
        print("  status   Check the status of AppLocker.")
        print("  help     Show this help message.")
        print("Perintah:")
        print("  server   Mulai server AppLocker.")
        print("  status   Cek status AppLocker.")
        print("  help     Tampilkan pesan bantuan ini.")
    elif command == "version" or command == "-v":
        version_path = os.path.join(BASE_DIR, VERSION_FILE)
        with open(version_path, "r") as version_file:
            version_info = json.load(version_file)
            print(f"Version: {version_info['version']} | GitHub [{version_info['license']}]: {version_info['github']}")
    else:
        print("Unknown command.")
        print("Perintah tidak dikenal.")

if __name__ == "__main__":
    main()