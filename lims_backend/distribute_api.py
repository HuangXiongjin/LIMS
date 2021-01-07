import json
from datetime import datetime

from flask import Blueprint, request

# from lims_run import CRUD
from tools.handle import MyEncoder, log, get_short_id, get_uuid
from common.lims_models import db_session, ClassifyTree, QualityStandardCenter, QualityStandard, CheckForm, \
    CheckProject, Distribute, ProductSave, CheckLife, Worker, Record, WorkerBook, ProductSaveSurvey

distribute = Blueprint('distribute', __name__)


@distribute.route('/CheckRecord', methods=['GET', 'POST'])
def record():
    """记录获取"""
    if request.method == 'GET':
        data = db_session.query(Record).filter_by(CheckProjectNO=request.values.get('CheckProjectNO')).first()
        return json.dumps({'code': '1000', 'msg': '操作成功', 'data': data}, cls=MyEncoder, ensure_ascii=False)
    if request.method == 'POST':
        CheckProjectNO = request.values.get('CheckProjectNO')
        data = db_session.query(CheckForm).filter_by(CheckProjectNO=CheckProjectNO).first()
        db_session.add(Record(CheckProjectNO=CheckProjectNO, Product=data.Name, ProductNumber=data.ProductNumber,
                              Specs=data.Specs, CheckDepartment=data.CheckDepartment,
                              Type=request.values.get('Type'),
                              Number=data.Amount, SampleTime=data.SampleTime,
                              CheckTime=request.values.get('CheckTime'),
                              Basis=request.values.get('Basis')))
        db_session.commit()
        return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)


@distribute.route('/Worker', methods=['GET', 'POST'])
def get_worker():
    """实验室组员检测项分发"""
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
                result.append({'ID': i.ID, 'Name': i.Name})
        elif data1.Group == '微生物组主管':
            data = db_session.query(Worker).filter_by(Group='微生物组').all()
            for i in data:
                result.append({'ID': i.ID, 'Name': i.Name})
        elif data1.Group == '物料组主管':
            data = db_session.query(Worker).filter_by(Group='物料组').all()
            for i in data:
                result.append({'ID': i.ID, 'Name': i.Name})
        return json.dumps({'code': '1000', 'msg': '操作成功', 'data': result, 'Group': groups}, cls=MyEncoder,
                          ensure_ascii=False)
    if request.method == 'POST':
        Name = request.values.get('Name')
        work_name = request.values.get('Worker')
        CheckProjectNO = request.values.get('CheckProjectNO')
        Content = json.loads(request.values.get('Content'))
        CheckStartTime = request.values.get('CheckStartTime')
        Character = json.loads(request.values.get('Character'))
        Discern = json.loads(request.values.get('Discern'))
        Inspect = json.loads(request.values.get('Inspect'))
        # Content = request.values.get('Content')
        Microbe = json.loads(request.values.get('Microbe'))
        # Content = {"张三": ["性状", "检查1", "鉴别1"], "李四": ["鉴别2"]}
        data = db_session.query(CheckForm).filter_by(CheckProjectNO=CheckProjectNO).first()
        db_session.add(CheckLife(Product=data.Product, Specs=data.Specs, Supplier=data.Supplier, ProductNumber=data.ProductNumber,
                  Number=data.Number, Amount=data.Amount, Unit=data.Unit, CheckProcedure=data.CheckProcedure,
                  CheckDepartment=data.CheckDepartment, CheckDate=CheckStartTime, CheckUser=Name,
                  Content='完成了样品质检项的分发', Status='质检', CheckProjectNO=CheckProjectNO,
                  CheckNumber=data.CheckNumber, ProductType=data.ProductType
                  ))
        db_session.commit()
        data.Status = '质检'
        db_session.add(data)
        db_session.commit()
        if len(Content) > 0:
            for work in Content:
                db_session.add(WorkerBook(CheckProjectNO=CheckProjectNO, Name=work_name, CheckProject=work,
                                          CheckStartTime=CheckStartTime, CheckType='Content'))
                db_session.commit()
        if len(Discern) > 0:
            for work in Discern:
                db_session.add(WorkerBook(CheckProjectNO=CheckProjectNO, Name=work_name, CheckProject=work,
                                          CheckStartTime=CheckStartTime, CheckType='Discern'))
                db_session.commit()
        if len(Character) > 0:
            for work in Character:
                db_session.add(WorkerBook(CheckProjectNO=CheckProjectNO, Name=work_name, CheckProject=work,
                                          CheckStartTime=CheckStartTime, CheckType='Character'))
                db_session.commit()
        if len(Inspect) > 0:
            for work in Inspect:
                db_session.add(WorkerBook(CheckProjectNO=CheckProjectNO, Name=work_name, CheckProject=work,
                                          CheckStartTime=CheckStartTime, CheckType='Inspect'))
                db_session.commit()
        if len(Microbe) > 0:
            for work in Microbe:
                db_session.add(WorkerBook(CheckProjectNO=CheckProjectNO, Name=work_name, CheckProject=work,
                                          CheckStartTime=CheckStartTime, CheckType='Microbe'))
                db_session.commit()
        return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder)


