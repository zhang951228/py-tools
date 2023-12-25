@echo off

REM  JTM

setlocal enableextensions
cd /d %~dp0
if exist init.cmd pushd . && goto init
if exist ..\init.cmd pushd .. & goto init
goto :eof

:init
call init.cmd
title start Tomcat Server
goto check

:check
sc query |find /i "%tomcat_dir%" >nul 2>nul
if not errorlevel 1 (goto service_exist) else goto start_service

:service_exist
echo -----------------------------------------------------------------
echo Tomcat 服务已经启动
echo -----------------------------------------------------------------
set /p input=是否继续?(Y/N)
if /i "%input%"=="y" goto start_service
echo.
goto end

:start_service
echo Starting Tomcat, please wait ...

cd "%universitymarkignurl%\mysql\bin"
net start mysql

echo.
goto end

:end
popd