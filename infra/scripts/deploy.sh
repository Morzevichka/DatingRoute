#!/bin/bash

cd /opt/app
docker compose pull --quiet
docker compose up --detach

