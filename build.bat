@echo off
echo Building AppLocker...

REM === Bersihkan build sebelumnya (opsional)
echo Deleting previous build files...
if exist dist rmdir /s /q dist
if exist build_temp rmdir /s /q build_temp
echo create dist folder if not exist dist
if not exist dist mkdir dist
echo Copying additional files...
echo Copying icon file to dist folder...
copy AppLock_icon.ico dist\
copy version.json dist\
copy locker_db.json dist\
xcopy templates dist\templates\ /E /I /Y

echo Starting build process...

REM === Build locker.py
python -m PyInstaller --onefile --name=applocker --icon=AppLock_icon.ico ^
--distpath dist ^
locker.py

REM === Build runapp.py
python -m PyInstaller --onefile --noconsole --name=applocker_run --icon=AppLock_icon.ico ^
--distpath dist ^
runapp.py

REM === Build server.py
python -m PyInstaller --onefile --noconsole --name=applocker_server ^
--distpath dist ^
server.py

echo ✅ Build selesai! Semua file berada di folder 'dist/'
pause
