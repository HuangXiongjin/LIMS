from flask import Flask
from flask_cors import CORS

from database.connect_db import CONNECT_DATABASE
# from lims_backend.test import t1

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT_DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def main():
    CORS(app, supports_credentials=True)
    from lims_backend.test import t1

    app.register_blueprint(t1, url_prefix='/work')
    app.run(port=10002)
    return app


@app.route('/')
def hello_world():
    return 'This is lims_backend!'


if __name__ == '__main__':
    main()
