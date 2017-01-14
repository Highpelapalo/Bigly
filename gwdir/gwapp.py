from flask import Flask, request, jsonify
import ast
import commands

app = Flask(__name__)

commands.import_plugins()

class Connection:
    def __init__(self, name):
        self.name = name
        self.pending = []

    def add_pending(command):
        self.pending.append(command)

connections = {}

def handle_command(name, command):
    """Gets (int, string - command tag) and return a commands json"""
    connections[name].remove(command)
    print(command, 'handle')
    return jsonify(commands.commands[command](commands.Data(name=name)))

@app.route('/connect',methods=['POST'])
def connection():
    name = request.form['name']
    version = request.form['version']
    print('Submit request from {name}'.format(name=name))
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
    name = request.form['name']
    data = request.form['data']
    data = ast.literal_eval(data)
    command = request.form['command']
    print('{name} - {data}'.format(name=name, data=data))
    react = commands.run_reactor(command, commands.Data(**data))
    connections[name].insert(0,react)
    if react:
        return jsonify({'command':'come'})
    else:
        return jsonify({'command':'sleep', 'time':5})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
