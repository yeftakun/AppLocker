python -m PyInstaller --onefile --name=applocker --icon=AppLock_icon.ico locker.py
python -m PyInstaller --onefile --noconsole --name=runapp --icon=AppLock_icon.ico --add-data "AppLock_icon.ico;." runapp.py
python -m PyInstaller --onefile --noconsole --name=listapp --windowed listapp.py
python -m PyInstaller --onefile --noconsole --name=addapp --windowed addapp.py