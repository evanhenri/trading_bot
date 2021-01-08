from flask import Blueprint, jsonify
from flask_restful import Api


blueprint = Blueprint('api_v1', __name__)
api = Api(blueprint, catch_all_404s=True)


from . import (
    exceptions,
    resources
)


@blueprint.errorhandler(exceptions.AppError)
def handle_error(error):
    resp = jsonify(error.to_dict())
    resp.status_code = error.status_code
    return resp
