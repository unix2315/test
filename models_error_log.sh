#!/bin/bash

FILENAME=$(date +"%Y-%m-%d")

if [ ! -d "models_log" ]; then
    mkdir models_log
fi

python manage.py models_count 2>> models_log/${FILENAME}.dat
