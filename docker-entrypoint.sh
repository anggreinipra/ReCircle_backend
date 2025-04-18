#!/bin/sh

if [ "$1" = "migrate" ]; then
  echo "🔁 Running migrations..."
  alembic upgrade head
  echo "✅ Migrations complete."
  exit 0
fi

echo "🚀 Starting Flask server..."
flask run --host=0.0.0.0 --port=5000