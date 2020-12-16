import json
from datetime import datetime

from flask import Blueprint, request

from tools.handle import MyEncoder, log, get_short_id, get_uuid
from common.lims_models import db_session, ClassifyTree, QualityStandardCenter, QualityStandard, CheckForm, \
    CheckProject, Distribute, ProductSave, CheckLife, Worker, Record, WorkerBook

distribute = Blueprint('distribute', __name__)


@distribute.route('/CheckRecord', methods=['GET', 'POST'])
def record():
    """记录获取"""
    try:
        if request.method == 'GET':
            data = db_session.query(Record).filter_by(CheckProjectNO=request.values.get('CheckProjectNO')).first()
            return json.dumps({'code': '1000', 'msg': '操作成功', 'data': data}, cls=MyEncoder, ensure_ascii=False)
        if request.method == 'POST':
            CheckProjectNO = request.values.get('CheckProjectNO')
            data = db_session.query(CheckForm).filter_by(CheckProjectNO=CheckProjectNO).first()
            db_session.add(Record(CheckProjectNO=CheckProjectNO, Product=data.Name, ProductNumber=data.ProductNumber,
                                  Specs=data.Specs, CheckDepartment=data.CheckDepartment, Type=request.values.get('Type'),
                                  Number=data.Amount, SampleTime=data.SampleTime, CheckTime=request.values.get('CheckTime'),
                                  Basis=request.values.get('Basis')))
            db_session.commit()
            return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)}, cls=MyEncoder)


@distribute.route('/Worker', methods=['GET', 'POST'])
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
        if request.method == 'POST':
            CheckProjectNO = request.values.get('CheckProjectNO')
            # Content = json.loads(request.values.get('Content'))
            CheckStartTime = request.values.get('CheckStartTime')
            Content = {"张三": ["性状", "检查1", "鉴别1"], "李四": ["鉴别2"]}
            for name, works in Content.items():
                for work in works:
                    db_session.add(WorkerBook(CheckProjectNO=CheckProjectNO, Name=name, CheckProject=work,
                                              CheckStartTime=CheckStartTime))
                    db_session.commit()
            return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder)
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)}, cls=MyEncoder)


@distribute.route('/Distribute', methods=['GET', 'POST'])
def product_distribute():
    """样品分发"""
    try:

        if request.method == 'POST':
            Action = json.loads(request.values.get('Action'))
            CheckProjectNO = request.values.get('CheckProjectNO')
            User = request.values.get('User')
            Account = json.loads(request.values.get('Account'))
            No = json.loads(request.values.get('no'))
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
                    d = Distribute()
                    d.CheckProjectNO = CheckProjectNO
                    data.Action = '检验'
                    data.Status = '检验中'
                    data.JAccount = Account[item]
                    d.User = User
                    d.Time = Time
                    d.No = No[item]
                    d.Number = Account[item]
                    data.OutUser = User
                    db_session.add_all([data, d])
                    db_session.commit()
                elif Action[item] == 'F':
                    d = Distribute()
                    d.CheckProjectNO = CheckProjectNO
                    data.Action = '复查'
                    data.Status = '复查'
                    data.FAccount = Account[item]
                    data.FUser = User
                    d.User = User
                    d.Time = Time
                    d.No = No[item]
                    d.Number = Account[item]
                    data.OutUser = User
                    db_session.add_all([data, d])
                    db_session.commit()
                elif Action[item] == 'L':
                    d = Distribute()
                    d.CheckProjectNO = CheckProjectNO
                    data.Action = '留样'
                    data.Status = '留样'
                    data.LAccount = Account[item]
                    data.LUser = User
                    d.User = User
                    d.Time = Time
                    d.No = No[item]
                    d.Number = Account[item]
                    data.OutUser = User
                    db_session.add_all([data, d])
                    db_session.commit()
                elif Action[item] == '接收':
                    d = Distribute()
                    d.CheckProjectNO = CheckProjectNO
                    data.Action = '接收'
                    data.LaboratoryUser = LaboratoryUser
                    d.User = User
                    d.Time = Time
                    d.No = No[item]
                    d.Number = Account[item]
                    data.OutUser = User
                    db_session.add_all([data, d])
                    db_session.commit()
            return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)}, cls=MyEncoder)


@distribute.route('/ProductSave', methods=['POST'])
def product_save():
    """留样单"""
    try:
        data = db_session.query(CheckForm).filter_by(CheckProjectNO=request.values.get('CheckProjectNO')).first()
        db_session.add(CheckLife(No=request.values.get('CheckProjectNO'), User=request.values.get('BatchName'),
                                 Status='留样', Product=data.Name, ProductType=data.ProductType,
                                 OperationTime=request.values.get('BatchTime'), Work='样品留样'))
        db_session.commit()
        db_session.add(ProductSave(CheckProjectNO=request.values.get('CheckProjectNO'), Name=request.values.get('Name'),
                                   Specs=request.values.get('Specs'), Position=request.values.get('Position'),
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
        return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)}, cls=MyEncoder)


@distribute.route('/Check', methods=['GET', 'POST'])
def test():
    """人员检测"""
    try:
        if request.method == 'GET':
            name = request.values.get('Name')
            query_work = db_session.query(WorkerBook).filter_by(Name=name).all()
            check_data = [item.CheckProject for item in query_work]
        return json.dumps({'code': '1000', 'msg': '操作成功', 'data': check_data}, cls=MyEncoder, ensure_ascii=False)
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)}, cls=MyEncoder)
