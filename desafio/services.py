
import requests
from desafio.extensions import fpika
import json
import pika
import time


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


class ServiceQuoteCurrencyPrice:

    def __init__(self, symbol_currency="USD", currencies_quote=[]):
        self.symbol_currency = symbol_currency
        self.currencies_quote = currencies_quote
        self.key_free = "8dd7e72df5931f3f65993c10baebecaaf4dbe39ce879a2aee00c076b1eafd46a"

    def get_currencies_quote(self):
        currencies_quote = ','.join(self.currencies_quote)
        qs = f"?fsym={self.symbol_currency}&tsyms={currencies_quote}"
        api_url_base = f"https://min-api.cryptocompare.com/data/price{qs}"
        try:
            response = requests.get(api_url_base)
        except requests.exceptions.ConnectionError:
            return {'error': f'Foi execedido o maximo de requisições para: {api_url_base}'}

        if response.status_code == 200:
            return json.loads(response.content.decode("utf-8"))
        else:
            return None

    def find_symbol_currency(self, symbol_currency):
        qs = f"?fsym={symbol_currency}&api_key={self.key_free}"
        api_url_base = f"https://min-api.cryptocompare.com/data/v2/pair/mapping/fsym{qs}"

        response = requests.get(api_url_base)

        if response.status_code == 200:
            return json.loads(response.content.decode("utf-8"))
        else:
            return None

    def calc_currency_price_by_currencies_quote(self, amount):

        currencies_quote = self.get_currencies_quote()

        if 'error' in currencies_quote.keys():
            return currencies_quote
        if 'Response' in currencies_quote.keys():
            raise ValueError

        return {currency: round(amount * price, 2) for currency,
                price in currencies_quote.items()}
