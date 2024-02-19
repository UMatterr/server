docker rm server-web-1 server-db-1 server-nlp_db-1 && \
docker compose -f docker-compose-dev.yaml up --build
