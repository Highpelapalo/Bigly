import mqutils

class Publisher:
    def __init__(self, mqc, exchange_name, exchange_type):
        self.mqc = mqc
        self.channel = mqutils.Channel(mqc.channel())
        self.exchange = mqc.exchange_declare(self.channel, exchange_name, exchange_type)

    def publish(self, key, message):
        self.channel = mqc.publish(self.channel, self.exchange, key, message)

    def queue_declare(self, name):
        return self.mqc.queue_declare(self.channel, name)

    def queue_bind(self, queue, key):
        self.mqc.queue_bind(self.channel, self.exchange, queue, key)
