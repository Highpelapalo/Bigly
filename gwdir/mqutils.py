import pika
import collections
import time

def connection_state(handler):
    """A decorator you use when you have to make sure the connection is updated"""
    def decorator(func):
        def decorated_func(*args,**kwds):
            if len(args) == 0:
                raise TypeError('Misssing a required argument to function {func}'.format(func=func.__name__)) 
            handler(args[0])
            return func(*args, **kwds)
        return decorated_func
    return decorator

def compare_dicts(dict1, dict2):
    if not len(dict1.items()) == len(dict2.items()):
        return False
    set1 = set(dict1.items())
    set2 = set(dict2.items())
    shared = set1 & set2
    if len(shared) == len(set1):
        return True

def default_handler(mqc):
    if mqc.connection:
        if not compare_dicts(mqc._connection_parameters, mqc.args):
            try:
                print('Found a newer connection')
                mqc.close()
            except Exception as e:
                print('Can\'t finish opening the new connection', e)
            finally:
                mqc.connect(wait=True)
        elif not mqc.connection.is_open:
            mqc.connect(wait=True)
            print('Using new connection, old one is closed')
    return mqc

class Channel:
    def __init__(self, channel):
        self.channel = channel

    def close(self):
        self.channel.close()


class MQC:
    def __init__(self, host, args={}):
        self.connection = None
        self.args=args
        self.args['host'] = host
        self.channels = []
        self.exchanges = []
        self.queues = {}
    
    def connect(self, wait=False):
        self.connection = None
        self._connection_parameters = dict(self.args)
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(**self.args))
            for channel in self.channels:
                channel.channel = self.channel(add=False)
        except:
            if wait:
                print('Waiting for connection')
                time.sleep(3)
                self.connect(wait)

    def close(self):
        ret_val = self.connection.close()
        del self.connection
        return ret_val

    @connection_state(default_handler)
    def channel(self, add=True):
        channel = Channel(self.connection.channel())
        if add:
            self.channels.append(channel)


    @connection_state(default_handler)
    def exchange_declare(self, channel, name, exchange_type):
        try:
            channel.channel.exchange_decalre(exchange=name, type=exchange_type)
            self.channels.add((name, exchange_type))
            return name
        except:
            self.connect(wait=True)
            #exchange_declare(self, channel, name, exchange_type)

    @connection_state(default_handler)
    def publish(self, channel, exchange, key, message):
        try:
            channel.channel.basic_publish(exchange=exchange, routing_key=key, message=message)
        except:
            self.connect(wait=True)
            publish(self, channel, exchange, key, message)
            

    @connection_state(default_handler)
    def queue_declare(self, channel, name):
        try:
            res = channel.channel.queue_declare(queue=name, exclusive=True)
            self.queues[res.method.queue] = None
            return res.method.queue
        except:
            self.connect(wait=True)
            #queue_declare(self, channel, **kwds)

    @connection_state(default_handler)
    def queue_bind(self, channel, exchange, queue, key):
        try:
            channel.channel.queue_bind(exchange=exchange, queue=queue, routing_key=key)
            self.queues[queue] = (exchange, key)
        except:
            self.connect(wait=True)
            #queue_bind(self, channel, exchange, queue, key)

    @connection_state(default_handler)
    def consume(self, channel, callback, queue, **kwds):
        try:
            channel.basic_consume(callback, queue=queue, **kwds)
        except:
            self.connect(wait=True)
            consume(self, channel, callback, queue, **kwds)
