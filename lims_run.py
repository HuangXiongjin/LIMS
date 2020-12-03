from flask import Flask
from flask_cors import CORS

from database.connect_db import CONNECT_DATABASE
# from lims_backend.test import t1
from lims_backend.system_api import system_interface
from system_backend.SystemManagement import account_auth
from system_backend.SystemManagement.account_auth import login_auth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT_DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '1qaz2wsx3edd45'
account_auth.login_manager.init_app(app)

CORS(app, supports_credentials=True)
# app.register_blueprint(t1, url_prefix='/work')
app.register_blueprint(system_interface)
app.register_blueprint(login_auth)


def main():
    # app.run(host='0.0.0.0', port=10002)
    app.run(host='127.0.0.1', port=10002)


@app.route('/')
def hello_world():
    return 'This is lims_backend!'


if __name__ == '__main__':
    main()
