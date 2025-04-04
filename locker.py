import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        subprocess.Popen(["runapp.exe"])
        return

    command = sys.argv[1]

    if command == "run":
        subprocess.Popen(["runapp.exe"])
    elif command == "list":
        subprocess.Popen(["listapp.exe"])
    elif command == "-p":
        subprocess.Popen(["addapp.exe"] + sys.argv[1:])
    elif command == "del":
        subprocess.Popen(["listapp.exe"])
    else:
        print("Perintah tidak dikenal.")

if __name__ == "__main__":
    main()