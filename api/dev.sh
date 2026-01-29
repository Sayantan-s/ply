#!/bin/bash

# Load environment variables from .env.local if it exists
if [ -f .env.local ]; then
    # Use a loop to handle spaces in values correctly
    while IFS= read -r line || [ -n "$line" ]; do
        # Skip comments and empty lines
        [[ "$line" =~ ^[[:space:]]*#.*$ ]] && continue
        [[ "$line" =~ ^[[:space:]]*$ ]] && continue
        # Remove potential surrounding quotes from the value and export
        # This handles KEY="VALUE" or KEY='VALUE' or KEY=VALUE
        if [[ "$line" =~ ^([^=]+)=(.*)$ ]]; then
            key="${BASH_REMATCH[1]}"
            value="${BASH_REMATCH[2]}"
            # Remove leading/trailing quotes
            value="${value%\"}"
            value="${value#\"}"
            value="${value%\'}"
            value="${value#\'}"
            export "$key=$value"
        fi
    done < .env.local
fi

# Set default port if not specified in .env.local
PORT=${PORT:-7153}

# Use uvicorn from .venv if available
UVICORN=".venv/bin/uvicorn"
if [ ! -f "$UVICORN" ]; then
    UVICORN="uvicorn"
fi

echo "Starting ngrok on port $PORT..."
ngrok http $PORT > /dev/null 2>&1 &
NGROK_PID=$!

# Function to clean up ngrok on exit
cleanup() {
    echo ""
    echo "Shutting down ngrok (PID: $NGROK_PID)..."
    kill $NGROK_PID 2>/dev/null
    exit
}

# Trap signals to ensure cleanup occurs
trap cleanup SIGINT SIGTERM EXIT

echo "Starting FastAPI server on port $PORT..."
$UVICORN app.main:app --host 0.0.0.0 --port $PORT --reload
