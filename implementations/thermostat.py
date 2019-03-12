import time

import grovepi
from flask import Response
#from . import relay_heating

TEMP_SENSOR_PORT = 2
RELAY_PIN = 4
HYSTERESIS = 0.05

CONTROL_INTERVAL = 40

def get_temperature():
    [temp, humidity] = grovepi.dht(TEMP_SENSOR_PORT, 0)
    return temp

def activate_heating():
    print('thermostat on')
    grovepi.digitalWrite(RELAY_PIN, 1)

def deactivate_heating():
    print('thermostat off')
    grovepi.digitalWrite(RELAY_PIN, 0)



def thermostat_set(temp):
    current_temp = get_temperature()

    if current_temp > temp:
        return Response('current temperature above target temperature', status=500)

    while True:
        current_temp = get_temperature()
        print('Control Cycle current temperature %s' % current_temp)

        up_threshold = temp + HYSTERESIS * temp
        down_threshold = temp - HYSTERESIS * temp

        if current_temp < down_threshold:
            activate_heating()
        elif current_temp > up_threshold:
            deactivate_heating()
        else:
            pass

        time.sleep(CONTROL_INTERVAL)

    return Response('thermostat set to target temperature ' + temp, status=200)