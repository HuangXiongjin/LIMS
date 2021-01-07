import json
from datetime import datetime

from flask import Blueprint, request

from tools.handle import MyEncoder, log, get_short_id, get_uuid
from common.lims_models import db_session, ClassifyTree, QualityStandardCenter, QualityStandard, CheckForm, \
    CheckProject, Distribute, ProductSave, CheckLife, Worker, Record, WorkerBook, ConclusionRecord, ReportVerify, \
    DestructionForm

report = Blueprint('report', __name__)


@report.route('/QualityTesting', methods=['GET', 'POST'])
def quality_testing():
    """质检报告检测"""
    if request.method == 'GET':
        name = request.values.get('Name')
        CheckProjectNO = request.values.get('CheckProjectNO')
        query_data = db_session.query(WorkerBook).filter_by(CheckProjectNO=CheckProjectNO).all()

        check_data = set(item.CheckType for item in query_data)
        results = []
        for item in check_data:
            child = []
            parent = {'CheckType': item, 'values': child}
            query_data2 = db_session.query(WorkerBook).filter_by(CheckProjectNO=CheckProjectNO, CheckType=item).all()
            for i in query_data2:
                child.append({'ID': i.ID, 'Name': i.Name, 'work': i.CheckProject, 'Status': i.Status})
            results.append(parent)
        return json.dumps({'code': '1000', 'msg': '操作成功', 'data': results}, cls=MyEncoder, ensure_ascii=False)
    if request.method == 'POST':
        NO = request.values.get('CheckProjectNO')
        Name = request.values.get('Name')
        Isopt = request.values.get('Isopt')
        CheckEndTime = request.values.get('CheckEndTime')
        Action = json.loads(request.values.get('Action', '[]'))
        Comment = request.values.get('Comment', '')
        for item in Action:
            if item is not None:
                data = db_session.query(WorkerBook).filter_by(ID=int(item['ID'])).first()
                result = '符合规定' if item['Status'] == 'true' else '不符合规定'
                data.Result = result
                data.Status = item['Status']
                data.CheckEndTime = CheckEndTime
                data.Comment = Comment
                data.Isopt = Isopt
                db_session.add(data)
                db_session.commit()
                query_check = db_session.query(CheckForm).filter_by(CheckProjectNO=NO).first()
                query_data = db_session.query(Distribute).filter_by(CheckProjectNO=NO).first()
                # query_WorkerBook = db_session.query(WorkerBook).filter_by(ID=ID).first()
                query_record = db_session.query(Record).filter_by(
                    CheckProjectNO=request.values.get('CheckProjectNO')).first()
                db_session.add(
                    CheckLife(CheckProjectNO=NO, CheckUser=Name, Status="质检", Product=data.Name, CheckNumber=query_check.CheckNumber,
                              ProductType=query_check.ProductType, CheckDate=CheckEndTime, Content="完成了质检内容"))
                db_session.commit()
                db_session.add(ConclusionRecord(CheckNumber=query_check.Foo, TestDate=query_check.CheckDate,
                                                ActualTime=query_check.SampleTime, CheckDate=query_data.Time,
                                                Name=query_check.Name, ProductNumber=query_check.ProductNumber,
                                                SampleDepartment=query_check.CheckDepartment,
                                                Type=query_check.ProductType,
                                                medicine=query_record.Type, Specs=query_check.Specs,
                                                CheckProject=data.CheckProject,
                                                Judge=result, CheckName=data.Name))
                db_session.commit()
        result = db_session.query(WorkerBook).filter_by(CheckProjectNO=NO, Isopt='N').all()
        if len(result) == 0:
            query_check = db_session.query(CheckForm).filter_by(CheckProjectNO=NO).first()
            query_check.Status = '报告'
            db_session.add(query_check)
            db_session.commit()
        return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)


