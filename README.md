# Umatter Backend Source code

## Prerequisites

Please ask the config.tar.gz file from @HoonHenry

```shell
# unzip gz file
tar zxvf config.tar.gz
```

```bash
📦server
 ┣ 📂.github
 ┣ 📂config     # tar the gz file and pur the folder here
 ┃ ┣ 📂django
 ┃ ┃ ┣ 📜.env
 ┃ ┃ ┣ 📜.env-dev
 ┃ ┃ ┣ 📜.env-local
 ┃ ┃ ┗ 📜requirements.txt
 ┃ ┗ 📂postgres
 ┃ ┃ ┣ 📜.env
 ┃ ┃ ┗ 📜.env-dev
 ┣ 📂umatter
 ┣ 📜.gitignore
 ┣ 📜Dockerfile
 ┣ 📜README.md
 ┣ 📜check_dev_db.sh
 ┣ 📜clean_dev_containers.sh
 ┣ 📜docker-compose-dev.yaml
 ┣ 📜docker-compose.yaml
 ┣ 📜entrypoint.sh
 ┣ 📜restart_dev_web.sh
 ┗ 📜run_dev_web.sh
```

## Run the web server and db

```shell
# the sh file will execute docker compose with docker-compose.yaml.
# the docker compose will build the containers.
# docker compose will run in the foreground.
# To stop the process, press ctrl+c
./run_dev_web.sh
```

## Restart the web server and db

```shell
# If no docker containers run,
# the sh file will remove the containers and build the new containers
./restart_dev_web.sh
```

## To attach on the db container

```shell
# the sh file will attach on the db container
# the password is in ./config/postgres/.env
./check_dev_db.sh
```
