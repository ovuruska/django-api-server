#! /bin/bash
# Run the docker container
set -e
set -a; source .env; set +a
docker pull postgres
docker stop postgres-container || true
docker rm -f postgres-container || true
docker run --rm --name  postgres-container -e POSTGRES_DB=$DB_NAME -e POSTGRES_USER=$DB_USER  -e POSTGRES_PASSWORD=$DB_PASSWORD -p 5432:5432 -d postgres

BUILD_ARGS=$(cat .env | awk -F= '{printf("--build-arg %s=%s ", $1, $2)}')
docker build $BUILD_ARGS -t lambda-docker-image .

PARAMS=$(cat .env | awk -F= '{printf("ParameterKey=%s,ParameterValue=%s ", $1, $2)}')


sam build --use-container
sam local start-api --debug --parameter-overrides $PARAMS
