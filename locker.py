import sys
import subprocess
import psutil
import json

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
        with open("version.json", "r") as version_file:
            version_info = json.load(version_file)
            print(f"Version: {version_info['version']} | GitHub [{version_info['license']}]: {version_info['github']}")
    else:
        print("Unknown command.")
        print("Perintah tidak dikenal.")

if __name__ == "__main__":
    main()