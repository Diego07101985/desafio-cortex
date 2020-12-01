import requests
import json
import pika


class ProducerCurrency():
    def __init__(self, channel):
        self.channel = channel
        self.count = 0

    def get_currencys_in_base_bbb(self, priority):
        self.count = self.count + 1
        self.channel.exchange_declare(
            exchange='topic_priority', exchange_type='topic')

        routing_key = 'anonymous.info'
        message = {'id':  self.count, 'priority': str(priority)}

        self.channel.basic_publish(
            properties=pika.BasicProperties(
                priority=priority, delivery_mode=2),
            exchange='topic_priority',
            routing_key=routing_key,
            body=json.dumps(message)
        )
