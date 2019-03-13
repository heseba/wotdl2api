import threading
import time
import grovepi

class HeatingThread(threading.Thread):

    def __init__(self):
        self.on_interval = .5 * 20
        self.off_interval = .5 * 20
        super(HeatingThread, self).__init__(target=self.interval_heating)
        self._stop_event = threading.Event()
        grovepi.pinMode(8, 'OUTPUT')

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def interval_heating(self):
        grovepi.pinMode(8, 'OUTPUT')
        if self.on_interval == 20:
            grovepi.digitalWrite(8, 1)
        else:
            while not self.stopped():
                grovepi.digitalWrite(8, 1)
                time.sleep(self.on_interval)
                grovepi.digitalWrite(8, 0)
                time.sleep(self.off_interval)