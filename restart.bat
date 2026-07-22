@echo off
echo 正在重启知识库服务...
wmic process where "commandline like '%%knowledge-base%%server%%'" delete >nul 2>&1
timeout /t 1 >nul
start /B "" "D:\dev\sdk\Python\Python314\python.exe" "d:\code\knowledge-base\server.py"
echo 知识库已启动 → http://localhost:5004/
