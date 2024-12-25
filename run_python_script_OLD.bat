@echo off

REM Log file path
set LOG_PATH=E:\Projet\api_coingecko\logfile.log

REM Set the path to the Python executable
set PYTHON_PATH=E:\Python312\python.exe

REM Set the path to the Python script
set SCRIPT_PATH=E:\Projet\api_coingecko\coingecko.py

REM Execute the Python script and log the output
"%PYTHON_PATH%" "%SCRIPT_PATH%" >> "%LOG_PATH%" 2>&1


