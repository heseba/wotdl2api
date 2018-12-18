#!/usr/bin/env bash
PORT=9000
MODULE=wot_api
API=api.yaml
GENERATOR_PATH=/usr/local/Cellar/openapi-generator/3.3.4/bin
PYTHON_PATH=/Users/sebastian/virtualenvs/python3/bin
TARGET=flask_out
${GENERATOR_PATH}/openapi-generator generate -i ${API} -g python-flask -o ${TARGET} -c config.json
#sed -i '' '1s;^;import wot2api;' "${TARGET}/${MODULE}/controllers/default_controller.py"
cd ${TARGET}
echo
echo running API, open http://0.0.0.0:${PORT}/api/ui in your browser
echo
#${PYTHON_PATH}/python -m ${MODULE}