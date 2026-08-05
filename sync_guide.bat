@echo off
title Sync guide.html (Dashboard)
echo ==========================================
echo   Sync guide.html: Local + Server
echo ==========================================
echo.

set "SRC=D:\code\knowledge-base\guide.html"
set "DST_MT=D:\code\math-inverse\guide.html"
set "SRV=root@106.53.70.121"
set "DST_SRV=/opt/knowledge-base/guide.html"

echo [1/3] Copy to math-inverse\guide.html ...
copy /Y "%SRC%" "%DST_MT%" >nul
if errorlevel 1 goto FAIL_COPY
echo   [OK]

echo [2/3] Upload to %SRV% ...
scp -q "%SRC%" %SRV%:%DST_SRV% 2>nul
if errorlevel 1 goto FAIL_SCP
echo   [OK]

echo [3/3] Verify on server ...
ssh -o BatchMode=yes %SRV% "ls -la %DST_SRV%" 2>nul

echo.
echo ==========================================
echo   DONE. All aligned:
echo     - localhost:5003  math-inverse
echo     - knowledge-base  source
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
