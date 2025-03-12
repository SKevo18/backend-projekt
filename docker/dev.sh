#!/bin/bash

# set env
if [ -z "$DB_ROOT_PASSWORD" ]; then
    read -sp "'DB_ROOT_PASSWORD' = " DB_ROOT_PASSWORD
    echo
fi

if [ -z "$DB_PASSWORD" ]; then
    read -sp "'DB_PASSWORD' = " DB_PASSWORD
    echo
fi

export DB_ROOT_PASSWORD
export DB_PASSWORD

# run (default profile - HTTP only)
docker compose --profile="default" -f docker-compose.yaml up -d --build