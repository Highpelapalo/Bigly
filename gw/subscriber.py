import mqutils
import pika

### TODO ###
class Subscriber:
    def __init__(self, mqc, callback):
        self.mqc = mqc
        self.callback = callback
        self.channel = mqutils.Channel(mqc.channel)

    def subscribe(self, exchange, queue, **kwds):
        self.channel = mqc.consume(self.channel, self.callback, queue=queue, **kwds)

    def start(self):
        self.channel.channel.start_consuming()
        
