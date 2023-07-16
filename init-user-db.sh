#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "postgres" <<-EOSQL
    CREATE ROLE "$POSTGRES_USER" WITH LOGIN PASSWORD '$POSTGRES_PASSWORD';
    ALTER ROLE "$POSTGRES_USER" CREATEDB;
    CREATE DATABASE "$POSTGRES_DB";
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO "$POSTGRES_USER";
EOSQL