docker run -d --rm -e POSTGRES_USER=root --env-file config/postgres/.env -p 5432:5432 --name db postgres:15 && \
docker ps
