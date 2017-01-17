from furl import furl
import utils

default_host = 'localhost'
default_connect = 'connect'
default_finish = 'finish'
default_port = 8000
default_scheme = 'http'

class URL:
    def __init__(self, host=None, connect=None, finish=None, port=None, scheme=None):
        self.host = utils.set_default(default_host, host)
        self.connect = utils.set_default(default_connect, connect)
        self.finish = utils.set_default(default_finish, finish)
        self.port = utils.set_default(default_port, port)
        self.scheme = utils.set_default(default_scheme, scheme)

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
