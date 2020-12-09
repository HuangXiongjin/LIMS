import json
from datetime import datetime

from flask import Blueprint, request

from tools.handle import MyEncoder, log, get_short_id, get_uuid
from common.lims_models import db_session, ClassifyTree, QualityStandardCenter, QualityStandard, CheckForm, \
    CheckProject, Distribute

distribute = Blueprint('distribute', __name__)


@distribute.route('/Distribute', methods=['POST'])
def product_distribute():
    CheckProjectNO = request.values.get('CheckProjectNO')
    User = request.values.get('User')
    Number = request.values.get('Number')
    Group = request.values.get('Group')
    GroupUser = request.values.get('GroupUser')
    Time = request.values.get('GroupUser')
    db_session.add(Distribute(CheckProjectNO=CheckProjectNO, User=User, Number=Number, Group=Group, GroupUser=GroupUser,
                              Time=Time))
    db_session.commit()
    return json.dumps({'code': '1000', 'msg': '操作成功'}, ensure_ascii=False)

