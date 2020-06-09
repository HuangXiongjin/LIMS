from flask import Blueprint, jsonify

from backend.common.models import Users

from backend.common.schema import UserSchema

users = Blueprint('users', __name__)


@users.route('/', methods=['GET'])
def index():
    # get_data = Users.query.all()
    # user_schema = UserSchema(many=True)
    # data = user_schema.dump(get_data)
    return jsonify({'data': "data"})
