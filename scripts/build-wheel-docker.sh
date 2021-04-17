#!/bin/bash
pwd
docker build -t pybluemonday .
docker run --rm -it -d --name pybluemonday-temp pybluemonday sh
docker cp pybluemonday-temp:/root/dist dist
docker stop pybluemonday-temp