from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource

from database.connect_db import CONNECT_DATABASE
from lims_backend.check_api import check
from lims_backend.distribute_api import distribute
from lims_backend.quality_standard_api import system_interface
from lims_backend.report_api import report
from system_backend.SystemManagement import account_auth
from system_backend.SystemManagement.account_auth import login_auth
from tools.MyEncode import MyEncoder

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT_DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '1qaz2wsx3edd45'
account_auth.login_manager.init_app(app)
# app.json_decoder = MyEncoder

CORS(app, supports_credentials=True)
app.register_blueprint(report)
app.register_blueprint(distribute)
app.register_blueprint(check)
app.register_blueprint(system_interface)
app.register_blueprint(login_auth)

api = Api(app)
from common.common_cuid import select, update, delete, insert
class CUIDList(Resource):
    def get(self):
        return select(request.values)

    def post(self):
        return insert(request.values)

    def put(self):
        return update(request.values)

    def delete(self):
        return delete(request.values)


api.add_resource(CUIDList, '/CUID')


def main():
    # app.run(host='0.0.0.0', port=10002)
    app.run(host='127.0.0.1', port=10002)


@app.route('/')
def hello_world():
    return 'This is lims_backend!'


if __name__ == '__main__':
    main()