@distribute.route('/Distribute', methods=['GET', 'POST'])
def product_distribute():
    """样品分发"""
    if request.method == 'POST':
        Action = json.loads(request.values.get('Action', '1'))
        CheckProjectNO = request.values.get('CheckProjectNO')
        User = request.values.get('User')
        Account = json.loads(request.values.get('Account', '1'))
        No = json.loads(request.values.get('no', '1'))
        Group = json.loads(request.values.get('Group', '1'))
        GroupUser = request.values.get('GroupUser')
        Time = request.values.get('Time')
        CheckForm_data = db_session.query(CheckForm).filter_by(CheckProjectNO=CheckProjectNO).first()
        for item in range(0, len(Action)):
            if Action[item] == 'J':
                d = Distribute()
                d.CheckProjectNO = CheckProjectNO
                d.Status = 'J'
                d.User = User
                d.Time = Time
                d.No = No[item]
                d.JNumber = Account[item]
                db_session.add_all([CheckForm_data, d])
                db_session.commit()
                db_session.add(
                    CheckLife(Product=CheckForm_data.Product, Specs=CheckForm_data.Specs, Supplier=CheckForm_data.Supplier,
                              ProductNumber=CheckForm_data.ProductNumber,
                              Number=CheckForm_data.Number, Amount=CheckForm_data.Amount, Unit=CheckForm_data.Unit,
                              CheckProcedure=CheckForm_data.CheckProcedure,
                              CheckDepartment=CheckForm_data.CheckDepartment, CheckDate=Time, CheckUser=User,
                              Content='完成了样品检验分发', Status='分发', CheckProjectNO=CheckProjectNO,
                              CheckNumber=CheckForm_data.CheckNumber, ProductType=CheckForm_data.ProductType
                              ))
                db_session.commit()
            elif Action[item] == 'F':
                d = Distribute()
                d.CheckProjectNO = CheckProjectNO
                d.Status = 'F'
                d.User = User
                d.Time = Time
                d.No = No[item]
                d.FNumber = Account[item]
                db_session.add(
                    CheckLife(Product=CheckForm_data.Product, Specs=CheckForm_data.Specs,
                              Supplier=CheckForm_data.Supplier,
                              ProductNumber=CheckForm_data.ProductNumber,
                              Number=CheckForm_data.Number, Amount=CheckForm_data.Amount, Unit=CheckForm_data.Unit,
                              CheckProcedure=CheckForm_data.CheckProcedure,
                              CheckDepartment=CheckForm_data.CheckDepartment, CheckDate=Time, CheckUser=User,
                              Content='完成了样品备用分发', Status='备用分发', CheckProjectNO=CheckProjectNO,
                              CheckNumber=CheckForm_data.CheckNumber, ProductType=CheckForm_data.ProductType
                              ))
                db_session.commit()
                db_session.add_all([CheckForm_data, d])
                db_session.commit()
            elif Action[item] == 'L':
                d = Distribute()
                # d = db_session.query(Distribute).filter_by(CheckProjectNO=CheckProjectNO).first()
                pro_save = ProductSave()
                d.CheckProjectNO = CheckProjectNO
                d.Status = 'L'
                pro_save.CheckProjectNO = CheckProjectNO
                pro_save.BatchAmount = Account[item]
                pro_save.BatchNumber = No[item]
                pro_save.Status = '待接收'
                d.User = User
                d.Time = Time
                d.No = No[item]
                d.LNumber = Account[item]
                CheckForm_data.OutUser = User
                db_session.add_all([CheckForm_data, d, pro_save])
                db_session.commit()
                db_session.add(
                    CheckLife(Product=CheckForm_data.Product, Specs=CheckForm_data.Specs,
                              Supplier=CheckForm_data.Supplier,
                              ProductNumber=CheckForm_data.ProductNumber,
                              Number=CheckForm_data.Number, Amount=CheckForm_data.Amount, Unit=CheckForm_data.Unit,
                              CheckProcedure=CheckForm_data.CheckProcedure,
                              CheckDepartment=CheckForm_data.CheckDepartment, CheckDate=Time, CheckUser=User,
                              Content='完成了样品留样分发', Status='留样分发', CheckProjectNO=CheckProjectNO,
                              CheckNumber=CheckForm_data.CheckNumber, ProductType=CheckForm_data.ProductType
                              ))
                db_session.commit()
            elif Action[item] == 'Q':
                d = db_session.query(Distribute).filter_by(CheckProjectNO=CheckProjectNO, Status='J').first()
                d.Group = str(Group)
                d.User = GroupUser
                d.Time = Time
                db_session.add(d)
                db_session.commit()
                db_session.add(
                    CheckLife(Product=CheckForm_data.Product, Specs=CheckForm_data.Specs,
                              Supplier=CheckForm_data.Supplier,
                              ProductNumber=CheckForm_data.ProductNumber,
                              Number=CheckForm_data.Number, Amount=CheckForm_data.Amount, Unit=CheckForm_data.Unit,
                              CheckProcedure=CheckForm_data.CheckProcedure,
                              CheckDepartment=CheckForm_data.CheckDepartment, CheckDate=Time, CheckUser=GroupUser,
                              Content='完成了样品小组分发', Status='小组分发', CheckProjectNO=CheckProjectNO,
                              CheckNumber=CheckForm_data.CheckNumber, ProductType=CheckForm_data.ProductType
                              ))
                db_session.commit()
        return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)


