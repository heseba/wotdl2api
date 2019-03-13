from flask import jsonify
import math
import grovepi

ltemp = 0.0
PORT = 4

def get_temperature(a=1):
    sensor = PORT
    [temp,humidity] = grovepi.dht(sensor, 0)
    if math.isnan(temp):
        temp = ltemp
    else:
        ltemp = temp
    return jsonify({'temperature': temp, 'text': str(temp), 'unit': 'Celsius'})

def get_humidity(a=1):
    sensor = PORT
    [temp,humidity] = grovepi.dht(sensor, 0)
    return jsonify({'humidity': humidity, 'text': str(humidity), 'unit': '%'})

