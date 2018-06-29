#!/usr/bin/env bash
set -e

./wait-for-it.sh postgres:5432
export PYTHONPATH=/app/teamster
alembic -c alembic/alembic.ini upgrade head

echo "$0"
echo "$1"

if [ "$1" = 'run' ]; then
    python3.6 -m aiohttp.web -H 0.0.0.0 -P $2 app:start
fi

if [ "$1" = 'sleep' ]; then
    sleep infinity
fi

exec "$@"
