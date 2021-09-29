:: Put the Batch file in the following directory to get autostart capabilities
:: Win + R -> shell:startup
echo off

:start

:: Put the path to the main Python File
python Path/To/gui.py

echo Logger Closed, Restarting

goto start