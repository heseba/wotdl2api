import fileinput
import sys

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
    request_device = r'(.*) request on device (.*)'
    pattern = re.compile(request_device)
    
    function = inspect.currentframe()
    function_name = function.f_code.co_name
    arguments = function.f_code.co_varnames[0:function.f_code.co_argcount]
    source_code = inspect.getsource(function.f_code)
    comments = StringIO(source_code)
    
    strings = [token for type, token, _, _, _ in tokenize.generate_tokens(comments.readline) if type == tokenize.STRING]
    
    matches = pattern.search(strings[0].strip('"'))
    request = matches.group(1)
    device = matches.group(2)
    
    return hub.invoke_implementation(function_name, arguments, request, device)
"""


filename = TARGET + '/' + MODULE + '/controllers/default_controller.py'

with open(filename, 'r+') as file:
    content = file.read()
    file.seek(0, 0)
    file.write(IMPORT_STATEMENTS + '\n' + content)

with fileinput.FileInput(filename, inplace=True) as file:
    for line in file:
        print(line.replace(REPLACE_TEXT, REPLACEMENT), end='')
