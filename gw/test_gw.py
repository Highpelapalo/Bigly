import requests
from furl import furl

host = 'localhost'
path = 'connect'
port = 8000

url = furl()
url.path = path
url.host = host
url.port = port

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
test_request()
