#!/bin/bash

cd /home/joaoalmeida/epi-creator-webapp
exec /home/joaoalmeida/epi-creator-webapp/epi-creator-venv/bin/gunicorn -w 1 --threads 2 -b 0.0.0.0:8383 run:app 

