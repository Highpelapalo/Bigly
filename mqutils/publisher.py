import mqutils

class Publisher:
    def __init__(self, mqc, exchange_name, exchange_type):
        self.mqc = mqc
        self.exchange = mqc.exchange_declare(exchange_name, exchange_type)

    def publish(self, key, message):
        return self.mqc.publish(self.exchange, key, message)

    def queue_declare(self, name):
        return self.mqc.queue_declare(name)

    def queue_bind(self, queue, key):
        return self.mqc.queue_bind(self.exchange, queue, key)
