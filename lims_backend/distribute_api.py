import json
from datetime import datetime

from flask import Blueprint, request

from tools.handle import MyEncoder, log, get_short_id, get_uuid
from common.lims_models import db_session, ClassifyTree, QualityStandardCenter, QualityStandard, CheckForm, \
    CheckProject, Distribute, ProductSave

distribute = Blueprint('distribute', __name__)


@distribute.route('/Distribute', methods=['POST'])
def product_distribute():
    """样品分发"""
    Action = request.values.get('Action')
    CheckProjectNO = request.values.get('CheckProjectNO')
    User = request.values.get('User')
    Account = request.values.get('Account')
    # no = request.values.get('no')
    Group = request.values.get('Group')
    GroupUser = request.values.get('GroupUser')
    LaboratoryUser = request.values.get('LaboratoryUser')
    Time = request.values.get('Time')
    print('1111111111')
    data = db_session.query(CheckForm).filter_by(CheckProjectNO=CheckProjectNO).first()
    if Action == 'J':
        data.Action = '检验'
        data.Status = '检验中'
    elif Action == 'F':
        data.Action = '复查'
        data.Status = '复查'
    elif Action == 'L':
        data.Action = '留样'
        data.Status = '留样'
    elif Action == '接收':
        data.Action = '接收'
        data.LaboratoryUser = LaboratoryUser
    data.OutUser = User
    data.Account = Account
    print('2222222222')
    db_session.add(data)
    db_session.commit()
    print('333333333333')
    db_session.add(Distribute(CheckProjectNO=CheckProjectNO, User=User, Group=Group, GroupUser=GroupUser, Time=Time))
    db_session.commit()
    print('44444444444444')
    return json.dumps({'code': '1000', 'msg': '操作成功'}, ensure_ascii=False)


@distribute.route('/ProductSave', methods=['POST'])
def product_save():
    """留样单"""
    db_session.add(ProductSave(CheckProjectNO=request.values.get('CheckProjectNO'), Name=request.values.get('Name'), Specs=request.values.get('Specs'),
                               PackSpecs=request.values.get('PackSpecs'), ProductNumber=request.values.get('ProductNumber'),
                               TheoreticalYield=request.values.get('TheoreticalYield'), BatchAmount=request.values.get('BatchAmount'),
                               BatchDepartment=request.values.get('BatchDepartment'), BatchName=request.values.get('BatchName'),
                               Handler=request.values.get('Handler'), ProductionDate=request.values.get('ProductionDate'),
                               ValidityDate=request.values.get('ValidityDate'), Comment=request.values.get('Comment'),
                               ProductSaveNo=get_uuid()))
    db_session.commit()
    return json.dumps({'code': '1000', 'msg': '操作成功'}, ensure_ascii=False)
