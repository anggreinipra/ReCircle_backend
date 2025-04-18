#!/bin/sh

# Run alembic migration
alembic upgrade head

# Run aplikasi Flask
flask run --host=0.0.0.0
