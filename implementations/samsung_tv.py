from flask import Response

print('samsungTV imported')

def switch_on_tv(path_param, power):
    return Response(path_param + str(power), status=200)

def switch_off_tv():
    return Response('Running', status=200)