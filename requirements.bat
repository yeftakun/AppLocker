@echo off
echo Installing exact versions of Python dependencies...

REM Install each module with specified version
pip install psutil==6.0.0
pip install schedule==1.2.2
pip install pystray==0.19.5
pip install pillow==11.1.0

echo.
echo === Installed Versions ===
for %%i in (psutil schedule pystray pillow) do (
    echo %%i:
    pip show %%i | findstr /R "^Version:"
    echo.
)

echo Requirements installed successfully.
echo If you want to run AppLocker at any directory, you must set to the system environment variable PATH the path to the AppLocker/dist directory.
pause
