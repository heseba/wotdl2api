import importlib


IMPLEMENTATION_PATH = 'wot_api.models'
print('hub imported')

PERSISTENCE = {}
INIT_FUNCTION_NAME = 'init'


def invoke_implementation(function_name, kwargs, request, device):
    import_path = IMPLEMENTATION_PATH + '.' + device

    implementation_spec = importlib.util.find_spec(import_path)
    found = implementation_spec is not None

    if found:
        implementation = importlib.import_module(import_path)
        if hasattr(implementation, INIT_FUNCTION_NAME):
            plugin_init_function = getattr(implementation, INIT_FUNCTION_NAME)
            plugin_init_function()
        if not hasattr(implementation, function_name):
            return 'Implementation required for %s of device %s' % (function_name, device)
        method = getattr(implementation, function_name)
        if len(kwargs) > 0:
            return method(**kwargs)
        else:
            return method()
    else:
        return 'Implementation required for device %s' % device