@report.route('/Report', methods=['GET', 'POST'])
def check_report():
    """报告审核"""
    # if request.method == 'GET':
    #
    #     pass
    if request.method == 'POST':
        CheckProjectNO = request.values.get('CheckProjectNO')
        Name = request.values.get('Name')
        Action = request.values.get('Action')
        data1 = db_session.query(ReportVerify).filter_by(CheckProjectNO=CheckProjectNO).first()
        Time = request.values.get('Time')
        data = db_session.query(CheckForm).filter_by(CheckProjectNO=CheckProjectNO).first()
        if Action == '1':
            data1.laboratory = 'Y'
            data.Life = '质检审核'
            data.Status = '质检审核'
            db_session.add(
                CheckLife(CheckProjectNO=CheckProjectNO, CheckUser=Name, Status="质检审核", Product=data.Name,
                          CheckNumber=data.CheckNumber,
                          ProductType=data.ProductType, CheckDate=Time, Content="完成质检了审核"))
            db_session.commit()
        if Action == '2':
            data1.QC = 'Y'
            data.Life = '质检审核'
            data.Status = '质检审核'
        if Action == '3':
            data1.QA = 'Y'
            data.Life = '质检审核'
            data.Status = '质检审核'
        if Action == '4':
            data1.QS = 'Y'
            data.Life = '放行'
            data.Status = '放行'
            db_session.add(
                CheckLife(CheckProjectNO=CheckProjectNO, CheckUser=Name, Status="放行", Product=data.Name,
                          CheckNumber=data.CheckNumber,
                          ProductType=data.ProductType, CheckDate=Time, Content="完成了审核放行"))
            db_session.commit()
        db_session.add_all([data1, data])
        db_session.commit()
        return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)


@report.route('/CheckLog', methods=['GET', 'POST'])
def check_log():
    if request.method == 'GET':
        # 当前页码
        page = int(request.values.get('Page'))
        # 每页记录数
        per_page = int(request.values.get('PerPage'))
        # status = request.values.get('Status')
        Product = request.values.get('Product')
        ProductType = request.values.get('ProductType')
        # start_time = "'" + request.values.get('DateTime') + " 00:00:00'"
        # end_time = "'" + request.values.get('DateTime') + " 23:59:59'"
        name = request.values.get('Name')
        if name is None:
            results = db_session.query(CheckLife).filter(CheckLife.Product == Product, CheckLife.ProductType == ProductType
                                                     ).order_by(CheckLife.ID.desc()).all()
        else:
            results = db_session.query(CheckLife).filter(CheckLife.CheckUser == name).order_by(CheckLife.ID.desc()).all()
        data = results[(page - 1) * per_page:page * per_page]
        return json.dumps({'code': '1000', 'msg': '成功', 'data': data, 'total': len(results)}, cls=MyEncoder,
                          ensure_ascii=False)


@report.route('/Board', methods=['GET'])
def board():
    """功能看板"""
    if request.method == 'GET':
        if request.values.get('Action') == 'p':
            CheckProjectNO = request.values.get('CheckProjectNO')
            if CheckProjectNO:
                status_list = ['申请', '请验审核', '取样', '接收', '分发', '质检', '报告', '质检审核', '放行']
                data = []
                results = db_session.query(CheckLife).filter_by(CheckProjectNO=CheckProjectNO).all()
                for result in results:
                    if results.Status in status_list:
                        data.append(result)
                return json.dumps({'code': '1000', 'msg': '成功', 'data': results}, cls=MyEncoder, ensure_ascii=False)
            else:
                return json.dumps({'code': '1000', 'msg': '成功'}, cls=MyEncoder, ensure_ascii=False)
        # 当前页码
        page = int(request.values.get('Page'))
        # 每页记录数
        per_page = int(request.values.get('PerPage'))
        status = request.values.get('Status')
        Product = request.values.get('Product')
        results = db_session.query(CheckForm).filter(CheckForm.Product == Product, CheckForm.Status == status).order_by(
            CheckForm.ID.desc()).all()
        data = results[(page - 1) * per_page:page * per_page]
        return json.dumps({'code': '1000', 'msg': '成功', 'data': data, 'total': len(results)}, cls=MyEncoder,
                          ensure_ascii=False)
    if request.method == 'POST':
        no_array = json.loads(request.values.get('CheckProjectNO'))
        data = []
        for item in no_array:
            query_data = db_session.query(CheckForm).filter_by(CheckProjectNO=item).first()
            if query_data is not None:
                data.append(query_data)
        return json.dumps({'code': '1000', 'msg': '成功', 'data': data}, cls=MyEncoder, ensure_ascii=False)


