import requests
import json

from flask import Response

LAMP_ENDPOINT = "http://10.0.1.118/api/T6GrbnZ0D2QyEYy7DXT7a6v023lHqNixkBU01m8o/lights/2/state"

def switch_on_lamp(a=1):
    j = json.dumps({"on": True})
    r = requests.put(LAMP_ENDPOINT, data=j)
    return Response('hue on', status=200)
def switch_off_lamp(a=1):
    j = json.dumps({"on": False})
    r = requests.put(LAMP_ENDPOINT, data=j)
    return Response('hue off', status=200)
