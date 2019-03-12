from flask import Response

print('samsungTV imported')

def switch_tv_on(path_param, query_param1=None):
    return Response(path_param, status=200)