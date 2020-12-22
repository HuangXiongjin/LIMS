import json
from datetime import datetime

from flask import Blueprint, request

from tools.handle import MyEncoder, log, get_short_id, get_uuid
from common.lims_models import db_session, ClassifyTree, QualityStandardCenter, QualityStandard, CheckForm, \
    CheckProject, Distribute, ProductSave, CheckLife, Worker, Record, WorkerBook, ConclusionRecord, ReportVerify

report = Blueprint('report', __name__)


@report.route('/QualityTesting', methods=['GET', 'POST'])
def quality_testing():
    """质检报告检测"""
    try:
        if request.method == 'GET':
            name = request.values.get('Name')
            query_work = db_session.query(WorkerBook).filter_by(Name=name).first()
            query_data = db_session.query(WorkerBook).filter_by(CheckProjectNO=query_work.CheckProjectNO).all()
            check_data = set(item.CheckType for item in query_data)
            results = []
            for item in check_data:
                query_data = db_session.query(WorkerBook).filter_by(CheckProjectNO=query_work.CheckProjectNO, CheckType=item).all()
                child = []
                parent = {'CheckType': item, 'values': child}
                for i in query_data:
                    # parent = {'CheckType': item, 'Id': i.Id, 'Name': i.Name, 'work': i.CheckProject}
                    child.append({'Id': i.Id, 'Name': i.Name, 'work': i.CheckProject})
                results.append(parent)
            # check_data = [{"name": item.Name, "work": item.CheckProject} for item in query_data]
            return json.dumps({'code': '1000', 'msg': '操作成功', 'data': results}, cls=MyEncoder, ensure_ascii=False)
        if request.method == 'POST':
            NO = request.values.get('CheckProjectNO')
            Name = request.values.get('Name')
            CheckEndTime = request.values.get('CheckEndTime')
            Id = int(request.values.get('Id'))
            Action = '符合规定' if request.values.get('Action') == 'Y' else '不符合规定'
            Comment = request.values.get('Comment')
            data = db_session.query(WorkerBook).filter_by(Id=Id).first()
            query_check = db_session.query(CheckForm).filter_by(Id=Id).first()
            query_data = db_session.query(Distribute).filter_by(CheckProjectNO=NO).first()
            # query_WorkerBook = db_session.query(WorkerBook).filter_by(Id=Id).first()
            query_record = db_session.query(Record).filter_by(CheckProjectNO=request.values.get('CheckProjectNO')).first()
            data.Result = '符合规定'
            data.CheckEndTime = CheckEndTime
            data.Comment = Comment
            db_session.add_all(data)
            db_session.commit()
            db_session.add(
                CheckLife(No=NO, User=Name, Status="质检", Product=data.Name, CheckNumber=data.CheckNumber,
                          ProductType=data.ProductType, OperationTime=CheckEndTime, Work="完成了单项质检"))
            db_session.commit()
            db_session.add(ConclusionRecord(CheckNumber=query_check.Foo, TestDate=query_check.CheckDate,
                                            ActualTime=query_check.SampleTime, CheckDate=query_data.Time,
                                            Name=query_check.Name, ProductNumber=query_check.ProductNumber,
                                            SampleDepartment=query_check.CheckDepartment, Type=query_check.ProductType,
                                            medicine=query_record.Type, Specs=query_check.Specs, CheckProject=data.CheckProject,
                                            Judge=Action, CheckName=data.Name))
            db_session.commit()
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)}, cls=MyEncoder)


@report.route('/Report', methods=['GET', 'POST'])
def check_report():
    """报告审核"""
    try:
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
            db_session.add_all([data1, data])
            db_session.commit()
            db_session.add(
                CheckLife(No=CheckProjectNO, User=Name, Status="审核", Product=data.Name, CheckNumber=data.CheckNumber,
                          ProductType=data.ProductType, OperationTime=Time, Work="完成了审核"))
            db_session.commit()
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)}, cls=MyEncoder)


@report.route('/CheckLog', methods=['GET', 'POST'])
def check_log():
    try:
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
            results = db_session.query(CheckLife).filter(CheckLife.Product==Product, CheckLife.ProductType == ProductType
                                                         ).order_by(CheckLife.Id.desc()).all()
            data = results[(page - 1) * per_page:page * per_page]
            return json.dumps({'code': '1000', 'msg': '成功', 'data': data, 'total': len(results)}, cls=MyEncoder,
                              ensure_ascii=False)
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)}, cls=MyEncoder)


@report.route('/Board', methods=['GET'])
def board():
    try:
        if request.method == 'GET':
            if request.values.get('Action') == 'p':
                CheckProjectNO = request.values.get('CheckProjectNO')
                results = db_session.query(CheckLife).filter_by(No=CheckProjectNO).all()
                return json.dumps({'code': '1000', 'msg': '成功', 'data': results}, cls=MyEncoder, ensure_ascii=False)
            # 当前页码
            page = int(request.values.get('Page'))
            # 每页记录数
            per_page = int(request.values.get('PerPage'))
            status = request.values.get('Status')
            Product = request.values.get('Product')
            results = db_session.query(CheckLife.No).filter_by(Product=Product, Status=status).all()
            data = []
            for result in results:
                for item in result:
                    query_data = db_session.query(CheckForm).filter_by(CheckProjectNO=item).first()
                    if query_data is not None:
                        data.append(query_data)
            result_data = data[(page - 1) * per_page:page * per_page]
            return json.dumps({'code': '1000', 'msg': '成功', 'data': result_data, 'total': len(data)}, cls=MyEncoder,
                              ensure_ascii=False)
        if request.method == 'POST':
            no_array = json.loads(request.values.get('CheckProjectNO'))
            data = []
            for item in no_array:
                query_data = db_session.query(CheckForm).filter_by(CheckProjectNO=item).first()
                if query_data is not None:
                    data.append(query_data)
            return json.dumps({'code': '1000', 'msg': '成功', 'data': data}, cls=MyEncoder, ensure_ascii=False)
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)}, cls=MyEncoder)


@report.route('/Test', methods=['GET', 'POST'])
def test():
    try:
        if request.method == 'GET':
            # 当前页码
            page = int(request.values.get('Page'))
            # 每页记录数
            per_page = int(request.values.get('PerPage'))
            table_name = request.values.get('TableName')
            sql = f"select * from {table_name} order by Id offset {(page-1)*per_page} rows fetch next {page*per_page} rows only"
            results = db_session.execute(sql).fetchall()
            data = [dict(zip(result.keys(), result)) for result in results]
            # pass
            print(data)
            return json.dumps({'code': '1000', 'msg': '成功', 'data': data, 'total': 'len(results)'}, cls=MyEncoder,
                              ensure_ascii=False)
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)}, cls=MyEncoder)
