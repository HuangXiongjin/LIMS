import json
import socket
import datetime

from flask import Flask, request
from flask_cors import CORS

from database.connect_db import CONNECT_DATABASE
from lims_backend.check_api import check
from lims_backend.curd_api import crud_interface
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
app.register_blueprint(crud_interface)
app.register_blueprint(report)
app.register_blueprint(distribute)
app.register_blueprint(check)
app.register_blueprint(system_interface)
app.register_blueprint(login_auth)


def main():
    # app.run(host='0.0.0.0', port=10002)
    app.run(host='127.0.0.1', port=10002)


@app.route('/')
def hello_world():
    return 'This is lims_backend!'


@app.errorhandler(Exception)
def error_handler(e):
    """全局捕获异常"""
    re_path = request.path
    re_func = request.url_rule.endpoint.split('.')[1]
    re_method = request.method
    # root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # file_path = os.path.join(root_path, 'logs\\logs.txt')
    ip = socket.gethostbyname(socket.gethostname())
    result = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -- {ip} -- {re_path} -- {re_func} -- {re_method} -- {e} "
    print(result)
    return json.dumps({'code': '2000', 'msg': result}, cls=MyEncoder, ensure_ascii=False)


if __name__ == '__main__':
    main()
