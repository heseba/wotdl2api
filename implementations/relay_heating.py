import time
import grovepi
import threading
from flask import Response


RELAY_PIN = 4
MAX_INTERVAL = 20 #seconds


grovepi.pinMode(RELAY_PIN, 'OUTPUT')

class HeatingThread(threading.Thread):

    def __init__(self):
        self.on_interval = .5 * MAX_INTERVAL
        self.off_interval = .5 * MAX_INTERVAL
        super(HeatingThread, self).__init__(target=self.interval_heating)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def interval_heating(self):
        if self.on_interval == MAX_INTERVAL:
            grovepi.digitalWrite(RELAY_PIN, 1)
        else:
            while not self.stopped():
                grovepi.digitalWrite(RELAY_PIN, 1)
                time.sleep(self.on_interval)
                grovepi.digitalWrite(RELAY_PIN, 0)
                time.sleep(self.off_interval)

WORKER = HeatingThread()

def activate_heating(power):
    if power < .2 or power > 1:
        raise ValueError
    else:
        on_interval = power * MAX_INTERVAL
        off_interval = (1-power) * MAX_INTERVAL

        WORKER.on_interval = on_interval
        WORKER.off_interval = off_interval

        print('Starting Heating Thread')
        WORKER.start()

def deactivate_heating():
    print('Stopping Heating Thread')
    WORKER.stop()
    time.sleep(0.5)
    print('Turning Relay Off')
    grovepi.digitalWrite(RELAY_PIN, 0)




def heating_on(power):
    activate_heating(power)
    return Response(power, status=200)

def heating_off():
    deactivate_heating
    return Response('off', status=200)