import json
from datetime import datetime

from flask import Blueprint, request

from tools.handle import MyEncoder, log, get_short_id, get_uuid
from common.lims_models import db_session, ClassifyTree, QualityStandardCenter, QualityStandard, CheckForm, CheckProject

check = Blueprint('check', __name__)


@check.route('/CheckForm', methods=['GET', 'POST'])
def check_form():
    """样品请检申请"""
    try:
        if request.method == 'GET':
            # 当前页码
            page = int(request.values.get('Page'))
            # 每页记录数
            per_page = int(request.values.get('PerPage'))
            status = request.values.get('Status')
            start_time = "'" + request.values.get('DateTime') + " 00:00:00'"
            end_time = "'" + request.values.get('DateTime') + " 23:59:59'"
            Product = request.values.get('Product')
            results = db_session.query(CheckForm).filter(CheckForm.Name==Product, CheckForm.Status==status, CheckForm.CheckDate.between(start_time, end_time)).order_by(CheckForm.Id.desc()).all()
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
            db_session.add(CheckForm(Name=Name, Specs=Specs, Supplier=Supplier, ProductNumber=ProductNumber, Number=Number,
                                     Amount=Amount, Unit=Unit, CheckProcedure=CheckProcedure, CheckDepartment=CheckDepartment,
                                     CheckDate=CheckDate, CheckUser=CheckUser, Type=Type, Comment=Comment,
                                     CheckProjectNO=CheckProjectNO, CheckNumber=CheckNumber, ProductType=ProductType,
                                     Life='待审核')
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
            return json.dumps({'code': '1000', 'msg': '操作成功'}, ensure_ascii=False)
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)})


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
        data.VerifyUser = VerifyName
        data.VerifyDate = DateTime
        data.Status = '待取样'
        result.append(data)
    db_session.add_all(result)
    db_session.commit()
    return json.dumps({'code': '1000', 'msg': '操作成功'}, ensure_ascii=False)


@check.route('/Sample', methods=['GET', 'POST'])
def sample():
    """取样登记"""
    if request.method == 'GET':
        CheckProjectNO = request.values.get('CheckProjectNO')
        results = db_session.query(CheckProject).filter_by(No=CheckProjectNO).all()
        project = []
        character = []
        discern = []
        inspect = []
        content = []
        microbe = []
        data = [
            {'CheckProjectNO': CheckProjectNO, 'Project': project, 'Character': character, 'Discern': discern, 'Inspect': inspect, 'Content': content,
             'Microbe': microbe}]
        for result in results:
            if result.Project is not None:
                project.append({'id': result.Id, 'value': result.Project})
            if result.Character is not None:
                character.append({'id': result.Id, 'value': result.Character})
            if result.Discern is not None:
                discern.append({'id': result.Id, 'value': result.Discern})
            if result.Inspect is not None:
                inspect.append({'id': result.Id, 'value': result.Inspect})
            if result.Content is not None:
                content.append({'id': result.Id, 'value': result.Content})
            if result.Microbe is not None:
                microbe.append({'id': result.Id, 'value': result.Microbe})
        return json.dumps({'code': '1000', 'msg': '成功', 'data': data}, cls=MyEncoder, ensure_ascii=False)
    if request.method == 'POST':
        CheckProjectNO = request.values.get('CheckProjectNO')
        SampleUser = request.values.get('SampleUser')
        data = db_session.query(CheckForm).filter_by(CheckProjectNO=CheckProjectNO).first()
        data.SampleUser = SampleUser
        data.Status = '待检验'
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
    SampleUser = request.values.get('SampleUser')
    ReceiveUser = request.values.get('ReceiveUser')
    data = db_session.query(CheckForm).filter_by(CheckProjectNO=CheckProjectNO).first()
    data.IntoUser = ReceiveUser
    db_session.add(data)
    db_session.commit()
    return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)