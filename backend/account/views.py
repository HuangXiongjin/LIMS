import json
from flask import Blueprint, render_template, request
from flask import Blueprint, jsonify

from backend.tools import autocode
from backend.tools.MyEncode import AlchemyEncoder
from backend.common.models import Users

users = Blueprint('users', __name__)


@users.route('/', methods=['GET'])
def index():
    get_data = Users.query.all()
    return json.dumps({'data': get_data}, cls=AlchemyEncoder, ensure_ascii=True)


@users.route('/system_set/make_model', methods=['POST', 'GET'])
def make_model():
    if request.method == 'POST':
        data = request.values
        try:
            jsonstr = json.dumps(data.to_dict())
            return autocode.make_model_main(data)
        except Exception as e:
            print(e)


