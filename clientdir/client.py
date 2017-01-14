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
    return {'coolness':6}
def tag2():
    return {'coolness':7}
    

def test_request():
    url.path = 'connect'
    r = requests.post("http://" + url.url, data={'name':'cool_123', 'version':'0.1.8'})
    data = r.json()
    print(data)
    d = data['command'] 
    url.path = 'finish'
    r = requests.post("http://" + url.url, data={'name':'cool_123', 'command':d, 'data':str(tag1())})
    d = r.json()['command']
    if d == 'come':
        test_request()

def get_data(data=None):
    if not data:
        data = ''
    return {'name':name, 'version':version, 'data':data}

def run():
    while True:
        r = requests.post(GW_URL.connect_url(), data=get_data())
        data = r.json()
        print(data)
        command = data['command']
        if command == 'tag1':
            r = requests
            r = requests.post(GW_URL.finish_url(), get_data(str(tag1())))
        elif command == 'tag2':
            r = requests
            r = requests.post(GW_URL.finish.url(), get_data(str(tag1())))
        elif command == 'sleep':
            time.sleep(data['time'])
        elif command == 'exit':
            break

if __name__ == '__main__':
    GW_URL = URL()
    run()
