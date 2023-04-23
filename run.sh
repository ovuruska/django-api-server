#! /bin/bash
# Run the docker container
set -e
set -a; source .env; set +a
docker pull postgres
docker stop postgres-container || true
docker rm -f postgres-container || true
docker run --rm --name  postgres-container -e POSTGRES_DB=$DB_NAME -e POSTGRES_USER=$DB_USER  -e POSTGRES_PASSWORD=$DB_PASSWORD -p 5432:5432 -d postgres

docker build -t lambda-docker-image .

sam build -t template.dev.yaml --use-container
sam local start-api -t template.dev.yaml --debug