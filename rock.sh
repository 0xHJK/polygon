#!/bin/bash
# Author HJK 2016-11-21

REPO='hjk/ice'
NAME='ice'
DIR=$(pwd)/app
DOMAIN='ice.hjk.im'
PORT_HOST=6002
PORT_DOCKER=5000
ENV=$1

run()
{
    if [[ `docker ps -a | awk '{print $NF}' | grep "^${NAME}$"` ]]; then
        docker start ${NAME}
    elif [[ ${ENV} == 'dev' ]]; then
        docker run -it --name ${NAME} -e VIRTUAL_HOST='ice.local.com' -v ${DIR}:/lambda/app -p ${PORT_HOST}:${PORT_DOCKER} ${REPO} python3 ./app/main.py
    elif [[ ${ENV} == 'build' ]]; then
        docker run -d --name ${NAME} -e VIRTUAL_HOST=${DOMAIN} -v ${DIR}:/lambda/app -p ${PORT_HOST}:${PORT_DOCKER} ${REPO} python3 ./app/main.py
    fi
}

if [[ `docker images | awk '{print $1}' | grep "^${REPO}$"` ]]; then
    run
else
    docker build -t ${REPO} .
    run
fi

