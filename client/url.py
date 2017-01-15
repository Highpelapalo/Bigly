from furl import furl

default_host = 'localhost'
default_connect = 'connect'
default_finish = 'finish'
default_port = 8000
default_scheme = 'http'

def set_default(default_value, value=None):
    if value:
        return value
    else:
        return default_value

class URL:
    def __init__(self, host=None, connect=None, finish=None, port=None, scheme=None):
        self.host = set_default(default_host, host)
        self.connect = set_default(default_connect, connect)
        self.finish = set_default(default_finish, finish)
        self.port = set_default(default_port, port)
        self.scheme = set_default(default_scheme, scheme)

    def connect_url(self):
        url = furl()
        url.host= self.host
        url.path = self.connect
        url.port = self.port
        url.scheme = self.scheme
        return url.url

    def finish_url(self):
        url = furl()
        url.host= self.host
        url.path = self.finish
        url.port = self.port
        url.scheme = self.scheme
        return url.url
