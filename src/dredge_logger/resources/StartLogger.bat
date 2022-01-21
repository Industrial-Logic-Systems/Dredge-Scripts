:: Put the Batch file in the following directory to get autostart capabilities
:: Win + R -> shell:startup
echo off

:start

dredge_logger

echo Logger Closed, Restarting

goto start
