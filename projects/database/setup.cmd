@echo off
setlocal
set "TASK_MYSQL=mysql.exe"
if not "%~1"=="" set "TASK_MYSQL=%~1"
set "TASK_DBPORT=3306"
if not "%~2"=="" set "TASK_DBPORT=%~2"
for %%F in (sample exercise) do (
  "%TASK_MYSQL%" --default-character-set=utf8mb4 --user=root --password "--port=%TASK_DBPORT%" < "%~dp0%%F.sql"
  if errorlevel 1 exit /b 1
)
exit /b 0
