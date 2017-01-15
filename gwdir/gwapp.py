from flask import Flask, request, jsonify
import ast
import commands
from mqutils import MQC
import subscriber
import publisher
import sys

app = Flask(__name__)
mqc = None

commands.import_plugins()

class Connection:
    def __init__(self, name):
        self.name = name
        self.pending = []

    def add_pending(command):
        self.pending.append(command)

connections = {}

publish_worker = None

def handle_command(name, command):
    """Gets (int, string - command tag) and return a commands json"""
    global connections
    connections[name].remove(command)
    print(command, 'handle')
    return jsonify(commands.commands[command](commands.Data(name=name)))

@app.route('/connect',methods=['POST'])
def connection():
    global connections
    name = request.form['name']
    version = request.form['version']
    print('Connect request from {name}'.format(name=name))
    publish_worker.publish('client_logs', 'Connect request from {name}'.format(name=name))
    if name in connections.keys():
        try:
            pending = connections[name][0]
            return handle_command(name, pending)
        except:
            return jsonify({'command':'sleep', 'time':5})
    tags = commands.run_matchers(commands.Data(name=name)) 
    connections[name] = []
    for tag in tags:
        com = commands.commands[tag](commands.Data(name=name))
        connections[name].append(tag)
    return handle_command(name, connections[name][0])

@app.route('/finish', methods=['POST'])
def diconnect():
    global connections
    name = request.form['name']
    data = request.form['data']
    data = ast.literal_eval(data)
    command = data['command']
    print('Finish request from {name} - {data}'.format(name=name, data=data))
    publish_worker.publish('client_product', str({'name':name, 'data':data}))
    react = commands.run_reactor(command, commands.Data(**data))
    connections[name].insert(0,react)
    if react:
        return jsonify({'command':'come'})
    else:
        return jsonify({'command':'sleep', 'time':5})

def run(host=None):
    if not host:
        host = '172.20.0.2'
    global mqc
    mqc = MQC(host)
    mqc.connect(wait=True)
    global publish_worker
    publish_worker = publisher.Publisher(mqc, 'client_direct', 'direct')
    print('Establishing connection to MQ')
    queue = publish_worker.queue_declare('client_logs')
    queue2 = publish_worker.queue_declare('client_product')
    publish_worker.queue_bind(queue, 'client_logs')
    publish_worker.queue_bind(queue2, 'client_product')
    
    app.run(host='0.0.0.0', port=8000)

if __name__ == '__main__':
    print('Starting GW')
    if len(sys.argv) > 1:
        run(host=sys.argv[1])
    else:
        run()
