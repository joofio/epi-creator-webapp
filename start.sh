# /home/joaoalmeida/gh_epi_creator_app/start.sh
#!/bin/bash

cd /home/joaoalmeida/gh_epi_creator_app
exec gunicorn -w 4 -b 0.0.0.0:8000 run:app \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log