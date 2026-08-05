@echo off
title Sync dashboard pages (guide + architecture)
echo ==========================================
echo   Sync dashboard pages: Local + Server
echo ==========================================
echo.

set "KB=D:\code\knowledge-base"
set "MT=D:\code\math-inverse"
set "SRV=root@106.53.70.121"
set "DST=/opt/knowledge-base"

echo [1/3] Copy guide.html + architecture.html to math-inverse ...
copy /Y "%KB%\guide.html" "%MT%\guide.html" >nul
if errorlevel 1 goto FAIL_COPY
copy /Y "%KB%\architecture.html" "%MT%\architecture.html" >nul
if errorlevel 1 goto FAIL_COPY
echo   [OK]

echo [2/3] Upload both to server ...
scp -q "%KB%\guide.html" %SRV%:%DST%/guide.html 2>nul
if errorlevel 1 goto FAIL_SCP
scp -q "%KB%\architecture.html" %SRV%:%DST%/architecture.html 2>nul
if errorlevel 1 goto FAIL_SCP
echo   [OK]

echo [3/3] Verify on server ...
ssh -o BatchMode=yes %SRV% "ls -la %DST%/guide.html %DST%/architecture.html" 2>nul

echo.
echo ==========================================
echo   DONE. guide.html + architecture.html synced
echo     - localhost:5003  math-inverse
echo     - server 5003/5004
echo ==========================================
echo.
echo Note: Browser may cache old version. Ctrl+F5 to refresh.
pause
exit /b 0

:FAIL_COPY
echo   [FAIL] copy failed - check paths
pause
exit /b 1

:FAIL_SCP
echo   [FAIL] scp failed - check SSH key or server
pause
exit /b 1
