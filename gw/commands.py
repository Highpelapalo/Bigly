from collections import defaultdict
from inspect import getmembers, isfunction
import os, sys
from path import Path

sys.path.append(os.path.join(os.path.dirname(__file__), 'plugins'))

matchers=defaultdict(list)
commands={}
reactors={}

PLUGINS_DIR='plugins/'

class Config:
    def __init__(self, **kwds):
        self.args = kwds

class Data:
    def __init__(self, **kwds):
        for key, value in kwds.items():
            setattr(self, key, value)
        self.args = kwds
    def __repr__(self):
        return str(self.args)

def matcher(value):
    def match(func):
        def decorated(*args, **kwds):
            return func(*args, **kwds)
        matchers[value].append(decorated)
        return decorated
    return match

def command(tag):
    def decorator(func):
        def decorated(*args, **kwds):
            print('Sending command {tag}'.format(tag=tag))
            return func(*args, **kwds)
        commands[tag] = decorated
        return decorated
    return decorator

def reactor(tag):
    def decorator(func):
        def decorated(*args, **kwds):
            print('Sending reactor {tag}'.format(tag=tag))
            return func(*args, **kwds)
        reactors[tag] = func
        return decorated
    return decorator

def import_plugins(path=None):
    if not path:
        path = PLUGINS_DIR
    plugin_dir = Path(path) 
    for plugin in plugin_dir.files('*_plugin.py'):
        enable_plugin(plugin)

def enable_plugin(plugin_string):
    plugin_string = plugin_string.replace('.py', '')
    plugin = __import__(os.path.basename(plugin_string))
    function_list = [o[1] for o in getmembers(plugin) if isfunction(o[1])]
    for func in function_list:
        func

def run_matcher(matcher, data):
    tag = matcher(data)
    return tag

def run_reactor(reactor, data):
    print(reactors, reactor)
    tag = reactors[reactor](data)
    return tag

def run_matchers(data):
    tags = []
    values = matchers.keys()
    for value in values:
        for matcher in matchers[value]:
            tag = run_matcher(matcher, data)
            if tag:
                tags.append(tag)
    return tags
