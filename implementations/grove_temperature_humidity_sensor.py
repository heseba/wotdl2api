from flask import jsonify
import math
import grovepi

PORT = 4

def get_temperature_grove():
    sensor = PORT
    [temp,humidity] = grovepi.dht(sensor, 0)
    if math.isnan(temp):
        temp = 0.0
    else:
        LTEMP = temp
    return jsonify({'temperature': temp, 'text': str(temp), 'unit': 'Celsius'})

def get_humidity():
    sensor = PORT
    [temp,humidity] = grovepi.dht(sensor, 0)
    return jsonify({'humidity': humidity, 'text': str(humidity), 'unit': '%'})
