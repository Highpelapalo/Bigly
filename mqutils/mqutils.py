import pika
import collections
import time

def connection_state(func):
    """A decorator you use when you have to make sure the connection is updated"""
    def decorated_func(*args,**kwds):
        if len(args) == 0:
            raise TypeError('Misssing a required argument to function {func}'.format(func=func.__name__)) 
        mqc = args[0]
        wait = True
        default_handler(mqc)
        if 'wait' in kwds:
            wait = kwds['wait']
        flag = True
        while flag:
            flag = wait
            try:
                ret_value =  func(*args, **kwds)
                return ret_value
            except pika.exceptions.AMQPError as e:
                print("Bump decor")
                mqc.connect(wait)
                continue
                
    return decorated_func

def compare_dicts(dict1, dict2):
    return len(dict1) == len(dict2) == len(dict1.items() & dict2.items())

def default_handler(mqc):
    if mqc.connection:
        if not compare_dicts(mqc._connection_parameters, mqc.args):
            try:
                print('Found a newer connection')
                mqc.close()
            except pika.exceptions.AMQPError as e:
                print('Can\'t finish opening the new connection', e)
            finally:
                print("Bump handler final")
                mqc.connect()
        elif not mqc.connection.is_open:
            print("Bump handler not open")
            mqc.connect(wait)
            print('Using new connection, old one is closed')
    return mqc

class MQConnection:
    def __init__(self, host, args={}):
        self.connection = None
        self.args=args
        self.args['host'] = host
        self.channel = None
        self.exchanges = {}
        self.queues = {}
    
    def connect(self, wait=False):
        self.connection = None
        self._connection_parameters = dict(self.args)
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(**self.args))
            self.channel = self.create_channel()
        except :
            if wait:
                print('Waiting for connection to MQ server')
                time.sleep(3)
                self.connect(wait)
            else:
                raise ValueError('Failed to connect to MQ')

    def close(self):
        ret_val = self.connection.close()
        del self.connection
        return ret_val

    def change_connetion(self, host, args):
        self.args = args
        self.args['host'] = host

    @connection_state
    def create_channel(self, wait=True):
        print("Creating channel")
        self.channel = self.connection.channel()
        return self.channel

    @connection_state
    def exchange_declare(self, name, exchange_type, wait=True):
        #try:
        self.channel.exchange_declare(exchange=name, type=exchange_type)
        self.exchanges[name] = exchange_type
        return name
        #except pika.exceptions.AMQPError as e:
        #    self.connect(wait=True)

    @connection_state
    def publish(self, exchange, key, message, wait=True):
        #try:
        self.channel.basic_publish(exchange=exchange, routing_key=key, body=message)
        #except pika.exceptions.AMQPError as e:
        #    self.connect(wait=True)
            

    @connection_state
    def queue_declare(self, name, wait=True):
        #try:
        res = self.channel.queue_declare(queue=name, exclusive=True)
        self.queues[res.method.queue] = None
        return res.method.queue

    @connection_state
    def queue_bind(self, exchange, queue, key, wait=True):
        self.channel.queue_bind(exchange=exchange, queue=queue, routing_key=key)
        self.queues[queue] = (exchange, key)

    @connection_state
    def consume(self, callback, queue, wait=True, **kwds):
        self.channel.basic_consume(callback, queue=queue, **kwds)

    @connection_state
    def start_consuming(self):
        self.channel.start_consuming()
