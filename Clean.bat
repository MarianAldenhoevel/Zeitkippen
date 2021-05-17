@ECHO OFF

REM Remove old data and create a fresh data folder
RMDIR html\data /s /q
MKDIR html\data

DEL *.log /Q /F 
