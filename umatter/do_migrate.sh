#!/bin/bash
set -e

echo Checking the db is running
db_check=$(docker ps | grep db)
if [ -z "$db_check" ]; then
   echo "Database not running"
   cd ..
   ./run_local_db.sh
   cd -
   sleep 2
fi

echo Checking the current directory
current_dir=$(pwd)
if [ "/Users/dhs/k_digital/final/server/umatter" != "$current_dir" ]; then
   cd ~/k_digital/final/server/umatter
fi

if ls ./{event,friend,user,nlp}/migrations/[0-9]*.py 1> /dev/null 2>&1; then
   echo Cleaning the existing migrations
   rm ./{event,friend,user,nlp}/migrations/[0-9]*.py
fi 

echo executing the user migrations
./manage.py makemigrations
./manage.py migrate --database=app_db
./manage.py migrate --database=nlp_db
./manage.py loaddata --database=app_db event_initial_data.json
./manage.py loaddata --database=nlp_db nlp_initial_data.json
