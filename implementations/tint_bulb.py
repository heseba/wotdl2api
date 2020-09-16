import requests
import json

from flask import Response

LAMP_ENDPOINT = "http://10.0.1.200:80/api/E70AB7E7DB/lights/5/state"

def switch_on_tint_lamp():
    j = json.dumps({"on": True})
    r = requests.put(LAMP_ENDPOINT, data=j)
    print(r.text)
    return Response('tint lamp on', status=200)
def switch_off_tint_lamp():
    j = json.dumps({"on": False})
    r = requests.put(LAMP_ENDPOINT, data=j)
    return Response('tint lamp off', status=200)
