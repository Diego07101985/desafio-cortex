from flask import jsonify, Blueprint

bp = Blueprint('default', __name__,
               url_prefix="/")

currencies = Blueprint('currencies', __name__,
                       url_prefix="/currency")


JSON_CONTENT = {'Content-Type': 'application/json'}


@bp.route("/healthcheck", methods=['GET'], strict_slashes=False)
def healthcheck():
    return jsonify({'status': 'online'})
