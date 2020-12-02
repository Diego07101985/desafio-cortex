import json
import pika


class ProducerCurrency():
    def __init__(self, channel):
        self.channel = channel

    def get_currencys_in_base_bbc(self, priority, routing_key, rp_currency):
        self.channel.exchange_declare(
            exchange='topic_priority', exchange_type='topic')

        self.channel.basic_publish(
            properties=pika.BasicProperties(
                priority=priority, delivery_mode=2),
            exchange='topic_priority',
            routing_key=routing_key,
            body=json.dumps({
                'to_simbol': rp_currency.to_simbol,
                'from_simbol':  rp_currency.from_simbol,
                'initial_date': rp_currency.initial_date,
                'final_date': rp_currency.final_date
            })
        )
