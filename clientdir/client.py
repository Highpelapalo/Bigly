import requests
from furl import furl
from url import URL
import time

default_host = 'localhost'
default_path = 'connect'
default_port = 8000

name='cool_123'

version='0.1.8'

GW_URL=None


def tag1():
    return {'command':'tag1', 'coolness':6}
def tag2():
    return {'command':'tag2', 'coolness':7}
    
def get_data(data=None):
    if not data:
        data = ''
    return {'name':name, 'version':version, 'data':data}

def run():
    while True:
        try:
            print('Sending request to gw {gw}'.format(gw=GW_URL.connect_url()))
            r = requests.post(GW_URL.connect_url(), data=get_data())
            data = r.json()
            print(data)
            command = data['command']
            if command == 'tag1':
                print("Sending finish")
                r = requests
                r = requests.post(GW_URL.finish_url(), get_data(str(tag1())))
            elif command == 'tag2':
                r = requests
                r = requests.post(GW_URL.finish_url(), get_data(str(tag2())))
            elif command == 'sleep':
                time.sleep(data['time'])
            elif command == 'exit':
                break
            else:
                print('Bug')
        except:
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
    time.sleep(2)
    
    run()
