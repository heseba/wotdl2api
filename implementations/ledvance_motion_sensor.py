from flask import jsonify
import requests
import json



MOTION_ENDPOINT = "http://10.0.1.200:80/api/E70AB7E7DB/sensors/2"
TEMPERATURE_ENDPOINT = "raspberrypi.local:80/api/E70AB7E7DB/sensors/3"


def get_motion_ledvance():
    response = requests.get(MOTION_ENDPOINT)
    json_data = json.loads(response.text)
    if json_data['state']['presence'] is True:
        return jsonify({'motion': 1, 'text': 'motion detected'})
    else:
        return jsonify({'motion': 0, 'text': 'no motion detected'})



def get_temperature_ledvance():
    response = requests.get(TEMPERATURE_ENDPOINT)
    json_data = json.loads(response.text)
    temperature = json_data['state']['temperature']
    return jsonify({'temperature': temperature, 'text': str(temperature), 'unit': 'Celsius'})