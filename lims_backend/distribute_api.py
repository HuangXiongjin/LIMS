import json
from datetime import datetime

from flask import Blueprint, request

from tools.handle import MyEncoder, log, get_short_id, get_uuid
from common.lims_models import db_session, ClassifyTree, QualityStandardCenter, QualityStandard, CheckForm, \
    CheckProject, Distribute, ProductSave, CheckLife, Worker, Record

distribute = Blueprint('distribute', __name__)


@distribute.route('/Record', methods=['GET', 'POST'])
def record():
    """记录获取"""
    if request.method == 'GET':
        data = db_session.query(Record).filter_by(CheckProjectNO=request.values.get('CheckProjectNO')).first()
        return json.dumps({'code': '1000', 'msg': '操作成功', 'data': data}, cls=MyEncoder, ensure_ascii=False)
    if request.method == 'POST':
        data = request.values
        db_session.add(Record(CheckProjectNO=data.get('CheckProjectNO'), Product=data.get('Product'), ProductNumber=data.get('ProductNumber'),
                              Specs=data.get('Specs'), CheckDepartment=data.get('CheckDepartment'), Type=data.get('Type'),
                              Number=data.get('Number'), SampleTime=data.get('SampleTime'), CheckTime=data.get('CheckTime'),
                              Basis=data.get('Basis')))
        db_session.commit()
        return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)


@distribute.route('/Worker', methods=['GET'])
def get_worker():
    """实验室组员"""
    try:
        if request.method == 'GET':
            groups = json.loads(request.values.get('Group'))
            print(groups)
            # groups = request.json
            result = []
            for item in groups:
                data = db_session.query(Worker).filter_by(Group=item).all()
                for i in data:
                    result.append({'Id': i.Id, 'Name': i.Name})
            return json.dumps({'code': '1000', 'msg': '操作成功', 'data': result}, cls=MyEncoder, ensure_ascii=False)
        # if request.method == 'POST':
        #     data = request.values
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)})


@distribute.route('/Distribute', methods=['POST'])
def product_distribute():
    """样品分发"""
    Action = json.loads(request.values.get('Action'))
    CheckProjectNO = request.values.get('CheckProjectNO')
    User = request.values.get('User')
    Account = json.loads(request.values.get('Account'))
    # no = request.values.get('no')
    Group = request.values.get('Group')
    GroupUser = request.values.get('GroupUser')
    LaboratoryUser = request.values.get('LaboratoryUser')
    Time = request.values.get('Time')
    data = db_session.query(CheckForm).filter_by(CheckProjectNO=CheckProjectNO).first()
    db_session.add(CheckLife(No=CheckProjectNO, User=LaboratoryUser, Status='分发', Product=data.Name,
                             ProductType=data.ProductType, OperationTime=Time, Work='样品分发'))
    db_session.commit()
    for item in range(0, len(Action)):
        if Action[item] == 'J':
            data.Action = '检验'
            data.Status = '检验中'
            data.JAccount = Account[item]
        elif Action[item] == 'F':
            data.Action = '复查'
            data.Status = '复查'
            data.FAccount = Account[item]
            data.FUser = User
        elif Action[item] == 'L':
            data.Action = '留样'
            data.Status = '留样'
            data.LAccount = Account[item]
            data.LUser = User
        elif Action[item] == '接收':
            data.Action = '接收'
            data.LaboratoryUser = LaboratoryUser
    data.OutUser = User
    db_session.add(data)
    db_session.commit()
    db_session.add(Distribute(CheckProjectNO=CheckProjectNO, User=User, Group=Group, GroupUser=GroupUser, Time=Time))
    db_session.commit()
    return json.dumps({'code': '1000', 'msg': '操作成功'}, ensure_ascii=False)


@distribute.route('/ProductSave', methods=['POST'])
def product_save():
    """留样单"""
    data = db_session.query(CheckForm).filter_by(CheckProjectNO=request.values.get('CheckProjectNO')).first()
    db_session.add(CheckLife(No=request.values.get('CheckProjectNO'), User=request.values.get('BatchName'),
                             Status='留样', Product=data.Name, ProductType=data.ProductType,
                             OperationTime=request.values.get('BatchTime'), Work='样品留样'))
    db_session.commit()
    db_session.add(ProductSave(CheckProjectNO=request.values.get('CheckProjectNO'), Name=request.values.get('Name'),
                               Specs=request.values.get('Specs'),
                               PackSpecs=request.values.get('PackSpecs'),
                               ProductNumber=request.values.get('ProductNumber'),
                               TheoreticalYield=request.values.get('TheoreticalYield'),
                               BatchAmount=request.values.get('BatchAmount'),
                               BatchDepartment=request.values.get('BatchDepartment'),
                               BatchName=request.values.get('BatchName'),
                               Handler=request.values.get('Handler'),
                               ProductionDate=request.values.get('ProductionDate'),
                               ValidityDate=request.values.get('ValidityDate'), Comment=request.values.get('Comment'),
                               ProductSaveNo=get_uuid(), BatchTime=request.values.get('BatchTime')))
    db_session.commit()
    return json.dumps({'code': '1000', 'msg': '操作成功'}, ensure_ascii=False)
