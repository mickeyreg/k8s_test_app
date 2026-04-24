#!/bin/sh
envsubst '${POD_IP} ${NODE_IP} ${NODE_NAME}' \
    < /usr/share/nginx/html/index.html.template \
    > /usr/share/nginx/html/index.html

