FROM nginx:latest

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        bzip2 \
        ca-certificates \
        wget \
        xz-utils

RUN echo "Installing node.js" \
    && wget -O - https://nodejs.org/dist/v9.0.0/node-v9.0.0-linux-x64.tar.xz | tar -xJvf - -C /usr/local --strip-components=1 \
    && npm install -g yarn

COPY ./nginx.conf /etc/nginx/nginx.conf

ENV APP_ROOT /app
ENV WWW_USER www-data
ENV WWW_GROUP www-data
ENV STATIC_ROOT /var/www

WORKDIR ${APP_ROOT}

RUN [ -d ${APP_ROOT} ] && rm -rf ${APP_ROOT}

COPY ./app/build ${APP_ROOT}/build
COPY ./app/config ${APP_ROOT}/config
COPY ./app/src ${APP_ROOT}/src
COPY ./app/static ${APP_ROOT}/static
COPY ./app/.* ./app/*.html ./app/*.js ./app/*.json ./app/yarn.lock ${APP_ROOT}/

RUN cd ${APP_ROOT} \
    && yarn install --pure-lockfile \
    && yarn build \
    && install -d -m 0755 -o ${WWW_USER} -g ${WWW_GROUP} ${STATIC_ROOT} \
    && mv ${APP_ROOT}/dist/* ${STATIC_ROOT} \
    && chown -R ${WWW_USER}: ${STATIC_ROOT} \
    && yarn cache clean \
    && rm -rf ${APP_ROOT}/{dist,node_modules}
