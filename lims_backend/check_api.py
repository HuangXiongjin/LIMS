import json
from datetime import datetime

from flask import Blueprint, request

from tools.handle import MyEncoder, log, get_short_id, get_uuid
from common.lims_models import db_session, ClassifyTree, QualityStandardCenter, QualityStandard, CheckForm, CheckProject

check = Blueprint('check', __name__)


@check.route('/CheckForm', methods=['POST'])
def check_form():
    """样品请检申请"""
    try:
        data = request.values
        CheckNumber = data.get('CheckNumber')
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
                                 CheckProjectNO=CheckProjectNO, CheckNumber=CheckNumber))
        db_session.commit()

        json_data = json.loads(check_project)
        for result in json_data:
            print(result)
            if result == '项目':
                for item in json_data[result]:
                    c = CheckProject()
                    c.No = CheckNumber
                    c.Product = Name
                    c.Project = item
                    db_session.add(c)
                    db_session.commit()
            if result == '性状':
                for item in json_data[result]:
                    c = CheckProject()
                    c.No = CheckNumber
                    c.Product = Name
                    c.Character = item
                    db_session.add(c)
                    db_session.commit()
            if result == '鉴别':
                data = []
                for item in json_data[result]:
                    c = CheckProject()
                    c.No = CheckNumber
                    c.Product = Name
                    c.Discern = item
                    data.append(c)
                db_session.add_all(data)
                db_session.commit()
            if result == '检查':
                for item in json_data[result]:
                    c = CheckProject()
                    c.No = CheckNumber
                    c.Product = Name
                    c.Inspect = item
                    db_session.add(c)
                    db_session.commit()
            if result == '含量测定':
                for item in json_data[result]:
                    c = CheckProject()
                    c.No = CheckNumber
                    c.Product = Name
                    c.Content = item
                    db_session.add(c)
                    db_session.commit()
            if result == '微生物限定':
                for item in json_data[result]:
                    c = CheckProject()
                    c.No = CheckNumber
                    c.Product = Name
                    c.Microbe = item
                    db_session.add(c)
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
