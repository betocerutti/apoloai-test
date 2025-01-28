#!/bin/bash

# Check if the database has been initialized
if [ ! -f "/app/db.sqlite3" ]; then
  echo "Initializing database..."
  python manage.py migrate
  python manage.py loaddata products_fixtures
fi

# Run the server
exec "$@"