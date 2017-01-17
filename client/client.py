import requests
from furl import furl
from url import URL
import json, time
import random

default_host = 'localhost'
default_path = 'connect'
default_port = 8000

name='cool_{}'.format(random.randrange(100, 1000))

version='0.1.8'

GW_URL=None

def tag1():
    rand = random.randrange(1,10)
    return {"command":"tag1", "coolness":rand}
def tag2():
    rand = random.randrange(1,10)
    return {"command":"tag2", "coolness":rand}
    
def get_data(data=None):
    if not data:
        data = ""
    return {"name":name, "version":version, "data":data}

def run():
    while True:
        try:
            print('Sending request to gw {gw}'.format(gw=GW_URL.connect_url()))
            r = requests.post(GW_URL.connect_url(), data=get_data())
            data = r.json()
            command = data['command']
            if command == 'tag1':
                print("Sending finish")
                r = requests.post(GW_URL.finish_url(), data=get_data(str(tag1())))
            elif command == 'tag2':
                r = requests.post(GW_URL.finish_url(), data=get_data(str(tag2())))
            elif command == 'sleep':
                time.sleep(data['time'])
            elif command == 'exit':
                break
            else:
                print('Bug')
        except :
            print('Failed to connect, retrying in 2 seconds')
            time.sleep(2)

if __name__ == '__main__':
    import sys
    print('Starting client')
    host = None
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        global name
        name = sys.argv[2]
    global GW_URL
    GW_URL = URL(host=host)
    print('Working with GW {gw}'.format(gw=GW_URL.host))
    run()
