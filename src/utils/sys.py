'''
Interface between the program and system

'''

import signal

from pynvml import *
from inspect import getfullargspec
from json import load


'''
Auto extracting function's arguments

'''

def func_args(fn, params=None):
    args_keys = getfullargspec(fn)[0]
    if 'self' in args_keys:
        # class constructor
        args_keys.remove('self')

    if params is None:
        return args_keys
    elif len(params) == 0:
        raise Exception("Can not retrive parameter values for the function {} from empty parameter source".format(fn))
    
    args = {}
    for argk in args_keys:
        if argk in params:
            args[argk] = params[argk]
    
    return args


'''
Exception handler

'''

def signal_handler(signal, frame):
    pass


def monitor_signals(signals=[signal.SIGINT, signal.SIGUSR1], handlers=signal_handler):
    if not isinstance(handlers, list) and handlers is not None:
        handlers = [handlers for _ in signals]
        
    for sig, handler in zip(signals, handlers):
        signal.signal(sig, handler)


'''
CUDA

'''




'''
Files

'''

def load_json(filepath):
    with open(filepath, 'rb') as f:
        return load(f)
        

