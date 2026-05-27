#!/bin/sh
export LOG_TO_FILES=1
gunicorn  run:app -w 2 --threads 2 -b 0.0.0.0:80 --access-logfile logs/access.log --error-logfile logs/error.log