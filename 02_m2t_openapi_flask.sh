#!/usr/bin/env bash
PORT=9000
MODULE=wot_api
API=api.yaml
GENERATOR_PATH=/usr/local/Cellar/openapi-generator/3.3.4/bin
PYTHON_PATH=/Users/mahda/.local/share/virtualenvs/wotdl2api-iHq_-KG6/bin
PI_PYTHON_PATH=/home/pi/.local/share/virtualenvs/wotdl2api-experiment-bAUvETzh/bin
TARGET=flask_out
PI_IP=10.0.1.200

( set -x ; ${GENERATOR_PATH}/openapi-generator generate -i ${API} -g python-flask -o ${TARGET} -c config.json)
( set -x ; ${PYTHON_PATH}/python3 post_generation.py ${TARGET} ${MODULE} ${API})
( set -x ; cp hub.py ${TARGET}/${MODULE})
echo
echo copying to raspberry
echo
#add for pi
( set -x ; rsync -av --progress flask_out/* pi@${PI_IP}:/home/pi/wotdl2api-experiment)
echo
#echo running API, open http://0.0.0.0:${PORT}/api/ui in your browser
#add for pi
echo running API, open http://${PI_IP}:${PORT}/api/ui in your browser
echo
( set -x ; ssh -t pi@${PI_IP} "lsof -ti tcp:9000 | xargs kill")
echo
#add for pi
( set -x ;ssh -t pi@${PI_IP} "cd /home/pi/wotdl2api-experiment ; exec ${PI_PYTHON_PATH}/python3 -m ${MODULE}")
#( set -x ; cd ${TARGET}; ${PYTHON_PATH}/python3 -m ${MODULE})
