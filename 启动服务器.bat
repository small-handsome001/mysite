@echo off
chcp 65001 >nul
title 本地服务器 - 关掉窗口即停止
cd /d "%~dp0"

echo.
echo   服务器启动中...
echo.
echo   浏览器访问：
echo      http://127.0.0.1:8123/                          网站首页
echo      http://127.0.0.1:8123/learning/10-width-test.html  第10课：四档宽度测试
echo      http://127.0.0.1:8123/learning/06-js.html        第6课：JS 练习
echo.
echo   改完代码不用重启，浏览器直接 F5。
echo   停止服务：关闭这个窗口。
echo.
echo   --------------------------------------------
echo.

python -m http.server 8123 --bind 127.0.0.1

echo.
echo   服务器已停止。
pause
