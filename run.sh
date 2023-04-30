#! /bin/bash
# Run the docker container
set -e
set -a; source .env; set +a
docker pull postgres
echo "Waiting for postgres to start..."
docker run --name  postgres-container -e POSTGRES_DB=$DB_NAME -e POSTGRES_USER=$DB_USER  -e POSTGRES_PASSWORD=$DB_PASSWORD -p 5432:5432 -d postgres || true > /dev/null
docker start postgres-container || true > /dev/null

BUILD_ARGS=$(cat .env | awk -F= '{printf("--build-arg %s=%s ", $1, $2)}')
docker build $BUILD_ARGS -t lambda-docker-image .

docker run  --rm --entrypoint python lambda-docker-image manage.py collectstatic --noinput
docker run --rm --entrypoint python lambda-docker-image manage.py migrate
PARAMS=$(cat .env | awk -F= '{printf("ParameterKey=%s,ParameterValue=%s ", $1, $2)}')

sam build --use-container
sam local start-api --debug --parameter-overrides $PARAMS
