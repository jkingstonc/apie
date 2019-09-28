# James Clarke
# 27/09/2019

import pickle

MAGIC_INDEX = 0
PATH_INDEX = 1
PAYLOAD_CODE_INDEX = 1
ARGS_INDEX = 2
DATA_INDEX = 2

# Generate a routereq header for the NetClient to send
def parse_routereq(route, args=()):
    return (
        3141,
        route,
        args
    )

# Generate a routereq header for the NetClient to send
def parse_routepayload(code, data):
    return (
        3141,
        code,
        data
    )

def get_requestpath(headder):
    return headder[PATH_INDEX]

def get_payloadcode(headder):
    return headder[PAYLOAD_CODE_INDEX]

def get_requestargs(headder):
    return headder[ARGS_INDEX]

def get_payloaddata(headder):
    return headder[DATA_INDEX]