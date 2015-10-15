#!/usr/bin/env bash

DB_NAME=dominion

mysql -u root -e "DROP DATABASE IF EXISTS $DB_NAME;"
mysql -u root -e "CREATE DATABASE $DB_NAME;"

./manage.py makemigrations
./manage.py migrate