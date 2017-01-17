from flask import Flask, request, jsonify
import ast
import commands
from mqutils import MQConnection
import subscriber
import publisher
import sys
from collections import deque, defaultdict
import json

app = Flask(__name__)
mqc = None

class Connection:
    def __init__(self, mqc=None):
        self.mqc = mqc
        self.connections = defaultdict(deque)
        self.publisher = None

    def start(self, mqc):
        self.mqc = mqc
        self.publisher = publisher.Publisher(mqc, 'client_direct', 'direct')
    
    def handle_command(self, name, command):
        """Gets (int, string - command tag) and return a commands json"""
        print(command, 'handle')
        return jsonify(commands.commands[command](commands.Data(name=name)))

    def get_command(self, name):
        if name in self.connections:
            try:
                pending = self.connections[name].popleft()
                return self.handle_command(name, pending)
            except IndexError:
                return jsonify({'command':'sleep', 'time':5})
        else:
            tags = commands.run_matchers(commands.Data(name=name)) 
            
            for tag in tags:
                com = commands.commands[tag](commands.Data(name=name))
                self.connections[name].append(tag)
            return self.handle_command(name, self.connections[name][0])

    def get_reactor(self, name, data):
        command = data['command']
        react = commands.run_reactor(command, commands.Data(**data))
        
        if react:
            self.connections[name].appendleft(react)
            return jsonify({'command':'come'})
        else:
            return jsonify({'command':'sleep', 'time':5})
            

commands.import_plugins()

connection = Connection()

@app.route('/connect',methods=['POST'])
def connect():
    name = request.form['name']
    version = request.form['version']
    print('Connect request from {name}'.format(name=name))

    connection.publisher.publish('client_logs', 'Connect request from {name}'.format(name=name))
    
    return connection.get_command(name)

@app.route('/finish', methods=['POST'])
def finish():
    name = request.form['name']
    data = request.form['data']
    data = ast.literal_eval(data)
    command = data['command']
    print('Finish request from {name} - {data}'.format(name=name, data=data))
    mq_json = json.dumps({'name':name, 'data':data})

    connection.publisher.publish('client_products', str(mq_json))
    return connection.get_reactor(name, data)

def run(host=None):
    if not host:
        host = '172.20.0.2'
    global mqc
    mqc = MQConnection(host)
    mqc.connect(wait=True)
    connection.start(mqc)
    print('Establishing connection to MQ')
    queue = connection.publisher.queue_declare('client_logs')
    queue2 = connection.publisher.queue_declare('client_products')
    connection.publisher.queue_bind(queue, 'client_logs')
    connection.publisher.queue_bind(queue2, 'client_products')
    
    app.run(host='0.0.0.0', port=8000)

if __name__ == '__main__':
    print('Starting GW')
    if len(sys.argv) > 1:
        run(host=sys.argv[1])
    else:
        run()
