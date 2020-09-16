import time
import grovepi
from flask import Response
from .heating_thread import HeatingThread
from .. import hub

def init():
    if not 'WORKER' in hub.PERSISTENCE:
        hub.PERSISTENCE['WORKER'] = HeatingThread()
    return

def activate_heating(power):
    #power = body['power']
    if power < .2 or power > 1:
        raise ValueError
    else:
        grovepi.pinMode(8, 'OUTPUT')
        on_interval = power * 20
        off_interval = (1-power) * 20

        hub.PERSISTENCE['WORKER'].on_interval = on_interval
        hub.PERSISTENCE['WORKER'].off_interval = off_interval

        print('Starting Heating Thread')
        hub.PERSISTENCE['WORKER'].start()

def deactivate_heating():
    grovepi.pinMode(8, 'OUTPUT')
    print('Stopping Heating Thread')
    hub.PERSISTENCE['WORKER'].stop()
    time.sleep(0.5)
    print('Turning Relay Off')
    grovepi.digitalWrite(8, 0)




def heating_on(power):
    activate_heating(power)
    return Response(power, status=200)

def heating_off():
    deactivate_heating()
    return Response('off', status=200)