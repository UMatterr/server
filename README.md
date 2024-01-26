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
 ┣ 📜check_db.sh
 ┣ 📜clean_containers.sh
 ┣ 📜docker-compose-dev.yaml
 ┣ 📜docker-compose.yaml
 ┣ 📜entrypoint.sh
 ┣ 📜restart_web.sh
 ┗ 📜run_web.sh
```

### Before running django server, build python virtual environment

```bash
# python version: 3.11.7
# For, linux and macOS
# move to a folder you want to create the project
cd /path/to/a/project

# download this git repository
git clone https://github.com/UMatterr/server.git

# install the virtualenv library into the python which runs in global scope
# for example, /usr/local/bin/python3 or /opt/homebrew/bin/python3, etc.
python3 -m pip install --user -U virtualenv

# create a virtual environment
virtualenv {NAME}

# activate 
source /path/to/a/project/{NAME}/bin/activate
 
# move to the repository root folder
cd server

pip3 install -r ./config/django/requirements.txt
```

## 
## Run the db container

```shell
# the sh file will execute docker compose with docker-compose.yaml.
# the docker compose will build the containers.
# docker compose will run in the foreground.
# To stop the process, press ctrl+c
./run_local_db.sh
```

## Restart the web server and db

```shell
# If no docker containers run,
# the sh file will remove the containers and build the new containers
./restart_web.sh
```

## To attach on the db container

```shell
# the sh file will attach on the db container
# the password is in ./config/postgres/.env
./check_db.sh
```
