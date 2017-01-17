from mqutils import MQConnection
import subscriber
import requests
import sys
from url import URL
import json
import requests

myurl = None
current_version = "0.1.9"

def send_api():
    pass

def get_client(name):
    search_clients = myurl.get_client_name_url(name)

    r = requests.get(search_clients)
    data = r.json()
    if data:
        return data[0]['url']
    else:
        return None

def read_product(ch, method, properties, body):
    data = json.loads(body.decode())
    client = data['name']
    command = data['data']['command']
    rest = {key:value for key, value in data['data'].items() if not key == command}
    rest = json.dumps(rest)
    client_url = get_client(client)
    if  not client_url:
        send_data = {"name": client, "version": current_version, "related_data": []}
        r = requests.post(myurl.get_base_clients_url(), data=send_data)
    
        client_url = r.json()['url']

    send_data = {"client": client_url, "command": command, "data": rest}

    r = requests.post(myurl.get_base_data_url(), data=send_data) 
    print(json.dumps(send_data), myurl.get_base_data_url())
    
if __name__ == '__main__':
    host = None
    port = None
    mq_host = None
    print(sys.argv)
    if len(sys.argv) > 1:
        mq_host = sys.argv[1]
    if len(sys.argv) > 2:
        host = sys.argv[2]
    if len(sys.argv) > 3:
        port = sys.argv[3]

    global myurl
    myurl = URL(host=host, port=port)
    
    mqc = MQConnection(mq_host)
    mqc.connect(wait=True)

    subs = subscriber.Subscriber(mqc, read_product, 'client_direct', 'direct')
    queue = subs.queue_declare('client_products_2')
    subs.queue_bind(queue, 'client_products')
    
    subs.subscribe(queue)
    subs.start()
