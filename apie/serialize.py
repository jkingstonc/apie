# James Clarke
# 28/09/2019

import json, yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

SER_JSON = b'\x00'
SER_YAML = b'\x01'

def ser_json_func(data):
    return json.dumps(data)

def dser_json_func(data):
    return json.loads(data)

def ser_yaml_func(data):
    return yaml.dump(data, Dumper=Dumper)

def dser_yaml_func(data):
    return yaml.load(data, Loader=Loader)

ser_funcs = {
    SER_JSON : (ser_json_func, dser_json_func),
    SER_YAML : (ser_yaml_func, dser_yaml_func),
    }

def serialize(ser_method, data):
    return ser_funcs.get(ser_method)[0](data)

def deserialize(ser_method, data):
    return ser_funcs.get(ser_method)[1](data)