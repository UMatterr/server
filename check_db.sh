#!/bin/bash

set -e

docker exec -it server-db-1 psql -U root -d umatter -W
