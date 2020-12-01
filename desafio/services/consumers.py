
import requests
from desafio.extensions import fpika
import json
import pika
import time


class ConsumerCurrency():
    def __init__(self, channel):
        self.channel = channel

    def receive_currencys_in_base_bbb(self, binding_key):
        self.channel.exchange_declare(
            exchange='topic_priority', exchange_type='topic')

        # result = self.channel.queue_declare('priority_queue', exclusive=True)
        self.channel.queue_declare('priority_queue')

        queue_name = "priority_queue"
        self.channel.queue_bind(exchange='topic_priority',
                                queue=queue_name, routing_key=binding_key)

        def callback(ch, method, properties, body):
            print(" [x] %r:%r" % (method.routing_key, json.loads(body)))
            self.channel.basic_ack(delivery_tag=method.delivery_tag)
            time.sleep(1)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=callback)

        print(' [*] Waiting for currencys. To exit press CTRL+C')

        self.channel.start_consuming()