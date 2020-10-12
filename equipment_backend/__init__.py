from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from database.connect_db import CONNECT_DATABASE

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT_DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from equipment_backend.product.equipment_fitting import equipment
from equipment_backend.product.work_order import work_order
from common.equipment_models import *

app.register_blueprint(equipment, url_prefix='/equipment')
app.register_blueprint(work_order, url_prefix='/work')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route('/')
def hello_world():
    return 'This is LIMS!'
