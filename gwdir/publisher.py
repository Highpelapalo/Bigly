import mqcutils

class Publisher:
    def __init__(self, mqc):
        self.mqc = mqc
        self.channel = mqutils.Channel(mqc.channel)

    def publish(self, exchange, key, message):
        self.channel = mqc.publish(self.channel, exchange, key, message)
