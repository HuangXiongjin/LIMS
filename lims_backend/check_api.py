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
                                     CheckProjectNO=CheckProjectNO, CheckNumber=CheckNumber, ProductType=ProductType))
            db_session.commit()
            json_data = json.loads(check_project)
            for result in json_data:
                print(result)
                if result == 'xiangmu':
                    data = []
                    for item in json_data[result]:
                        c = CheckProject()
                        c.No = CheckNumber
                        c.Address = CheckProjectNO
                        c.Product = Name
                        c.Project = item
                        data.append(c)
                    db_session.add_all(data)
                    db_session.commit()
                if result == 'xingzhuang':
                    data = []
                    for item in json_data[result]:
                        c = CheckProject()
                        c.No = CheckNumber
                        c.Address = CheckProjectNO
                        c.Product = Name
                        c.Character = item
                        data.append(c)
                    db_session.add_all(data)
                    db_session.commit()
                if result == 'jianbie':
                    data = []
                    for item in json_data[result]:
                        c = CheckProject()
                        c.No = CheckNumber
                        c.Address = CheckProjectNO
                        c.Product = Name
                        c.Discern = item
                        data.append(c)
                    db_session.add_all(data)
                    db_session.commit()
                if result == 'jiancha':
                    data = []
                    for item in json_data[result]:
                        c = CheckProject()
                        c.No = CheckNumber
                        c.Address = CheckProjectNO
                        c.Product = Name
                        c.Inspect = item
                        data.append(c)
                    db_session.add_all(data)
                    db_session.commit()
                if result == 'hanliangceding':
                    data = []
                    for item in json_data[result]:
                        c = CheckProject()
                        c.No = CheckNumber
                        c.Address = CheckProjectNO
                        c.Product = Name
                        c.Content = item
                        data.append(c)
                    db_session.add_all(data)
                    db_session.commit()
                if result == 'weishengwu':
                    data = []
                    for item in json_data[result]:
                        c = CheckProject()
                        c.No = CheckNumber
                        c.Address = CheckProjectNO
                        c.Product = Name
                        c.Microbe = item
                        data.append(c)
                    db_session.add_all(data)
                    db_session.commit()
            # project = []
            # character = []
            # discern = []
            # inspect = []
            # content = []
            # microbe = []
            # data = [
            #     {'编号': No, '项目': project, '性状': character, '鉴别': discern, '检查': inspect, '含量测定': content, '微生物限度': microbe}]
            # for result in results:
            #     if result.Project is not None:
            #         project.append({'id': result.Id, 'value': result.Project})
            #     if result.Character is not None:
            #         character.append({'id': result.Id, 'value': result.Character})
            #     if result.Discern is not None:
            #         discern.append({'id': result.Id, 'value': result.Discern})
            #     if result.Inspect is not None:
            #         inspect.append({'id': result.Id, 'value': result.Inspect})
            #     if result.Content is not None:
            #         content.append({'id': result.Id, 'value': result.Content})
            #     if result.Microbe is not None:
            #         microbe.append({'id': result.Id, 'value': result.Microbe})
            return json.dumps({'code': '1000', 'msg': '操作成功'}, ensure_ascii=False)
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)})


@check.route('/CheckVerify', methods=['POST'])
def check_verify():
    CheckProjectNO = request.values.get('CheckProjectNO')
    VerifyName = request.values.get('VerifyName')
    DateTime = request.values.get('DateTime')
    result = []
    items = json.loads(CheckProjectNO)
    for item in items:
        data = db_session.query(CheckForm).filter_by(CheckProjectNO=item).first()
        data.VerifyUser = VerifyName
        data.CheckDate = DateTime
        result.append(data)
    db_session.add_all(result)
    db_session.commit()
    return json.dumps({'code': '1000', 'msg': '操作成功'}, ensure_ascii=False)


@check.route('/AllProduct', methods=['GET'])
def get_all_product():
    """获取全部品名"""
    data = db_session.query(QualityStandardCenter).all()
    results = list(set(item.Product for item in data))
    return json.dumps({'code': '1000', 'msg': '操作成功', 'data': results}, cls=MyEncoder, ensure_ascii=False)
