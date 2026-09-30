@echo off
cd /d "%~dp0"
if exist JSON-Compare.exe (JSON-Compare.exe) else (where py >nul 2>nul
if not errorlevel 1 (py -3 portable_json.py) else (python portable_json.py))
pause
