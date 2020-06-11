import json

from flask import Blueprint, jsonify

from backend.tools.MyEncode import AlchemyEncoder
from backend.common.models import Users

users = Blueprint('users', __name__)


@users.route('/', methods=['GET'])
def index():
    get_data = Users.query.all()
    return json.dumps({'data': get_data}, cls=AlchemyEncoder, ensure_ascii=True)
