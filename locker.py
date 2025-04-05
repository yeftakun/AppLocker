import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        subprocess.Popen(["applocker_run.exe"])
        return

    command = sys.argv[1]

    if command == "server":
        subprocess.Popen(["applocker_server.exe"])
    elif command == "-p":
        subprocess.Popen(["addapp.exe"] + sys.argv[1:])
    else:
        print("Perintah tidak dikenal.")

if __name__ == "__main__":
    main()