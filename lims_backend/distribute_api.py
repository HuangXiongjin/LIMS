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
    """实验室组员检测项分发"""
    try:
        if request.method == 'GET':
            CheckProjectNO = request.values.get('CheckProjectNO')
            Name = request.values.get('Name')
            # Name = '代晓进'
            data1 = db_session.query(Worker).filter_by(Name=Name).first()
            query_data = db_session.query(Distribute).filter_by(CheckProjectNO=CheckProjectNO).first()
            # print(query_data.Group)
            groups = query_data.Group
            result = []
            if data1.Group == '产品组主管':
                data = db_session.query(Worker).filter_by(Group='产品组').all()
                for i in data:
                    result.append({'Id': i.Id, 'Name': i.Name})
            elif data1.Group == '微生物组主管':
                data = db_session.query(Worker).filter_by(Group='微生物组').all()
                for i in data:
                    result.append({'Id': i.Id, 'Name': i.Name})
            elif data1.Group == '物料组主管':
                data = db_session.query(Worker).filter_by(Group='物料组').all()
                for i in data:
                    result.append({'Id': i.Id, 'Name': i.Name})
            return json.dumps({'code': '1000', 'msg': '操作成功', 'data': result, 'Group': groups}, cls=MyEncoder,
                              ensure_ascii=False)
        if request.method == 'POST':
            Name = request.values.get('Name')
            work_name = request.values.get('Worker')
            CheckProjectNO = request.values.get('CheckProjectNO')
            Content = json.loads(request.values.get('Content'))
            CheckStartTime = request.values.get('CheckStartTime')
            # Content = {"张三": ["性状", "检查1", "鉴别1"], "李四": ["鉴别2"]}
            data = db_session.query(CheckForm).filter_by(CheckProjectNO=CheckProjectNO).first()
            db_session.add(CheckLife(No=CheckProjectNO, User=Name, Status='质检', Product=data.Name,
                                     CheckNumber=data.CheckNumber, ProductType=data.ProductType, OperationTime=CheckStartTime,
                                     Work='完成了样品检测项分发'))
            db_session.commit()
            data.Life = '质检'
            db_session.add(data)
            db_session.commit()
            for work in Content:
                db_session.add(WorkerBook(CheckProjectNO=CheckProjectNO, Name=work_name, CheckProject=work,
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
            Action = json.loads(request.values.get('Action', '1'))
            CheckProjectNO = request.values.get('CheckProjectNO')
            User = request.values.get('User')
            Account = json.loads(request.values.get('Account', '1'))
            No = json.loads(request.values.get('no', '1'))
            Group = json.loads(request.values.get('Group', '1'))
            GroupUser = request.values.get('GroupUser')
            LaboratoryUser = request.values.get('LaboratoryUser')
            Time = request.values.get('Time')
            CheckForm_data = db_session.query(CheckForm).filter_by(CheckProjectNO=CheckProjectNO).first()
            db_session.add(CheckLife(No=CheckProjectNO, User=LaboratoryUser, Status='分发', Product=CheckForm_data.Name,
                                     CheckNumber=CheckForm_data.CheckNumber, ProductType=CheckForm_data.ProductType,
                                     OperationTime=Time, Work='完成了样品分发'))
            db_session.commit()
            for item in range(0, len(Action)):
                if Action[item] == 'J':
                    d = Distribute()
                    d.CheckProjectNO = CheckProjectNO
                    CheckForm_data.Action = '检验'
                    CheckForm_data.Status = '检验中'
                    CheckForm_data.Life = '分发'
                    CheckForm_data.JAccount = Account[item]
                    # data.JNo = No[item]
                    CheckForm_data.Foo = No[item]
                    d.User = User
                    d.Time = Time
                    d.No = No[item]
                    d.Number = Account[item]
                    d.Group = Group
                    CheckForm_data.OutUser = User
                    db_session.add_all([CheckForm_data, d])
                    db_session.commit()
                elif Action[item] == 'F':
                    d = Distribute()
                    d.CheckProjectNO = CheckProjectNO
                    CheckForm_data.Action = '复查'
                    CheckForm_data.Status = '复查'
                    CheckForm_data.FAccount = Account[item]
                    # data.FNo = No[item]
                    CheckForm_data.FUser = User
                    CheckForm_data.Foo = No[item]
                    d.User = User
                    d.Time = Time
                    d.No = No[item]
                    d.Number = Account[item]
                    CheckForm_data.OutUser = User
                    db_session.add_all([CheckForm_data, d])
                    db_session.commit()
                elif Action[item] == 'L':
                    d = Distribute()
                    pro_save = ProductSave()
                    d.CheckProjectNO = CheckProjectNO
                    pro_save.CheckProjectNO = CheckProjectNO
                    pro_save.BatchAmount = Account[item]
                    # CheckForm_data.Action = '留样'
                    CheckForm_data.LUser = User
                    CheckForm_data.LAccount = Account[item]
                    CheckForm_data.Foo = No[item]
                    d.User = User
                    d.Time = Time
                    d.No = No[item]
                    d.Number = Account[item]
                    CheckForm_data.OutUser = User
                    db_session.add_all([CheckForm_data, d, pro_save])
                    db_session.commit()
                elif Action[item] == 'Q':
                    d = Distribute()
                    d.CheckProjectNO = CheckProjectNO
                    CheckForm_data.Action = '接收'
                    CheckForm_data.LaboratoryUser = GroupUser
                    d.Group = str(Group)
                    d.User = User
                    d.Time = Time
                    CheckForm_data.OutUser = User
                    db_session.add_all([CheckForm_data, d])
                    db_session.commit()
                    db_session.add(CheckLife(No=CheckProjectNO, User=LaboratoryUser, Status='分发', Product=CheckForm_data.Name,
                                             CheckNumber=CheckForm_data.CheckNumber, ProductType=CheckForm_data.ProductType,
                                             OperationTime=Time,
                                             Work='完成了样品接收'))
                    db_session.commit()
            return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)}, cls=MyEncoder)


