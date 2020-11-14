from flask import Flask
from flask_cors import CORS

from database.connect_db import CONNECT_DATABASE
# from lims_backend.test import t1

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT_DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# app.register_blueprint(work_order, url_prefix='/work')


def create_app():
    CORS(app, supports_credentials=True)
    from lims_backend.test import t1

    app.register_blueprint(t1, url_prefix='/work')
    return app


@app.route('/')
def hello_world():
    return 'This is lims_backend!'


def main():
    app.run(port=10002)


if __name__ == '__main__':
    main()
