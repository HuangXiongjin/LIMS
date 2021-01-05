import json

from flask import Blueprint, request

from tools.handle import MyEncoder, get_uuid
from common.lims_models import db_session, ClassifyTree, QualityStandardCenter, QualityStandard, CheckForm, \
    CheckProject, CheckLife, Distribute, ReportVerify

check = Blueprint('check', __name__)


@check.route('/Life', methods=['GET', 'POST'])
def life():
    """功能看板"""
    if request.method == 'GET':
        # 当前页码
        page = int(request.values.get('Page'))
        # 每页记录数
        per_page = int(request.values.get('PerPage'))
        status = request.values.get('Status')
        ProductType = request.values.get('ProductType')
        # start_time = "'" + request.values.get('DateTime') + " 00:00:00'"
        # end_time = "'" + request.values.get('DateTime') + " 23:59:59'"
        # Product = request.values.get('Product')
        results = db_session.query(CheckForm).filter(CheckForm.ProductType == ProductType, CheckForm.Status == status
                                                     ).order_by(CheckForm.Id.desc()).all()
        data = results[(page - 1) * per_page:page * per_page]
        return json.dumps({'code': '1000', 'msg': '成功', 'data': data, 'total': len(results)}, cls=MyEncoder,
                          ensure_ascii=False)


@check.route('/CheckForm', methods=['GET', 'POST'])
def check_form():
    """样品请检申请"""
    if request.method == 'GET':
        # 当前页码
        page = int(request.values.get('Page'))
        # 每页记录数
        per_page = int(request.values.get('PerPage'))
        status = request.values.get('Status')
        start_time = "'" + request.values.get('DateTime') + " 00:00:00'"
        end_time = "'" + request.values.get('DateTime') + " 23:59:59'"
        Product = request.values.get('Product')
        results = db_session.query(CheckForm).filter(CheckForm.Name == Product, CheckForm.Status == status,
                                                     CheckForm.CheckDate.between(start_time, end_time)).order_by(
            CheckForm.Id.desc()).all()
        data = results[(page - 1) * per_page:page * per_page]
        return json.dumps({'code': '1000', 'msg': '成功', 'data': data, 'total': len(results)}, cls=MyEncoder,
                          ensure_ascii=False)
    if request.method == 'POST':
        data = request.values
        CheckNumber = data.get('CheckNumber')
        ProductType = data.get('ProductType')
        Name = data.get('Name')
        Specs = data.get('Specs')
        Supplier = data.get('Supplier')
        ProductNumber = data.get('ProductNumber')
        Number = data.get('Number')
        Amount = data.get('Amount')
        Unit = data.get('Unit')
        CheckProcedure = data.get('CheckProcedure')
        check_project = data.get('CheckProject')
        CheckDepartment = data.get('CheckDepartment')
        CheckDate = data.get('CheckDate')
        CheckUser = data.get('CheckUser')
        Type = data.get('Type')
        Comment = data.get('Comment')
        CheckProjectNO = get_uuid()
        db_session.add(
            CheckForm(Name=Name, Specs=Specs, Supplier=Supplier, ProductNumber=ProductNumber, Number=Number,
                      Amount=Amount, Unit=Unit, CheckProcedure=CheckProcedure, CheckDepartment=CheckDepartment,
                      CheckDate=CheckDate, CheckUser=CheckUser, Type=Type, Comment=Comment, Status='请验审核',
                      CheckProjectNO=CheckProjectNO, CheckNumber=CheckNumber, ProductType=ProductType,
                      Life='请验审核')
            )
        db_session.commit()
        json_data = json.loads(check_project)
        for result in json_data:
            data = []
            for item in json_data[result]:
                c = CheckProject()
                c.No = CheckNumber
                c.Product = Name
                c.Describe = item
                c.Type = result
                c.CheckProjectNO = CheckProjectNO
                data.append(c)
            db_session.add_all(data)
            db_session.commit()
        db_session.add(CheckLife(No=CheckProjectNO, User=CheckUser, Status='申请', ProductType=ProductType,
                                 CheckNumber=CheckNumber, Product=Name, OperationTime=CheckDate, Work='提交了请验单',
                                 Specs=Specs, Supplier=Supplier, ProductNumber=ProductNumber, Number=Number,
                                 Amount=Amount, Unit=Unit)
                       )
        db_session.commit()
        return json.dumps({'code': '1000', 'msg': '操作成功', 'data': CheckProjectNO}, ensure_ascii=False)


