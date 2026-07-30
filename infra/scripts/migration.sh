#!/bin/bash

ENV="--env-file /home/abhishek/prod/microservices-cdn-semver/.env"
COMPOSE_FILES="-f /home/abhishek/prod/microservices-cdn-semver/docker-compose.migrate.yml"

set -e  # stop on error

echo "=============================="
echo "Starting Database Migrations"
echo "=============================="

echo "Running Users Service migrations..."
docker compose $ENV $COMPOSE_FILES run --rm users_service_migrate

echo "Running Video Service migrations..."
docker compose $ENV $COMPOSE_FILES run --rm video_service_migrate

echo "Running Analytics Service migrations..."
docker compose $ENV $COMPOSE_FILES run --rm analytics_service_migrate

echo "=============================="
echo "All migrations completed successfully!"
echo "=============================="