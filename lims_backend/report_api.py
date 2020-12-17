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
            query_data = db_session.query(WorkerBook).filter_by(CheckProjectNO=request.values.get('CheckProjectNO')).all()
            return json.dumps({'code': '1000', 'msg': '操作成功', 'data': query_data}, cls=MyEncoder, ensure_ascii=False)
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
            if Action == '2':
                data1.QC = 'Y'
            if Action == '3':
                data1.QA = 'Y'
            if Action == '4':
                data1.QS = 'Y'
                data.Life = '放行'
            db_session.add_all([data1, data])
            db_session.commit()
            db_session.add(
                CheckLife(No=CheckProjectNO, User=Name, Status="审核", Product=data.Name, CheckNumber=data.CheckNumber,
                          ProductType=data.ProductType, OperationTime=Time, Work="完成了审核"))
            db_session.commit()
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)}, cls=MyEncoder)

