import mqutils
import pika

class Subscriber:
    def __init__(self, mqc, callback, exchange_name, exchange_type):
        self.mqc = mqc
        self.callback = callback
        self.exchange = mqc.exchange_declare(exchange_name, exchange_type)

    def subscribe(self, queue, **kwds):
        self.channel = self.mqc.consume(self.callback, queue=queue, **kwds)

    def queue_declare(self, name):
         return self.mqc.queue_declare(name)

    def queue_bind(self, queue, key):
        return self.mqc.queue_bind(self.exchange, queue, key)

    def start(self):
        self.mqc.start_consuming()
