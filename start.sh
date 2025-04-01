# /home/joaoalmeida/gh_epi_creator_app/start.sh
#!/bin/bash

cd /home/joaoalmeida/gh_epi_creator_app
exec /home/joaoalmeida/epi-creator-webapp/epi-creator-venv/bin/gunicorn -w 1 --threads 2 -b 0.0.0.0:8383 run:app 

