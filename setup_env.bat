@echo off

REM Check if .env file exists
if not exist .env (
    REM Copy .env.sample to .env
    copy .env.sample .env
    echo .env file created from .env.sample
) else (
    echo Environment variables loaded from .env file
)