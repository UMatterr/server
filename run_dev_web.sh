#!/bin/bash
set -e

docker compose -f docker-compose-dev.yaml up --build

docker ps
