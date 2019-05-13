from flask import Response

print('samsungTV imported')

def switch_on_tv(path_param):
    return Response(path_param, status=200)