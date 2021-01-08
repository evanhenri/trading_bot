#!/usr/bin/env bash

set -eo pipefail

# -----

for cmd in container image volume system network; do
    docker ${cmd} prune -f
done

find . -type d -name "tmpcharts" | xargs --no-run-if-empty rm -r
find . -type d -name "__pycache__" | xargs --no-run-if-empty rm -r

# -----

NAMESPACE=evanhenri
PKG_BASE=${NAMESPACE}/pkg-base:latest
STREAM=${NAMESPACE}/stream:0.1.0

pushd src

cat << EOF > ./Dockerfile.stream
FROM ${PKG_BASE}
CMD ["stream.py", "poloniex", "--patterns", "BTC_", "ETH_"]
EOF

docker build . -f Dockerfile.pkg_base -t ${PKG_BASE}
docker build . -f Dockerfile.stream -t ${STREAM}

popd

for image in ${PKG_BASE} ${STREAM}; do
   docker push ${image}
done

# -----

./aws.py --setup-aws

find . -type f -exec chmod 0644 "{}" \;
find . -type d -exec chmod 0775 "{}" \;

pushd ./config/stream
helm dependency update .
helm install --dry-run --debug .
helm lint .
helm upgrade --force --install --recreate-pods stream .
popd

# -----

UI_VERSION=0.0.1
UI_IMAGE=${NAMESPACE}/ui
pushd ./interface/ui
docker build . -t ${UI_IMAGE}:${UI_VERSION}
docker push ${UI_IMAGE}:${UI_VERSION}
popd

API_VERSION=0.0.1
API_IMAGE=${NAMESPACE}/api
pushd ./interface/api
docker build . -t ${API_IMAGE}:${API_VERSION}
docker push ${API_IMAGE}:${API_VERSION}
popd

pushd ./config/interface
helm dependency update .
helm install --dry-run --debug .
helm lint .
helm upgrade --force --install --recreate-pods interface .
popd

# -----

INGRESS_CONTROLLER_URL=$(kubectl get svc -o wide | awk '/LoadBalancer/{print $4}')
./aws.py --route53-cname ${INGRESS_CONTROLLER_URL}

kubectl get pods -w