@report.route('/Destruction', methods=['GET', 'POST'])
def destruction():
    if request.method == 'POST':
        # (留样销毁 - 样品销毁)
        destruction_type = request.values.get('DestructionType')
        items = json.loads(request.values.get('CheckProjectNO'))
        if destruction_type == '样品销毁':
            for item in items:
                data = db_session.query(CheckForm).filter_by(CheckProjectNO=item).first()
                data.ProductDestruction = '样品销毁'
                db_session.add(data)
                db_session.commit()
        if destruction_type == '留样销毁':
            for item in items:
                data = db_session.query(ProductSave).filter_by(CheckProjectNO=item).first()
                data.BatchDestruction = '留样销毁'
                db_session.add(data)
                db_session.commit()
        return json.dumps({'code': '1000', 'msg': '成功'}, cls=MyEncoder, ensure_ascii=False)

    if request.method == 'GET':
        # (留样销毁 - 样品销毁)
        destruction_type = request.values.get('DestructionType')
        # 当前页码
        page = int(request.values.get('Page'))
        # 每页记录数
        per_page = int(request.values.get('PerPage'))
        Product = request.values.get('Product')
        # now_time = datetime.today()
        # print(now_time)
        # StartTime = request.values.get('StartTime')
        # EndTime = request.values.get('EndTime')
        results = ''
        if destruction_type == '样品销毁':
            results = db_session.query(CheckForm).filter(CheckForm.Product == Product,
                                                         CheckForm.ProductDestruction == '样品销毁').order_by(
                CheckForm.ID.desc()).all()
        if destruction_type == '留样销毁':
            results = db_session.query(ProductSave).filter(ProductSave.Name == Product,
                                                           ProductSave.BatchDestruction == '留样销毁').order_by(
                ProductSave.ID.desc()).all()
        data = results[(page - 1) * per_page:page * per_page]
        return json.dumps({'code': '1000', 'msg': '成功', 'data': data, 'total': len(results)}, cls=MyEncoder,
                          ensure_ascii=False)


@report.route('/DestructionVerify', methods=['GET', 'POST'])
def destruction_verify():
    """销毁审核"""
    if request.method == 'GET':
        # (留样销毁 - 样品销毁)
        destruction_type = request.values.get('DestructionType')
        # 当前页码
        page = int(request.values.get('Page'))
        # 每页记录数
        per_page = int(request.values.get('PerPage'))
        Product = request.values.get('Product')
        # StartTime = request.values.get('StartTime')
        # EndTime = request.values.get('EndTime')
        results = ''
        if destruction_type == '样品销毁':
            results = db_session.query(DestructionForm).filter(DestructionForm.Name == Product,
                                                               DestructionForm.Type == '样品销毁').order_by(
                DestructionForm.ID.desc()).all()
        if destruction_type == '留样销毁':
            results = db_session.query(DestructionForm).filter(DestructionForm.Name == Product,
                                                               DestructionForm.Type == '留样销毁').order_by(
                DestructionForm.ID.desc()).all()
        data = results[(page - 1) * per_page:page * per_page]
        return json.dumps({'code': '1000', 'msg': '成功', 'data': data, 'total': len(results)}, cls=MyEncoder,
                          ensure_ascii=False)
    if request.method == 'POST':
        destruction_type = request.values.get('DestructionType')
        CheckProjectNO = request.values.get('CheckProjectNO')
        data = db_session.query(CheckForm).filter_by(CheckProjectNO=CheckProjectNO).first()
        if request.values.get('Isopt') == 'Y':
            data2 = DestructionForm()
            data2.CheckNumber = data.CheckNumber
            data2.ProductType = data.ProductType
            data2.Name = data.Name
            data2.Specs = data.Specs
            data2.Supplier = data.Supplier
            data2.ProductNumber = data.ProductNumber
            data2.Number = data.Number
            data2.Amount = data.Amount
            data2.Unit = data.Unit
            data2.CheckProcedure = data.CheckProcedure
            data2.CheckDepartment = data.CheckDepartment
            data2.CheckDate = data.CheckDate
            data2.CheckUser = data.CheckUser
            data2.DestructionTime = datetime.today().strftime('%Y-%m-%d')
            if destruction_type == '样品销毁':
                data = db_session.query(CheckForm).filter_by(CheckProjectNO=CheckProjectNO).first()
                data.ProductDestruction = '已销毁'
                data2.Type = '样品销毁'
            if destruction_type == '留样销毁':
                data = db_session.query(ProductSave).filter_by(CheckProjectNO=CheckProjectNO).first()
                data.BatchDestruction = '已销毁'
                data2.Type = '留样销毁'
            db_session.add_all([data, data2])
            db_session.commit()
            return json.dumps({'code': '1000', 'msg': '成功'}, cls=MyEncoder, ensure_ascii=False)
        else:
            if destruction_type == '样品销毁':
                data = db_session.query(CheckForm).filter_by(CheckProjectNO=CheckProjectNO).first()
                data.ProductDestruction = '未销毁'
            if destruction_type == '留样销毁':
                data = db_session.query(ProductSave).filter_by(CheckProjectNO=CheckProjectNO).first()
                data.BatchDestruction = '未销毁'
            db_session.add(data)
            db_session.commit()
            return json.dumps({'code': '1000', 'msg': '成功'}, cls=MyEncoder, ensure_ascii=False)
