#!/bin/bash

set -e

docker rm server-web-1 server-db-1

docker compose up --build
