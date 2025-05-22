@echo off

REM Check if .venv directory exists and remove it
if exist .venv (
    echo Removing existing .venv directory...
    rmdir /s /q .venv
)

REM Create new virtual environment
echo Creating new virtual environment...
python -m venv .venv

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

echo Setup completed successfully!