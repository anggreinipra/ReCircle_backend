#!/bin/sh

if [ "$1" = "migrate" ]; then
  alembic upgrade head
else
  alembic upgrade head
  flask run --host=0.0.0.0
fi
