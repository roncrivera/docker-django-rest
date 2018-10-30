#!/bin/sh
set -e

if [ "$DJANGO_MANAGEPY_MIGRATE" == "true" ]; then
    python gatekeeper/manage.py migrate --noinput
fi

exec "$@"
