@echo off
REM DaVinci Resolve Environment Setup Script
REM Based on official Blackmagic Design documentation
REM https://resolvedevdoc.readthedocs.io/en/latest/readme_resolveapi.html

echo Setting up DaVinci Resolve API environment variables...

REM Set the required environment variables for Windows
set "RESOLVE_SCRIPT_API=%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
set "RESOLVE_SCRIPT_LIB=C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
set "PYTHONPATH=%PYTHONPATH%;%RESOLVE_SCRIPT_API%\Modules\"

echo RESOLVE_SCRIPT_API=%RESOLVE_SCRIPT_API%
echo RESOLVE_SCRIPT_LIB=%RESOLVE_SCRIPT_LIB%
echo PYTHONPATH includes: %RESOLVE_SCRIPT_API%\Modules\

echo.
echo Environment variables set for current session.
echo To make permanent, add these to your system environment variables.
echo.
echo Now you can run: uv run test_basic_connection.py
pause 