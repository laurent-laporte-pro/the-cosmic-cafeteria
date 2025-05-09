#!/bin/sh

# Wait for database to be ready
echo "Waiting for database..."
while ! pg_isready -h tcc-db -p 5432 -U user -d cosmic_cafeteria
do
  echo "Waiting for database connection..."
  sleep 2
done
echo "Database is ready!"

# Apply database migrations
echo "Applying database migrations..."
flask db upgrade
echo "Migrations applied successfully!"

# Start the application
echo "Starting the Flask application..."
exec flask run
