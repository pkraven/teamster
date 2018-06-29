#!/usr/bin/env bash
set -e

./wait-for-it.sh postgres:5432
./wait-for-it.sh teamster:8080

pytest --tb short -vv .