@distribute.route('/ProductSave', methods=['GET', 'POST'])
def product_save():
    """留样单"""
    if request.method == 'GET':
        # 当前页码
        page = int(request.values.get('Page'))
        # 每页记录数
        per_page = int(request.values.get('PerPage'))
        status = request.values.get('Status')
        # start_time = "'" + request.values.get('DateTime') + " 00:00:00'"
        # end_time = "'" + request.values.get('DateTime') + " 23:59:59'"
        Product = request.values.get('Product')
        CheckProjectNO = request.values.get('CheckProjectNO')
        # db_session.query(Distribute).filter_by(Status=status, CheckProjectNO=CheckProjectNO).first()
        if CheckProjectNO is None:
            results = db_session.query(ProductSave).filter_by(Name=Product).order_by(ProductSave.ID.desc()).all()
            data = results[(page - 1) * per_page:page * per_page]
            return json.dumps({'code': '1000', 'msg': '操作成功', 'data': data, 'total': len(results)}, cls=MyEncoder,
                              ensure_ascii=False)
        else:
            data = db_session.query(ProductSave).filter_by(
                CheckProjectNO=request.values.get('CheckProjectNO'), Name=Product).first()
            return json.dumps({'code': '1000', 'msg': '操作成功', 'data': data}, cls=MyEncoder, ensure_ascii=False)
    if request.method == 'POST':
        data = db_session.query(CheckForm).filter_by(CheckProjectNO=request.values.get('CheckProjectNO')).first()
        pro_save = db_session.query(ProductSave).filter_by(
            CheckProjectNO=request.values.get('CheckProjectNO')).first()
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
        pro_save.Status = '留样观察中'
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
        db_session.add(
            CheckLife(Product=data.Product, Specs=data.Specs, Supplier=data.Supplier, ProductNumber=data.ProductNumber,
                      Number=data.Number, Amount=data.Amount, Unit=data.Unit, CheckProcedure=data.CheckProcedure,
                      CheckDepartment=data.CheckDepartment, CheckDate=request.values.get('BatchTime'), CheckUser=request.values.get('BatchName'),
                      Content='完成了样品留样分发', Status='留样分发', CheckProjectNO=request.values.get('CheckProjectNO'),
                      CheckNumber=data.CheckNumber, ProductType=data.ProductType
                      ))
        db_session.commit()
        return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)


@distribute.route('/ProductSaveSurvey', methods=['POST'])
def product_save_survey():
    if request.method == 'POST':
        data = ProductSaveSurvey()
        data.CheckProjectNO = request.values.get('CheckProjectNO')
        data.Name = request.values.get('Name')
        data.Temperature = request.values.get('Temperature')
        data.RH = request.values.get('RH')
        data.Position = request.values.get('Position')
        data.BatchNumber = request.values.get('BatchNumber')
        data.BatchDate = request.values.get('BatchDate')
        data.Specs = request.values.get('Specs')
        data.BatchAmount = request.values.get('BatchAmount')
        data.Handler = request.values.get('Handler')
        data.Project = request.values.get('Project')
        data.SixMonth = request.values.get('SixMonth')
        data.TwelveMonth = request.values.get('TwelveMonth')
        data.EighteenMonth = request.values.get('EighteenMonth')
        data.TwentyFourMonth = request.values.get('TwentyFourMonth')
        data.ThirtyMonth = request.values.get('ThirtyMonth')
        data.ThirtySix = request.values.get('ThirtySix')
        data.FortyEight = request.values.get('FortyEight')
        data.Conclude = request.values.get('Conclude')
        data.Comment = request.values.get('Comment')
        db_session.add(data)
        db_session.commit()
        return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)


@distribute.route('/ProductSaveList', methods=['GET'])
def save_list():
    if request.method == 'GET':
        # 当前页码
        page = int(request.values.get('Page'))
        # 每页记录数
        per_page = int(request.values.get('PerPage'))
        status = request.values.get('Status')
        # start_time = "'" + request.values.get('DateTime') + " 00:00:00'"
        start_time = request.values.get('DateTime')
        end_time = request.values.get('DateTime')
        # end_time = "'" + request.values.get('DateTime') + " 23:59:59'"
        Product = request.values.get('Product')
        results = db_session.query(ProductSave).filter(ProductSave.Name == Product, ProductSave.Status == status,
                                                       ProductSave.BatchTime.between(start_time, end_time)).order_by(
            ProductSave.ID.desc()).all()
        data = results[(page - 1) * per_page:page * per_page]
        return json.dumps({'code': '1000', 'msg': '成功', 'data': data, 'total': len(results)}, cls=MyEncoder,
                          ensure_ascii=False)
