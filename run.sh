#!/bin/sh

# Parse flags
while getopts "d" flag; do
    case "${flag}" in
        d) DELETE_ENV=true ;;
    esac
done
shift $((OPTIND-1))

# Delete .env if flag is set
if [ "$DELETE_ENV" = true ]; then
    rm -f .env
    echo ".env file deleted"
fi

# Call the setup_env.sh script to ensure .env file exists
./setup_env.sh

# Default values
DEFAULT_APP_MODULE="app.main:app"
DEFAULT_HOST="localhost"
DEFAULT_PORT=8000

# Use provided arguments or default values
APP_MODULE=${1:-$DEFAULT_APP_MODULE}
HOST=${2:-$DEFAULT_HOST}
PORT=${3:-$DEFAULT_PORT}

# Run the Uvicorn server with the specified parameters
exec uvicorn --reload --host "$HOST" --port "$PORT" "$APP_MODULE"
