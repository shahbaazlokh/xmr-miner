copy "%~dp0..\..\..\src\*.py"
copy "%~dp0..\..\..\src\amd64\*.dll"
pyinstaller --onefile --icon xmr-miner.ico --version-file xmr-miner.txt --add-data cryptonight.dll;. -p "%~dp0." xmr-miner.py
pause
