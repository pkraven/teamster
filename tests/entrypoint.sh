#!/usr/bin/env bash
set -e

echo "$0"
echo "$1"

if [ "$1" = 'run' ]; then
    ./wait-for-it.sh postgres:5432
    ./wait-for-it.sh teamster:8080
    pytest --tb short -vv .
fi

if [ "$1" = 'sleep' ]; then
    sleep infinity
fi

exec "$@"