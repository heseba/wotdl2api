from flask import jsonify
import grovepi
from .. import hub

def init():
    hub.PERSISTENCE['SPEED'] = 0
    return

def fan_set(body):
    target_speed = body['target_speed']
    speed = int(target_speed)
    if(speed < 0 or speed > 250):
        return jsonify({ "error": "speed " + str(speed) + " out of range (" + str(0) + "-" + str(250) + ")", 'speed': hub.PERSISTENCE['SPEED'] }), 400
    fan_port = 5
    grovepi.pinMode(fan_port,"OUTPUT")
    grovepi.analogWrite(fan_port,speed)
    hub.PERSISTENCE['SPEED'] = speed
    return jsonify({'speed': speed})

def increase_fan_speed(body):
    increment = body['increment']
    fan_port = 5
    speed = hub.PERSISTENCE['SPEED']
    speed += int(increment)
    if(speed < 0 or speed > 250):
        return jsonify({ "error": "speed " + str(speed) + " out of range (" + str(0) + "-" + str(250) + ")", 'speed': hub.PERSISTENCE['SPEED'] }), 400
    grovepi.pinMode(fan_port,"OUTPUT")
    print(speed)
    grovepi.analogWrite(fan_port,speed)
    hub.PERSISTENCE['SPEED'] = speed
    return jsonify({'speed': speed})


def decrease_fan_speed(body):
    decrement = body['decrement']
    fan_port = 5
    speed = hub.PERSISTENCE['SPEED']
    speed -= int(decrement)
    if(speed < 0 or speed > 250):
        return jsonify({ "error": "speed " + str(speed) + " out of range (" + str(0) + "-" + str(250) + ")", 'speed': hub.PERSISTENCE['SPEED'] }), 400
    grovepi.analogWrite(fan_port,speed)
    hub.PERSISTENCE['SPEED'] = speed
    return jsonify({'speed': speed})

def fan_turn_off(a=1):
    fan_port = 5
    grovepi.pinMode(fan_port,"OUTPUT")
    speed = 0
    grovepi.analogWrite(fan_port, speed)
    hub.PERSISTENCE['SPEED'] = speed
    return jsonify({'status': 'OFF'})


