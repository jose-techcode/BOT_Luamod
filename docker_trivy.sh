#!/bin/bash

# Stop in first error

set -e

# Root use proibithed

if [ "$EUID" -eq 0 ]; then
    echo "Don't use this script with root permission."
    exit 1
fi

# Building the Image

docker build -t bot_luamod .

# Scan the docker image with trivy tool (false positives are expected)

trivy image bot_luamod:latest

# Running the Container

docker run -it --name container_bot_luamod bot_luamod