from flask import Flask
from flask_cors import CORS

from database.connect_db import CONNECT_DATABASE
# from lims_backend.test import t1

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT_DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, supports_credentials=True)
# app.register_blueprint(t1, url_prefix='/work')


def main():
    app.run(host='0.0.0.0', port=10002)


@app.route('/')
def hello_world():
    return 'This is lims_backend!'


if __name__ == '__main__':
    main()
