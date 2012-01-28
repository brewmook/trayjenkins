@echo off
setlocal
set PYTHONPATH=%cd%/submodules/pyjenkins;%PYTHONPATH%
echo %PYTHONPATH%
python trayjenkins.py %*
