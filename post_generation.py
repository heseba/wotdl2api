import fileinput
import sys
import re
import yaml

TARGET = sys.argv[1]
MODULE = sys.argv[2]
OPENAPI_FILE_NAME = sys.argv[3]

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

FUNCTION_SIGNATURE = 'def (.*)\((.+)\):  # noqa: E501'
controller_function = re.compile(FUNCTION_SIGNATURE)

filename = TARGET + '/' + MODULE + '/controllers/default_controller.py'

with open(filename, 'r+') as file:
    content = file.read()
    file.seek(0, 0)
    file.write(IMPORT_STATEMENTS + '\n' + content)

with open(OPENAPI_FILE_NAME, 'r') as api_file:
    api_spec = yaml.load(api_file)

    with fileinput.FileInput(filename, inplace=True) as file:
        for line in file:
            if controller_function.match(line):
                #def switch_on_tv(path_param, power):  # noqa: E501
                function_name = controller_function.match(line).group(1)
                arguments = controller_function.match(line).group(2).split(',')
                updated_arguments = []
                request_type = ''
                for argument in arguments:
                    for path in api_spec['paths']:
                        for operation in api_spec['paths'][path]:
                            #move the assignment of request_type into the if statement                            
                            if api_spec['paths'][path][operation]['operationId'] == function_name:
                                request_type = operation
                                if 'parameters' in api_spec['paths'][path][operation]:
                                    for param in api_spec['paths'][path][operation]['parameters']:
                                        if param['name'].replace('-', '_') == argument:
                                            updated_arguments.append(argument.strip())
                                break
                if request_type in ['post', 'put']:
                    updated_arguments.append('body')
                updated_argument_list = ', '.join(updated_arguments)
                print(controller_function.sub(r'def \1(' + updated_argument_list + '):  # noqa: E501', line), end='')
            else:
                print(line.replace(REPLACE_TEXT, REPLACEMENT), end='')


#TODO: in __main__.py add custom resolver

