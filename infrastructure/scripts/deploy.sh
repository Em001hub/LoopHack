#!/bin/bash
echo "Deploying..."
git pull
docker-compose up -d --build
