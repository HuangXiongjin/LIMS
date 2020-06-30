from flask_bootstrap import Bootstrap
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask import Flask, request

from backend.common.common_cuid import insert, delete, update, select, accurateSelect
from backend.common.common_cuid import accurateSelect
from backend.database.connect_db import CONNECT_DATABASE

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT_DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'qa12wecde34fss2'

# 创建数据库连接对象
db = SQLAlchemy(app)

from backend.account.views import users
from backend.product.equipment_fitting import equipment
from backend.common.models import *

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(equipment, url_prefix='/equipment')


# 绑定app和数据库，迁移使用
migrate = Migrate(app, db)
# 传输命令行参数
manager = Manager(app)
manager.add_command('db', MigrateCommand)

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'qeqhdasdqiqd131'

from backend.account import views

views.login_manager.init_app(app)

api = Api(app)


class CUIDList(Resource):
    def get(self):
        data = request.values
        searchModes = data.get("searchModes")
        if searchModes == "精确查询":
            return accurateSelect(request.values)
        else:  # 模糊查询
            return select(request.values)

    def post(self):
        return insert(request.values)

    def put(self):
        return update(request.values)

    def delete(self):
        return delete(request.values)


# api.add_resource(CUIDList, '/CUID')


@app.route('/')
def hello_world():
    return 'Hello LIMS!'


