from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
import pymssql

from backend.database.connect_db import CONNECT_DATABASE

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT_DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 创建数据库连接对象
db = SQLAlchemy(app)

from backend.account.views import users
from backend.product.inner_product.views import products
from backend.common.models import *

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(products, url_prefix='/products')


# 绑定app和数据库，迁移使用
migrate = Migrate(app, db)
# 传输命令行参数
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route('/')
def hello_world():
    return 'Hello LIMS!'
