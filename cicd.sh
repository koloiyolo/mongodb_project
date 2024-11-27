#!/bin/bash

# run using crontab

# set env variable as 
# export PROJECT_PATH="/path/to/your/project"

PROJECT_PATH=${PROJECT_PATH:-"/home/opc/mongodb_project"}

cd "$PROJECT_PATH" || { echo "Directory not found at $PROJECT_PATH! Exiting..."; exit 1; }

echo "Fetching updates from remote..."
git fetch

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse @{u})

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "Changes detected! Pulling updates..."
    
    git pull origin "$(git rev-parse --abbrev-ref HEAD)"
    BUILD_VERSION=$(git rev-parse --short HEAD)

    echo "Restarting Docker containers..."

    echo "Scaling app up..."
    BUILD_VERSION=$BUILD_VERSION docker compose up -d --scale app=2 --no-recreate app

    sleep 30

    OLD_CONTAINER=$(docker ps -q --filter "name=app" | head -n 1)

    echo "Scaling down the old app instance..."
    docker rm -f "$OLD_CONTAINER"

    echo "Scaling app down..."
    BUILD_VERSION=$BUILD_VERSION docker compose up -d --scale app=1 --no-recreate app

    echo "Update and restart complete!"
else
    echo "No changes detected. Everything is up to date."
fi
