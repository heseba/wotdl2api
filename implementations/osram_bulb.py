import requests
import json

from flask import Response

LAMP_ENDPOINT = "http://10.0.1.200:80/api/E70AB7E7DB/lights/4/state"

def switch_on_osram_lamp():
    j = json.dumps({"on": True})
    r = requests.put(LAMP_ENDPOINT, data=j)
    print(r.text)
    return Response('osram lamp on', status=200)
def switch_off_osram_lamp():
    j = json.dumps({"on": False})
    r = requests.put(LAMP_ENDPOINT, data=j)
    return Response('osram lamp off', status=200)
