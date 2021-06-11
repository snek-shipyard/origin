  
#!/bin/sh
set -e

# Test connection with psql and echo result to console.
until psql $DATABASE_URL -c '\l'; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - continuing"

# Make sure media is writable by uWSGI process.
#>&2 echo "correct ownership of media"
#chown -Rv 1000:2000 /code/media/

# Migrate database for deployment.
#if [ "$1" = '/venv/bin/uwsgi' ]; then
#    /venv/bin/python manage.py migrate --noinput
#fi

# Load Initial Data for deployment.
#if [ "x$DJANGO_LOAD_INITIAL_DATA" = 'xon' ]; then
#	/venv/bin/python manage.py load_initial_data
#fi

exec "$@"

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
