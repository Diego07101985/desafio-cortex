from flask import jsonify, Blueprint

bp = Blueprint('default', __name__,
               url_prefix="/")


@bp.route("/healthcheck", methods=['GET'], strict_slashes=False)
def healthcheck():
    return jsonify({'status': 'online'})
