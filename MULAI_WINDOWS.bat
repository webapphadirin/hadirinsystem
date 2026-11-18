@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto failed
start http://localhost:8000
.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000
pause
exit /b
:failed
echo Instalasi gagal. Periksa koneksi internet dan Python.
pause
