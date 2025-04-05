echo off
echo Installing Python dependencies...
python -m PyInstaller --onefile --name=applocker --icon=AppLock_icon.ico locker.py
python -m PyInstaller --onefile --noconsole --name=applocker_run --icon=AppLock_icon.ico --add-data "AppLock_icon.ico;." --add-data "alert.wav;." runapp.py
python -m PyInstaller --noconfirm --add-data "templates;templates" --name=applocker_server --noconsole --onefile server.py
echo Installing complete...
pause