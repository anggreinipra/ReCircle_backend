#!/bin/sh

# Debug print env yang penting (opsional tapi berguna)
echo "📦 DATABASE_URL: $DATABASE_URL"
echo "📦 FLASK_ENV: $FLASK_ENV"

# Cek kalau variabel penting gak ada
if [ -z "$DATABASE_URL" ]; then
  echo "❌ ERROR: DATABASE_URL is not set. Exiting..."
  exit 1
fi

# Handle arg khusus: `migrate`
if [ "$1" = "migrate" ]; then
  echo "🔁 Running Alembic migrations..."
  alembic upgrade head
  echo "✅ Migrations complete."
  exit 0
fi

# Jalankan Alembic sebelum start server
echo "🔁 Running Alembic migrations..."
alembic upgrade head || {
  echo "❌ Alembic migration failed"
  exit 1
}

# Start Flask
echo "🚀 Starting Flask server..."
exec flask run --host=0.0.0.0 --port=5000
