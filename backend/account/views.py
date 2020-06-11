import json
from flask import Blueprint, render_template, request, make_response
from flask import Blueprint, jsonify
from flask_login import login_user, LoginManager

from backend.tools import autocode
from backend.tools.MyEncode import AlchemyEncoder
from backend.common.models import Users
from backend.common.system import db_session, User
import time, datetime


users = Blueprint('users', __name__)
login_manager = LoginManager()
login_manager.db_session_protection = 'strong'
login_manager.login_view = 'login_auth.login'


@users.route('/', methods=['GET'])
def index():
    get_data = Users.query.all()
    return json.dumps({'data': get_data}, cls=AlchemyEncoder, ensure_ascii=True)


@users.route('/system_set/make_model', methods=['POST', 'GET'])
def make_model():
    if request.method == 'POST':
        data = request.values
        try:
            jsonstr = json.dumps(data.to_dict())
            return autocode.make_model_main(data)
        except Exception as e:
            print(e)

@users.route('/account/userloginauthentication', methods=['GET', 'POST'])
def userloginauthentication():
    '''
    用户登陆认证
    :return:
    '''
    try:
        if request.method == 'POST':
            data = request.values
            WorkNumber = data.get('WorkNumber')
            password = data.get('password')
            # 验证账户与密码
            user = db_session.query(User).filter_by(WorkNumber=WorkNumber).first()
            resp = make_response()
            if user and (user.confirm_password(password) or user.Password == password):
                login_user(user)  # login_user(user)调用user_loader()把用户设置到db_session中
                user.session_id = str(time.time())
                user.LastLoginTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                db_session.commit()
                return 'OK'
            else:
                return '用户名密码错误'
    except Exception as e:
        print(e)
        db_session.rollback()
        return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

