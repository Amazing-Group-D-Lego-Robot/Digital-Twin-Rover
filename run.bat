@echo off

start cmd.exe /c python main.py

waitfor SomethingThatIsNeverHappening /t 5 2>NUL

cd visualisation
start cmd.exe /c python visualisation.py