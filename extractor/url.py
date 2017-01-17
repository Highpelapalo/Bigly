from furl import furl
import utils

default_api_host='localhost'
default_api_port='8000'
default_scheme='http'

# Yes this class is very much like client/url.py except for the paths
# --> I could have made a superior version and put it inside utils/
# but I rather concentrate on the exporter...

class URL:
    def __init__(self, host=None, port=None, scheme=None):
        self.url = furl()
        self.url.host = utils.set_default(default_api_host, host)
        self.url.port = utils.set_default(default_api_port, port)
        self.url.scheme = utils.set_default(default_scheme, scheme)

    def get_base_url(self):
        return self.url.url

    def get_base_data_url(self):
        self.url.path.segments = ['saver', 'data', '']
        return self.url.url

    def get_base_clients_url(self):
        self.url.path.segments = ['saver', 'clients', '']
        return self.url.url
        
    def get_client_name_url(self, name):
        self.url.path.segments = ['saver', 'clients', 'name', name, '']
        return self.url.url

    def get_client_pk_url(self, pk):
        self.url.path.segments = ['saver', 'clients', pk]
        return self.url.url

    def get_data_pk_url(self, pk):
        self.url.path.segments = ['saver', 'data', pk]
        return self.url.url
