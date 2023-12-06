set "universitymarkignurl=C:\myftp"
echo "start nginx"
cd "%universitymarkignurl%\nginx\nginxstartup.bat"
echo "%cd%"
@echo off
rem 当前bat的作用

echo ==================begin========================

cls
SET NGINX_PATH=C:
SET NGINX_DIR=C:\Program Files\nginx-1.19.7\
color 0a
TITLE Nginx 管理程序

CLS

ECHO.
ECHO.启动Nginx......
IF NOT EXIST "%NGINX_DIR%nginx.exe" ECHO "%NGINX_DIR%nginx.exe"不存在

%NGINX_PATH%

cd "%NGINX_DIR%"

IF EXIST "%NGINX_DIR%nginx.exe" (
    echo "start '' nginx.exe"
    start "" nginx.exe
)
ECHO.OK
