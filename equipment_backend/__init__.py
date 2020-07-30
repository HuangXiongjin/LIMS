from flask_bootstrap import Bootstrap
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask import Flask, request

from common.common_cuid import insert, delete, update, select
from common.common_cuid import accurateSelect
from database.connect_db import CONNECT_DATABASE

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT_DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'qa12wecde34fss2'

# 创建数据库连接对象
db = SQLAlchemy(app)

from account.user_auth import users
from account import user_auth
from equipment_backend.product.equipment_fitting import equipment
from equipment_backend.product.work_order import work_order
from common.equipment_models import *

app.register_blueprint(users)
app.register_blueprint(equipment, url_prefix='/equipment')
app.register_blueprint(work_order, url_prefix='/work')

# 绑定app和数据库，迁移使用
migrate = Migrate(app, db)
# 传输命令行参数
manager = Manager(app)
manager.add_command('db', MigrateCommand)

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'qeqhdasdqiqd131'

user_auth.login_manager.init_app(app)

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


api.add_resource(CUIDList, '/CUID')


@app.route('/')
def hello_world():
    return 'Hello LIMS!!!'
