@echo off
echo Installing required packages...

pip install psutil==6.0.0
pip install Pillow==11.1.0
pip install flask==3.0.3

:: Untuk pystray dan schedule, install tanpa versi karena versinya tidak terdeteksi
pip install pystray
pip install schedule

echo Done.
pause