@check.route('/CheckVerify', methods=['POST'])
def check_verify():
    """请验审核"""
    CheckProjectNO = request.values.get('CheckProjectNO')
    VerifyName = request.values.get('VerifyName')
    DateTime = request.values.get('DateTime')
    result = []
    items = json.loads(CheckProjectNO)
    for item in items:
        data = db_session.query(CheckForm).filter_by(CheckProjectNO=item).first()
        db_session.add(CheckLife(No=item, User=VerifyName, Status="请验审核", Product=data.Name, CheckNumber=data.CheckNumber,
                                 ProductType=data.ProductType, OperationTime=DateTime, Work="请验申请通过审核",
                                 Specs=data.Specs, Supplier=data.Supplier, ProductNumber=data.ProductNumber,
                                 Number=data.Number, Amount=data.Amount, Unit=data.Unit))
        db_session.commit()
        data.VerifyUser = VerifyName
        data.VerifyDate = DateTime
        data.Status = '取样'
        data.Life = '取样'
        result.append(data)
        db_session.add(ReportVerify(CheckProjectNO=item))
        db_session.commit()
    db_session.add_all(result)
    db_session.commit()
    return json.dumps({'code': '1000', 'msg': '操作成功'}, ensure_ascii=False)


@check.route('/Sample', methods=['GET', 'POST'])
def sample():
    """取样登记"""
    if request.method == 'GET':
        CheckProjectNO = request.values.get('CheckProjectNO')
        results = db_session.query(CheckProject).filter_by(CheckProjectNO=CheckProjectNO).all()
        project = []
        character = []
        discern = []
        inspect = []
        content = []
        microbe = []
        data = [
            {'CheckProjectNO': CheckProjectNO, 'Project': project, 'Character': character, 'Discern': discern,
             'Inspect': inspect, 'Content': content,
             'Microbe': microbe}]
        for result in results:
            if result.Type == 'Character':
                character.append({'id': result.Id, 'value': result.Describe})
            if result.Type == 'Discern':
                discern.append({'id': result.Id, 'value': result.Describe})
            if result.Type == 'Inspect':
                inspect.append({'id': result.Id, 'value': result.Describe})
            if result.Type == 'Content':
                content.append({'id': result.Id, 'value': result.Describe})
            if result.Type == 'Microbe':
                microbe.append({'id': result.Id, 'value': result.Describe})
        return json.dumps({'code': '1000', 'msg': '成功', 'data': data}, cls=MyEncoder, ensure_ascii=False)
    if request.method == 'POST':
        CheckProjectNO = request.values.get('CheckProjectNO')
        SampleUser = request.values.get('SampleUser')
        SampleTime = request.values.get('SampleTime')
        data = db_session.query(CheckForm).filter_by(CheckProjectNO=CheckProjectNO).first()
        db_session.add(CheckLife(No=CheckProjectNO, User=SampleUser, Status='取样', Product=data.Name,
                                 CheckNumber=data.CheckNumber, ProductType=data.ProductType,
                                 OperationTime=SampleTime, Work='完成了样品取样',
                                 Specs=data.Specs, Supplier=data.Supplier, ProductNumber=data.ProductNumber,
                                 Number=data.Number, Amount=data.Amount, Unit=data.Unit))
        db_session.commit()
        data.SampleUser = SampleUser
        data.Status = '接收'
        data.Life = '接收'
        db_session.add(data)
        db_session.commit()
        return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)


@check.route('/AllProduct', methods=['GET'])
def get_all_product():
    """获取全部品名"""
    data = db_session.query(QualityStandardCenter).all()
    results = list(set(item.Product for item in data))
    return json.dumps({'code': '1000', 'msg': '操作成功', 'data': results}, cls=MyEncoder, ensure_ascii=False)


@check.route('/Receive', methods=['POST'])
def receive():
    CheckProjectNO = request.values.get('CheckProjectNO')
    CheckNumber = request.values.get('CheckNumber')
    ReceiveUser = request.values.get('ReceiveUser')
    ReceiveTime = request.values.get('ReceiveTime')
    data = db_session.query(CheckForm).filter_by(CheckProjectNO=CheckProjectNO).first()
    db_session.add(CheckLife(No=CheckProjectNO, CheckNumber=CheckNumber, User=ReceiveUser, Status='接收', Product=data.Name,
                             ProductType=data.ProductType, OperationTime=ReceiveTime, Work='完成了样品接收',
                             Specs=data.Specs, Supplier=data.Supplier, ProductNumber=data.ProductNumber,
                             Number=data.Number, Amount=data.Amount, Unit=data.Unit))
    db_session.commit()
    data.IntoUser = ReceiveUser
    data.Status = '分发'
    db_session.add(data)
    db_session.commit()
    return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)
