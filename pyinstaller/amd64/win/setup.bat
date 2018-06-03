copy "%~dp0..\..\..\src\*.py"
copy "%~dp0..\..\..\src\amd64\*.dll"
"C:\Program Files\Python36\Scripts\pyinstaller.exe" --onefile --icon xmr-miner.ico --version-file xmr-miner.txt --add-data cryptonight.dll;. -p "%~dp0." xmr-miner.py
pause
