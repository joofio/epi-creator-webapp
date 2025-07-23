#!/bin/bash

cd /mnt/sandboxes/epi-creator-webapp
exec /mnt/sandboxes/epi-creator-webapp/epi-creator-venv/bin/gunicorn -w 1 --threads 2 -b 0.0.0.0:8383 run:app 

