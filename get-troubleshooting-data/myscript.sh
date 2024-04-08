#!/bin/bash

tag=$1

docker build -t sagarkundral/my-python-app:${tag} -f Dockerfile-new .
docker push sagarkundral/my-python-app:${tag}


