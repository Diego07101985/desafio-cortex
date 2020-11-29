from flask import jsonify, Blueprint
from desafio.extensions import fpika
from flask import request, jsonify
from desafio.services import ProducerCurrency
import time

bp = Blueprint('default', __name__,
               url_prefix="/")


@bp.route("/healthcheck", methods=['GET'], strict_slashes=False)
def healthcheck():
    return jsonify({'status': 'online'})


@bp.route("/testepika", methods=['GET'], strict_slashes=False)
def testpika():
    for i in range(50):
        ch = fpika.channel()
        producer = ProducerCurrency(ch)
        priority = int(request.args.get('priority'))
        producer.get_currencys_in_base_bbb(priority)
        fpika.return_broken_channel(ch)
    return jsonify({'status': 'online'})
