import fileinput
import sys
import re

TARGET = sys.argv[1]
MODULE = sys.argv[2]

IMPORT_STATEMENTS = """from .. import hub
import inspect
from io import StringIO
import tokenize
import re
""" #% (TARGET, MODULE)

REPLACE_TEXT = "return 'do some magic!'"
REPLACEMENT = """
    request_device_pattern = re.compile(r'(.*) request on device (.*)')
    param_pattern = re.compile(r':param (.*):')

    function = inspect.currentframe()
    function_name = function.f_code.co_name
    arguments = function.f_code.co_varnames[0:function.f_code.co_argcount]
    kwargs = {}
    for argument in arguments:
        kwargs[argument] = function.f_locals[argument]
    source_code = inspect.getsource(function.f_code)
    comments = StringIO(source_code)
    
    strings = [token for type, token, _, _, _ in tokenize.generate_tokens(comments.readline) if type == tokenize.STRING]
    
    matches = request_device_pattern.search(strings[0].strip('"'))
    request = matches.group(1)
    device = matches.group(2)

    params = []

    for line in strings[0].splitlines():
        param_matches = param_pattern.search(line.strip('"'))
        if param_matches != None:
            params.append(param_matches.group(1))
       
    return hub.invoke_implementation(function_name, params, kwargs, request, device)
 
"""

FUNCTION_SIGNATURE = 'def (.*)\(.+\):  # noqa: E501'
controller_function = re.compile(FUNCTION_SIGNATURE)

filename = TARGET + '/' + MODULE + '/controllers/default_controller.py'

with open(filename, 'r+') as file:
    content = file.read()
    file.seek(0, 0)
    file.write(IMPORT_STATEMENTS + '\n' + content)

with fileinput.FileInput(filename, inplace=True) as file:
    for line in file:
        if controller_function.match(line):
            print(controller_function.sub(r'def \1(body):  # noqa: E501', line), end='')
        else:
            print(line.replace(REPLACE_TEXT, REPLACEMENT), end='')

