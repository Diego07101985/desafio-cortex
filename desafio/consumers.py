
import json
from desafio.extensions import cache
from desafio.currency.models import RequestCurrencyQuotationParam
from desafio.currency.services import ServiceQuoteCurrencyPrice


class ConsumerCurrency():
    def __init__(self, channel):
        self.channel = channel
        self.exchange = 'topic_priority'
        self.channel.exchange_declare(
            exchange='topic_priority', exchange_type='topic')
        self.service_currency = ServiceQuoteCurrencyPrice()

    def receive_quotation_between_period_and_get_relation_currencys(self, binding_key, queue_name):
        self.channel.queue_declare(queue_name)
        self.channel.queue_bind(exchange=self.exchange,
                                queue=queue_name, routing_key=binding_key)

        def callback(ch, method, properties, body):
            rq_currency = json.loads(body)
            request_params = RequestCurrencyQuotationParam(
                rq_currency['from_simbol'], rq_currency['to_simbol'],
                rq_currency['initial_date'], rq_currency['final_date'])
            result = self.service_currency.get_relation_ratio_between_currencies_in_given_period(
                request_params)
            key_period_request = f"{rq_currency['from_simbol']}-{rq_currency['to_simbol']}-{rq_currency['initial_date']}-{rq_currency['final_date']}"

            cache.set(key_period_request, result, timeout=30*60)
            self.channel.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=callback)
        print(' [*] Waiting for worker currencys. To exit press CTRL+C')

        self.channel.start_consuming()
