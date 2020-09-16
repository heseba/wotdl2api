#!/usr/bin/env bash
PORT=9000
MODULE=wot_api
API=api.yaml
GENERATOR_PATH=/usr/local/Cellar/openapi-generator/3.3.4/bin
PYTHON_PATH=/Users/mahda/.local/share/virtualenvs/wotdl2api-iHq_-KG6/bin
PI_PYTHON_PATH=/home/pi/.local/share/virtualenvs/wotdl2api-experiment-bAUvETzh/bin
TARGET=flask_out
PI_IP=10.0.1.200
DEPLOY_ON_PI=true

( set -x ; ${GENERATOR_PATH}/openapi-generator generate -i ${API} -g python-flask -o ${TARGET} -c config.json)
( set -x ; ${PYTHON_PATH}/python3 post_generation.py ${TARGET} ${MODULE} ${API})
( set -x ; cp hub.py ${TARGET}/${MODULE})
echo
if $DEPLOY_ON_PI ; then
    echo copying to raspberry
    echo
    ( set -x ; rsync -av --progress flask_out/* pi@${PI_IP}:/home/pi/wotdl2api-experiment)
    echo
    ( set -x ; ssh -t pi@${PI_IP} "lsof -ti tcp:9000 | xargs kill")
    echo
    echo running API on raspberry pi, open http://${PI_IP}:${PORT}/api/ui in your browser
    echo
    ( set -x ;ssh -t pi@${PI_IP} "cd /home/pi/wotdl2api-experiment ; exec ${PI_PYTHON_PATH}/python3 -m ${MODULE}")
else
    echo running API locally, open http://0.0.0.0:${PORT}/api/ui in your browser
    ( set -x ; cd ${TARGET};
    ${PYTHON_PATH}/python3 -m ${MODULE})
fi

