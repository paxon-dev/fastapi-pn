@echo off

REM Parse flags
set "DELETE_ENV="
if "%1"=="-d" (
    set "DELETE_ENV=true"
    shift
)

REM Delete .env if flag is set
if defined DELETE_ENV (
    del /f .env
    echo .env file deleted
)

REM Call the setup_env.bat script to ensure .env file exists
call setup_env.bat

REM Activate virtual environment
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Please run setup_venv.bat first.
    exit /b 1
)

REM Default values
set "DEFAULT_APP_MODULE=app.main:app"
set "DEFAULT_HOST=localhost"
set "DEFAULT_PORT=8000"

REM Use provided arguments or default values
set "APP_MODULE=%1"
if not defined APP_MODULE set "APP_MODULE=%DEFAULT_APP_MODULE%"

set "HOST=%2"
if not defined HOST set "HOST=%DEFAULT_HOST%"

set "PORT=%3"
if not defined PORT set "PORT=%DEFAULT_PORT%"

REM Run the Uvicorn server with the specified parameters
uvicorn --reload --host "%HOST%" --port "%PORT%" "%APP_MODULE%"

REM Deactivate virtual environment when done
deactivate