@distribute.route('/ProductSave', methods=['POST'])
def product_save():
    """留样单"""
    try:
        if request.method == 'GET':
            CheckProjectNO = request.values.get('CheckProjectNO')
            if CheckProjectNO is None:
                pro_save = db_session.query(ProductSave).all()
                return json.dumps({'code': '1000', 'msg': '操作成功', 'data': pro_save}, cls=MyEncoder, ensure_ascii=False)
            else:
                pro_save = db_session.query(ProductSave).filter_by(
                    CheckProjectNO=request.values.get('CheckProjectNO')).first()
                return json.dumps({'code': '1000', 'msg': '操作成功', 'data': pro_save}, cls=MyEncoder, ensure_ascii=False)
        if request.method == 'POST':

            data = db_session.query(CheckForm).filter_by(CheckProjectNO=request.values.get('CheckProjectNO')).first()
            db_session.add(CheckLife(No=request.values.get('CheckProjectNO'), User=request.values.get('BatchName'),
                                     Status='留样', Product=data.Name, ProductType=data.ProductType, Work='完成了样品留样',
                                     OperationTime=request.values.get('BatchTime'), CheckNumber=data.CheckNumber))
            db_session.commit()
            pro_save = db_session.query(ProductSave).filter_by(CheckProjectNO=request.values.get('CheckProjectNO')).first()
            pro_save.Name = request.values.get('Product')
            pro_save.Specs = request.values.get('Specs')
            pro_save.Position = request.values.get('Position')
            pro_save.PackSpecs = request.values.get('PackSpecs')
            pro_save.ProductNumber = request.values.get('ProductNumber')
            pro_save.TheoreticalYield = request.values.get('TheoreticalYield')
            pro_save.BatchAmount = request.values.get('BatchAmount')
            pro_save.BatchDepartment = request.values.get('BatchDepartment')
            pro_save.BatchName = request.values.get('BatchName')
            pro_save.Handler = request.values.get('Handler')
            pro_save.ProductionDate = request.values.get('ProductionDate')
            pro_save.ValidityDate = request.values.get('ValidityDate')
            pro_save.Comment = request.values.get('Comment')
            pro_save.ProductSaveNo = get_uuid()
            pro_save.BatchTime = request.values.get('BatchTime')
            # db_session.add(ProductSave(CheckProjectNO=request.values.get('CheckProjectNO'), Name=request.values.get('Name'),
            #                            Specs=request.values.get('Specs'), Position=request.values.get('Position'),
            #                            PackSpecs=request.values.get('PackSpecs'),
            #                            ProductNumber=request.values.get('ProductNumber'),
            #                            TheoreticalYield=request.values.get('TheoreticalYield'),
            #                            BatchAmount=request.values.get('BatchAmount'),
            #                            BatchDepartment=request.values.get('BatchDepartment'),
            #                            BatchName=request.values.get('BatchName'),
            #                            Handler=request.values.get('Handler'),
            #                            ProductionDate=request.values.get('ProductionDate'),
            #                            ValidityDate=request.values.get('ValidityDate'), Comment=request.values.get('Comment'),
            #                            ProductSaveNo=get_uuid(), BatchTime=request.values.get('BatchTime')))
            db_session.add(pro_save)
            db_session.commit()
            return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)}, cls=MyEncoder)


@distribute.route('/Check', methods=['GET', 'POST'])
def test():
    """人员检测记录"""
    try:
        if request.method == 'GET':
            name = request.values.get('Name')
            query_work = db_session.query(WorkerBook).filter_by(Name=name).first()
            query_data = db_session.query(WorkerBook).filter_by(CheckProjectNO=query_work.CheckProjectNO).all()
            check_data = [{"name": item.Name, "work": item.CheckProject} for item in query_data]
            return json.dumps({'code': '1000', 'msg': '操作成功', 'data': check_data}, cls=MyEncoder, ensure_ascii=False)
        if request.method == 'POST':
            # pass
            return json.dumps({'code': '1000', 'msg': '操作成功', 'data': 'check_data'}, cls=MyEncoder, ensure_ascii=False)
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)}, cls=MyEncoder)
