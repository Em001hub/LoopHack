#!/bin/bash
echo "Setting up environment..."
cp .env.example .env
docker-compose up -d
