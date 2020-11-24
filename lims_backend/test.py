import json

from flask import Blueprint
from flask_login import current_user

from tools.handle import MyEncoder, log
from common.lims_models import db_session
from common.batch_plan_model import PlanManager

t1 = Blueprint('t123', __name__)


@t1.route('/index', methods=['GET'])
def index1():
    try:
        data = db_session.query(PlanManager).all()
        return json.dumps({'data': data}, cls=MyEncoder, ensure_ascii=False)
    except Exception as e:
        log(e, 'current_user.Name')
