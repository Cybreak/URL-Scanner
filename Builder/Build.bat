@echo off

:choice
set /P c=This is will build the exe file, confirm? (Y/N)
if /I "%c%" EQU "Y" goto :Yes
if /I "%c%" EQU "N" goto :No
goto :choice

:Yes
pip install -r requirements.txt
pyinstaller main.py --onefile
copy dist\main.exe .
del dist\main.exe
rmdir dist
del /s /q build
rmdir build\main\localpycs
rmdir build\main
rmdir build
del main.spec
ren .\main.exe URL-Scanner.exe
exit

:No
exit
