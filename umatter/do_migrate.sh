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
   rm -v ./{event,friend,user,nlp}/migrations/[0-9]*.py
fi 

echo executing the user migrations
echo 1
./manage.py makemigrations user
echo 2
./manage.py migrate --database=app_db
echo 3
./manage.py makemigrations event friend
echo 4
./manage.py migrate --database=app_db
echo 5
./manage.py makemigrations nlp
echo 6
./manage.py migrate --database=nlp_db
echo 7
./manage.py loaddata --database=app_db event_initial_data.json
echo 8
./manage.py loaddata --database=nlp_db nlp_initial_data.json
