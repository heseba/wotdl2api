#!/usr/bin/env bash
PORT=9000
MODULE=wot_api
API=api.yaml
GENERATOR_PATH=/usr/local/Cellar/openapi-generator/3.3.4/bin
PYTHON_PATH=~/virtualenvs/WotDL2API_NEW/bin
TARGET=flask_out

( set -x ; ${GENERATOR_PATH}/openapi-generator generate -i ${API} -g python-flask -o ${TARGET} -c config.json)
( set -x ; ${PYTHON_PATH}/python3 post_generation.py ${TARGET} ${MODULE} ${API})
( set -x ; cp hub.py ${TARGET}/${MODULE})
echo
echo running API, open http://0.0.0.0:${PORT}/api/ui in your browser
echo
#( set -x ; cd ${TARGET}; ${PYTHON_PATH}/python3 -m ${MODULE})