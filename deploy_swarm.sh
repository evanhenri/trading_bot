#!/usr/bin/env bash

set -eo pipefail

# -----

for cmd in container image volume system network; do
    docker ${cmd} prune -f &> /dev/null
done

find . -type d -name "tmpcharts" | xargs --no-run-if-empty rm -r
find . -type d -name "__pycache__" | xargs --no-run-if-empty rm -r

# -----

NAMESPACE=evanhenri
PKG_BASE=${NAMESPACE}/pkg-base:0.1.0
STREAM=${NAMESPACE}/stream:0.1.0
TRAIN=${NAMESPACE}/train:0.1.0

POSTGRES=postgres:latest
REDIS=redis:latest

pushd src

cat << EOF > ./Dockerfile.stream
FROM ${PKG_BASE}
CMD ["stream.py", "poloniex", "--patterns", "BTC_", "ETH_"]
EOF

docker build . -f Dockerfile.pkg_base -t ${PKG_BASE}
docker build . -f Dockerfile.stream -t ${STREAM}
docker build . -f Dockerfile.train -t ${TRAIN}

popd

# -----

GREEN='\033[0;32m'
PURPLE='\033[0;35m'
NC='\033[0m'

function executing() {
    echo -e "* ${PURPLE}$1${NC}";
}

function success() {
    echo -e "* ${GREEN}$1${NC}";
}

if ! $(docker swarm init &> /dev/null); then
    success "Swarm already initialized";
else
    executing "Initializing swarm"
    docker swarm init --advertise-addr <addr>;

    executing "Joining swarm"
    docker swarm join \
        --token <put-your-token-here> \
        192.168.0.114:2377;
fi;

if $(docker network ls | grep -q 'trader-network'); then
    success "'trader-network' already exists";
else
    executing "Creating 'trader-network' network"
    docker network create \
        -d overlay \
        trader-network;
fi;

if $(docker service ls | grep -q 'redis'); then
   success "'redis' service already exists";
else
   executing "Creating 'redis' service"
   docker service create \
       --name redis \
       --network trader-network \
       --replicas 1 \
       --detach \
       ${REDIS};
fi;

if $(docker service ls | grep -q 'postgres'); then
    success "'postgres' service already exists";
else
    executing "Creating 'postgres' service"
    docker service create \
        --name postgres \
        --network trader-network \
        --replicas 1 \
        --detach \
        ${POSTGRES};
fi;

if $(docker service ls | grep -q 'stream'); then
    success "'stream' service already exists";
else
    executing "Creating 'stream' service"
    docker service create \
        --name stream \
        --network trader-network \
        --replicas 1 \
        -e DB_HOST=postgres \
        -e DB_NAME=postgres \
        -e DB_PASS=example-password \
        -e DB_PORT=5432 \
        -e DB_USER=postgres \
        -e REDIS_HOST=redis \
        -e REDIS_PORT=6379 \
        --detach \
        ${STREAM};
fi;

if $(docker service ls | grep -q 'train'); then
   success "'train' service already exists";
else
   executing "Creating 'train' service"
   docker service create \
       --name train \
       --network trader-network \
       --replicas 1 \
       -e DB_HOST=postgres \
       -e DB_NAME=postgres \
       -e DB_PASS=example-password \
       -e DB_PORT=5432 \
       -e DB_USER=postgres \
       -e REDIS_HOST=redis \
       -e REDIS_PORT=6379 \
       --detach \
       ${TRAIN};
fi;

# docker stop
docker service scale trader=0

