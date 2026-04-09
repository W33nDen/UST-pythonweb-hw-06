#!/bin/bash
# Helper script to start PostgreSQL Docker container
# Container name: my-postgres
# Password: mypassword
# Database: school

docker run --name my-postgres -p 5432:5432 \
    -e POSTGRES_PASSWORD=mypassword \
    -e POSTGRES_DB=school \
    -d postgres
