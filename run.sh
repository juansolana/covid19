#!/bin/bash

# python manage.py migrate
# python manage.py collectstatic

./cloud_sql_proxy -instances=ethereal-yen-274604:us-central1:c19persons=tcp:5432 -credential_file=secrets/db-proxy.json &

# wait for the proxy to spin up
sleep 1

# Start the server
/usr/local/bin/gunicorn covidmap.wsgi:application -w 2 -b :$PORT