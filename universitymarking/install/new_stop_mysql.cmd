@echo off

REM  JTM

setlocal enableextensions
cd /d %~dp0
if exist new_init.cmd pushd . && goto init
if exist ..\new_init.cmd pushd .. & goto init
goto :eof

:init
call new_init.cmd
title stop MySQL server
goto check

:check
sc query |find /i "%mysql_service_name%" >nul 2>nul
if not errorlevel 1 (goto stop_mysql_service) else goto mysql_service_not_exist

:mysql_service_not_exist
echo -----------------------------------------------------------------
echo MySQL 服务未启动
echo -----------------------------------------------------------------
set /p input=是否继续?(Y/N)
if /i "%input%"=="y" goto stop_mysql_service
echo.
goto end

:stop_mysql_service
echo Shutting down MySQL, please wait ...
net stop %mysql_service_name%
%mysql_dir%\mysqld.exe --remove %mysql_service_name%
rem sc delete %mysql_service_name%
echo.
goto end
:end
popd