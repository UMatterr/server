#!/bin/bash
set -e

docker kill db nlp_db

docker ps -a
