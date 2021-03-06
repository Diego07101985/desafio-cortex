import json
from http import HTTPStatus
import desafio.currency.messages as messages
from desafio.extensions import cache, fpika
from desafio.currency.services import ServiceQuoteCurrencyPrice
from flask import jsonify, Blueprint, request
from desafio.producers import ProducerCurrency
from desafio.currency.models import RequestCurrencyQuotationParam


bp = Blueprint('default', __name__,
               url_prefix="/")

currencies = Blueprint('currencies', __name__,
                       url_prefix="/currency")


JSON_CONTENT = {'Content-Type': 'application/json'}


@bp.route("/healthcheck", methods=['GET'], strict_slashes=False)
def healthcheck():
    return jsonify({'status': 'online'})


@currencies.route('/', methods=["GET"])
def get_quotes():
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    initial_date = request.args.get('initial_date')
    final_date = request.args.get('final_date')

    if not from_currency or not to_currency or not initial_date or not final_date:
        return json.dumps({'error': messages.HTTP_STATUS_BAD_REQUEST_QUERY_GET}), \
            HTTPStatus.BAD_REQUEST, JSON_CONTENT

    amount = request.args.get('amount')
    priority = request.args.get('priority')

    try:
        amount = float(amount)
        priority = int(priority)
    except ValueError:
        return json.dumps({'error': messages.HTTP_STATUS_BAD_REQUEST_GET}), \
            HTTPStatus.BAD_REQUEST, JSON_CONTENT

    service_currencies = ServiceQuoteCurrencyPrice()

    cache_currency_key = 'currencys'
    cache_currencys = cache.get('currencys')

    if cache_currencys is None:
        try:
            cache_currencys = service_currencies.get_all_currencys()
            cache.set(cache_currency_key, cache_currencys)
        except ValueError:
            return json.dumps({'error':  messages.HTTP_STATUS_OK_GET_COTA}), \
                HTTPStatus.OK, JSON_CONTENT

    if from_currency not in cache_currencys or to_currency not in cache_currencys:
        return json.dumps({'error':  messages.HTTP_STATUS_NO_CONTENT_GET}), \
            HTTPStatus.NO_CONTENT, JSON_CONTENT

    key_period_request = f'{from_currency}-{to_currency}-{initial_date}-{final_date}'

    cache_period_request = cache.get(key_period_request)

    if not cache_period_request:
        request_params = RequestCurrencyQuotationParam(
            from_currency, to_currency, initial_date, final_date)
        result = service_currencies.get_relation_ratio_between_currencies_in_given_period(
            request_params)
        channel = fpika.channel()
        producer = ProducerCurrency(channel)
        if not priority:
            producer.get_currencys_in_base_bbc(
                1, 'relation.between.currencys', request_params)
        else:
            producer.get_currencys_in_base_bbc(
                priority, 'relation.between.currencys', request_params)

        quotations_currency = service_currencies.calc_quotes(result, amount)

        return json.dumps({'status': 'MISS', 'results': quotations_currency}), \
            HTTPStatus.OK, JSON_CONTENT

    quotations_currency = service_currencies.calc_quotes(
        cache_period_request, amount)
    return json.dumps({'status': 'HIT', 'results': quotations_currency}), \
        HTTPStatus.OK, JSON_CONTENT
