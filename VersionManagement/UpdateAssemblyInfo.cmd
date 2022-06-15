@echo off
start /B /WAIT "%~dp0" WindowsBuildVersionGenerator.exe
start /B /WAIT "%~dp0" WindowsAssemblyInfoVersionUpdater.exe "%1"
exit /b 0
