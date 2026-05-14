@echo off
setlocal

set "ROOT=%~dp0"
for %%I in ("%ROOT%.venv\Scripts\python.exe") do set "PYTHON_EXE=%%~fI"
for %%I in ("%ROOT%implementation\mcp_server.py") do set "SERVER_FILE=%%~fI"
for %%I in ("%ROOT%inspector.config.json") do set "INSPECTOR_CONFIG=%%~fI"
for %%I in ("%ROOT%.npm-cache") do set "NPM_CONFIG_CACHE=%%~fI"

if not exist "%PYTHON_EXE%" (
  echo Python interpreter not found: %PYTHON_EXE%
  echo Run: python -m venv .venv ^&^& .\.venv\Scripts\pip.exe install fastmcp
  exit /b 1
)

if not exist "%SERVER_FILE%" (
  echo MCP server not found: %SERVER_FILE%
  exit /b 1
)

if not exist "%NPM_CONFIG_CACHE%" mkdir "%NPM_CONFIG_CACHE%"

echo Starting MCP Inspector for sqlite-lab...
echo Python: %PYTHON_EXE%
echo Server: %SERVER_FILE%
echo Config: %INSPECTOR_CONFIG%
echo.
echo If Inspector opens a browser, keep this terminal running.
echo.

cmd /c npx -y @modelcontextprotocol/inspector --config "%INSPECTOR_CONFIG%" --server sqlite-lab
