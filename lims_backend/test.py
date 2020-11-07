import json

from flask import Blueprint

from equipment_backend.tools.handle import MyEncoder
from lims_models import db_session, plantCalendarScheduling

t1 = Blueprint('t123', __name__)


@t1.route('/index', methods=['GET'])
def index1():
    data = db_session.query(plantCalendarScheduling).all()
    return json.dumps({'data': data}, cls=MyEncoder, ensure_ascii=False)
