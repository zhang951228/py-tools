@echo off

REM  JTM

setlocal enableextensions
cd /d %~dp0
if exist init.cmd pushd . && goto init
if exist ..\init.cmd pushd .. & goto init
goto :eof

:init
call init.cmd
title start Rocketmq Server
goto check

:check
sc query |find /i "%rocketmq_dir%" >nul 2>nul
if not errorlevel 1 (goto service_exist) else goto start_service

:service_exist
echo -----------------------------------------------------------------
echo Rocketmq 服务已经启动
echo -----------------------------------------------------------------
set /p input=是否继续?(Y/N)
if /i "%input%"=="y" goto start_service
echo.
goto end

:start_service
echo Starting Rocketmq, please wait ...

cd "%universitymarkignurl%\rocketmq\bin"
start mqnamesrv.cmd -c  ..\conf\namesrv.properties
cd "%universitymarkignurl%\rocketmq\bin"
start mqbroker.cmd -c ..\conf\broker.conf
echo.
goto end

:end
popd