#!/bin/bash
set -e

docker rm server-web-1 server-db-1

dockr rmi server-web

docker compose -f docker-compose-dev.yaml up --build

docker ps
