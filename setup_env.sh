#!/bin/sh

# Check if .env file exists
if [ ! -f .env ]; then
    # Copy .env.sample to .env
    cp .env.sample .env
    echo ".env file created from .env.sample"
else
    echo "Environment variables loaded from .env file"
fi