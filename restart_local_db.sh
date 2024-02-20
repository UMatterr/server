#!/bin/bash
set -e

docker kill db nlp_db

docker ps -a

docker run -d \
    --rm \
    -e POSTGRES_USER=root \
    --env-file config/postgres/.env-dev \
    -p 5433:5432 \
    --name db \
    postgres:15

docker run -d \
    --rm \
    -e POSTGRES_USER=root \
    --env-file config/postgres/.env-nlp-dev \
    -p 5434:5432 \
    --name nlp_db \
    postgres:15

docker ps
