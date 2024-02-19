#!/bin/bash
set -e

docker run -d \
    --rm \
    --env-file config/postgres/.env-dev \
    -p 5432:5432 \
    --name db \
    postgres:15

docker run -d \
    --rm \
    --env-file config/postgres/.env-nlp-dev \
    -p 5433:5432 \
    --name nlp_db \
    postgres:15

docker ps
