import requests
import json

from flask import Response

LAMP_ENDPOINT = "http://10.0.1.146/api/5TNOk6IXINqrhn7DJtiYiWRIUqPyVA9NRPIzZASm/lights/1/state"

def switch_on_hue_lamp():
    j = json.dumps({"on": True})
    r = requests.put(LAMP_ENDPOINT, data=j)
    print(r.text)
    return Response('hue on', status=200)
def switch_off_hue_lamp():
    j = json.dumps({"on": False})
    r = requests.put(LAMP_ENDPOINT, data=j)
    return Response('hue off', status=200)
