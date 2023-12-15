@echo off

REM  JTM

setlocal enableextensions
cd /d %~dp0
if exist new_init.cmd pushd . && goto init
if exist ..\new_init.cmd pushd .. & goto init
goto :eof

:init
call new_init.cmd
title start MySQL server
goto check

:check
sc query |find /i "%mysql_service_name%" >nul 2>nul
if not errorlevel 1 (goto mysql_service_exist) else goto start_mysql_service

:mysql_service_exist
echo -----------------------------------------------------------------
echo MySQL 服务已经启动
echo -----------------------------------------------------------------
set /p input=是否继续?(Y/N)
if /i "%input%"=="y" goto start_mysql_service
echo.
goto end

:start_mysql_service
echo Starting MySQL, please wait ...
%mysql_dir%\mysqld.exe --install %mysql_service_name%
net start %mysql_service_name%
echo.
goto end

:end
popd