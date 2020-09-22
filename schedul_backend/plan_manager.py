from typing import Optional, Any
from collections import Counter
import time
import xlrd
import xlwt
from flask import Blueprint, render_template, send_from_directory
from openpyxl.compat import file
from sqlalchemy.orm import Session, relationship, sessionmaker
from sqlalchemy import create_engine, func
from flask import render_template, request, make_response
import json
import socket
import datetime
from flask_login import login_required, logout_user, login_user,current_user,LoginManager
import re
from sqlalchemy import create_engine, Column, ForeignKey, Table, Integer, String, and_, or_, desc,extract
from io import StringIO
import calendar
from spyne import ServiceBase
import schedul_backend
from common.BSFramwork import AlchemyEncoder
from common.common_cuid import logger,insertSyslog,insert,delete,update,select
import os
import openpyxl
import suds
from suds.client import Client
from datetime import timedelta
import system_backend.Global
from common.batch_plan_model import ProductUnit, ProductRule, PlanManager, ZYPlan, ZYTask, TaskNoGenerator, \
    ZYPlanWMS, ProcessUnit, StapleProducts, WMSTrayNumber, MaterialBOM, SchedulingStock, WMStatusLoad, SchedulePlan, \
    BatchModel
from common.schedul_model import Scheduling, plantCalendarScheduling, SchedulingStandard, \
    scheduledate
from database.connect_db import CONNECT_DATABASE
from enum import Enum, IntEnum, unique

login_manager = LoginManager()
# 创建对象的基类
engine = create_engine(CONNECT_DATABASE)
Session = sessionmaker(bind=engine)
db_session = Session()

batch_plan = Blueprint('batch_plan', __name__)

def getTaskNo():
    bReturn = True
    qry = db_session.query(func.max(TaskNoGenerator.TaskNoInt)).all()
    intTaskNo = int(qry[0][0])
    varTaskNo = str(intTaskNo + 1)
    if len(varTaskNo) == 1:
        varTaskNo = "00000" + varTaskNo
    elif len(varTaskNo) == 2:
        varTaskNo = "0000" + varTaskNo
    if len(varTaskNo) == 3:
        varTaskNo = "000" + varTaskNo
    if len(varTaskNo) == 4:
        varTaskNo = "00" + varTaskNo
    if len(varTaskNo) == 5:
        varTaskNo = "0" + varTaskNo
    else:
        varTaskNo = varTaskNo
    try:
        db_session.add(
            TaskNoGenerator(
                TaskNoInt=intTaskNo + 1,
                TaskNoVar=varTaskNo,
                Desc=""))
        db_session.commit()
        return bReturn,varTaskNo
    except Exception as e:
        bReturn = False
        print(e)
        logger.error(e)
        return  bReturn,varTaskNo

def makeZYPlanZYTask(id):
    try:
        ocalss = db_session.query(PlanManager).filter(PlanManager.ID == id).first()
        if ocalss:
            proclass = db_session.query(ProductUnit).filter(ProductUnit.BrandCode == ocalss.BrandCode).order_by("Seq").all()
            for i in proclass:
                pu = db_session.query(ProcessUnit).filter(ProcessUnit.PUCode == i.PUCode).first()
                zyplan = ZYPlan()
                zyplan.PlanDate = ocalss.PlanBeginTime
                zyplan.PlanNo = ocalss.SchedulePlanCode
                zyplan.BatchID = ocalss.BatchID
                zyplan.PlanSeq = pu.Seq
                zyplan.PUCode = i.PUCode
                zyplan.PlanType = system_backend.Global.PLANTYPE.SCHEDULE.value
                zyplan.BrandCode = ocalss.BrandCode
                zyplan.BrandName = ocalss.BrandName
                zyplan.ERPOrderNo = ""
                zyplan.PlanQuantity = ocalss.PlanQuantity
                zyplan.Unit = ocalss.Unit
                zyplan.EnterTime = ""
                zyplan.PlanBeginTime = ""
                zyplan.ZYPlanStatus = ""
                zyplan.LockStatus = system_backend.Global.TASKLOCKSTATUS.UNLOCK.value
                zyplan.INFStatus = system_backend.Global.TASKSTATUS.NEW.value
                zyplan.WMSStatus = system_backend.Global.TASKSTATUS.NEW.value
                db_session.add(zyplan)
                iTaskSeq = 0
                for j in range(0, pu.RelateTaskCount):
                    iTaskSeq = iTaskSeq + 1
                    bReturn, strTaskNo = getTaskNo()
                    if bReturn == False:
                        return False
                    zytask = ZYTask()
                    zytask.PlanDate = ocalss.PlanBeginTime
                    zytask.TaskID = strTaskNo
                    zytask.BatchID = ocalss.BatchID
                    zytask.PlanSeq = iTaskSeq
                    zytask.PUCode = i.PUCode
                    zytask.PlanType = system_backend.Global.PLANTYPE.SCHEDULE.value
                    zytask.BrandCode = ocalss.BrandCode
                    zytask.BrandName = ocalss.BrandName
                    zytask.PlanQuantity = ocalss.PlanQuantity
                    zytask.Unit = ocalss.Unit
                    zytask.EnterTime = ""
                    # zytask.SetRepeatCount = i.RelateTaskCount
                    zytask.TaskStatus = system_backend.Global.TASKSTATUS.NEW.value
                    zytask.LockStatus = system_backend.Global.TASKLOCKSTATUS.UNLOCK.value
                    db_session.add(zytask)
            db_session.commit()
    except Exception as ee:
        db_session.rollback()
        print(ee)
        logger.error(ee)
        insertSyslog("error", "下发计划生成ZY计划、任务报错Error" + str(ee), current_user.Name)
        return 'NO'

# 计划向导生成计划
@batch_plan.route('/makePlan', methods=['POST', 'GET'])
def makePlan():
    if request.method == 'POST':
        data = request.values  # 返回请求中的参数和form
        try:
            json_str = json.dumps(data.to_dict())
            if len(json_str) > 10:
                BatchID = data.get("BatchID")
                PlanQuantity = data.get("PlanQuantity")
                PlanBeginTime = data.get("PlanBeginTime")
                PlanEndTime = data.get("PlanEndTime")
                Unit = data.get("Unit")
                PlanNum = data.get("PlanNum")
                BrandCode = data.get("BrandCode")
                BrandName = data.get("BrandName")
                BrandType = data.get("BrandType")
                PlanBeginTime = data.get("PlanBeginTime")
                PlanEndTime = data.get("PlanEndTime")
                #批次号判重
                pcBatchID = db_session.query(PlanManager.BatchID).filter(PlanManager.BatchID == BatchID,
                                                                       PlanManager.BrandCode == BrandCode).first()
                if pcBatchID:
                    return json.dumps({"code": "201", "message": "批次号重复！"})
                pm = PlanManager()
                pm.SchedulePlanCode = PlanEndTime[0:10]
                pm.BatchID = BatchID
                pm.PlanQuantity = PlanQuantity
                pm.PlanNum = PlanNum
                pm.Unit = Unit
                pm.BrandCode = BrandCode
                pm.BrandName = BrandName
                pm.PlanStatus = system_backend.Global.PlanStatus.NEW.value
                pm.PlanBeginTime = PlanBeginTime
                pm.PlanEndTime = PlanEndTime
                db_session.add(pm)
                sp = SchedulePlan()
                SchedulePlanCode = PlanEndTime[0:10]
                Desc = system_backend.Global.SCHEDULETYPE.DAY.value
                dEndTime = datetime.datetime.strptime(PlanEndTime[0:10], '%Y-%m-%d') + timedelta(days=1)
                PlanBeginTime = PlanBeginTime
                PlanEndTime = PlanEndTime
                Type = system_backend.Global.SCHEDULETYPE.DAY.value
                db_session.add(sp)
                db_session.commit()
                return json.dumps({"code": "200", "message": "添加成功！"})
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "计划向导生成计划报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
    if request.method == 'GET':
        '''修改批次信息'''
        data = request.values
        try:
            ID = data.get("ID")
            BatchID = data.get("BatchID")
            PlanQuantity = data.get("PlanQuantity")
            PlanBeginTime = data.get("PlanBeginTime")
            PlanEndTime = data.get("PlanEndTime")
            Unit = data.get("Unit")
            ocalss = db_session.query(PlanManager).filter(PlanManager.ID == ID).first()
            if ocalss:
                pl = db_session.query(PlanManager).filter(PlanManager == BatchID).first()
                if not pl:
                    ocalss.BatchID = BatchID
                    ocalss.PlanQuantity = PlanQuantity
                    ocalss.PlanBeginTime = PlanBeginTime
                    ocalss.PlanEndTime = PlanEndTime
                    ocalss.Unit = Unit
                    return json.dumps({"code": "200", "message": "修改成功！"})
                else:
                    return json.dumps({"code": "201", "message": "批次号重复！"})
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "修改批次信息报错Error：" + str(e), current_user.Name)
            return json.dumps("修改批次信息报错", cls=AlchemyEncoder, ensure_ascii=False)
@batch_plan.route('/checkPlanManager', methods=['POST', 'GET'])
def checkPlanManager():
    '''
    审核计划
    :return:
    '''
    if request.method == 'POST':
        data = request.values  # 返回请求中的参数和form
        try:
            PlanStatus = data.get("PlanStatus")
            Describtion = data.get("Describtion")
            ID = data.get("ID")
            oclassplan = db_session.query(PlanManager).filter_by(ID=ID).first()
            oclassplan.PlanStatus = PlanStatus
            oclassplan = Describtion
            db_session.commit()
            return json.dumps({"code": "200", "message": "OK"})
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "审核计划报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

@batch_plan.route('/createZYPlanZYtask', methods=['POST', 'GET'])
def createZYPlanZYtask():
    '''下发计划'''
    if request.method == 'POST':
        data = request.values  # 返回请求中的参数和form
        try:
            jsonstr = json.dumps(data.to_dict())
            if len(jsonstr) > 10:
                PlanStatus = data.get("PlanStatus")
                ID = data.get("ID")
                if PlanStatus == "下发":
                    returnmsg = makeZYPlanZYTask(ID)
                    if (returnmsg == False):
                        return json.dumps({"code": "500", "message": "下发失败！"})
                    oclassplan = db_session.query(PlanManager).filter_by(ID=ID).first()
                    oclassplan.PlanStatus = system_backend.Global.PlanStatus.Realse.value
                    db_session.commit()
                    return json.dumps({"code": "200", "message": "下发成功！！"})
                else:
                    oclassplan = db_session.query(PlanManager).filter_by(ID=ID).first()
                    oclassplan.PlanStatus = system_backend.Global.PlanStatus.Realse.value
                    db_session.commit()
                    return json.dumps({"code": "200", "message": "撤回成功！！"})
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "下发计划生成ZY计划、任务报错Error：" + str(e), current_user.Name)
            return 'NO'


ALLOWED_EXTENSIONS = ['doc','docx']
def allowe_file(filename):
    '''
    限制上传的文件格式
    :param filename:
    :return:
    '''
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
@batch_plan.route('/batchmodelexport', methods=['GET', 'POST'])
def batchmodelexport():
    '''批记录模板导入'''
    if request.method == 'POST':
        try:
            file = request.files['file']
            file_path = os.path.join(os.path.realpath(r"system_backend\SystemManagement\files"), file.filename)
            if allowe_file(file_path) == True:
                file.save(file_path)
                return json.dumps({"code": "200", "message": "上传成功！"})
            else:
                return json.dumps({"code": "200", "message": "请上传.doc或.docx！"})

        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "批记录模板导入报错Error：" + str(e), current_user.Name)
            return json.dumps({"code": "500", "message": "后端报错"})
@batch_plan.route('/batchmodelinsert', methods=['GET', 'POST'])
def batchmodelinsert():
    '''批记录模板名称路径储存'''
    if request.method == 'POST':
        data = request.values
        try:
            BrandName = data.get("BrandName")
            PUCode = data.get("PUCode")
            BrandCode = data.get("BrandCode")
            PUIDName = data.get("PUIDName")
            FileName = data.get("FileName")
            #删除之前存的
            oclass = db_session.query(BatchModel).filter(BatchModel.BrandCode == BrandCode,
                                                         BatchModel.PUCode == PUCode).all()
            for oc in oclass:
                db_session.delete(oc)
                os.remove(oc.FilePath)
            db_session.commit()
            #新添加的
            bm = BatchModel()
            bm.BrandName = BrandName
            bm.PUCode = PUCode
            bm.BrandCode = BrandCode
            bm.PUIDName = PUIDName
            bm.FileName = FileName
            bm.FilePath = os.path.join(os.path.realpath(r"system_backend\SystemManagement\files"), FileName)
            bm.UserName = current_user.Name
            db_session.add(bm)
            db_session.commit()
            return json.dumps({"code": "200", "message": "上传成功！"})
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "批记录模板导入报错Error：" + str(e), current_user.Name)
            return json.dumps({"code": "500", "message": "后端报错"})
@batch_plan.route('/batchmodelselect', methods=['GET', 'POST'])
def batchmodelselect():
    '''查询批记录模'''
    if request.method == 'GET':
        data = request.values
        try:
            PUCode = data.get("PUCode")
            BrandCode = data.get("BrandCode")
            oclass = db_session.query(BatchModel).filter(BatchModel.BrandCode == BrandCode, BatchModel.PUCode == PUCode).all()
            dir_list = []
            for oc in oclass:
                dir = {}
                dir["ID"] = oc.ID
                dir["FilePath"] = oc.FilePath
                dir["FileName"] = oc.FileName
                dir_list.append(dir)
            return json.dumps({"code": "200", "message": dir_list})
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "查询批记录模报错Error：" + str(e), current_user.Name)
            return json.dumps({"code": "500", "message": "后端报错"})
@batch_plan.route('/ManualDelete', methods=['GET', 'POST'])
def ManualDelete():
    '''批记录模板删除'''
    if request.method == 'POST':
        data = request.values  # 返回请求中的参数和form
        try:
            jsonstr = json.dumps(data.to_dict())
            if len(jsonstr) > 10:
                jsonnumber = re.findall(r"\d+\.?\d*", jsonstr)
                for key in jsonnumber:
                    id = int(key)
                    try:
                        oclass = db_session.query(BatchModel).filter(
                            BatchModel.ID == id).first()
                        if oclass:
                            db_session.delete(oclass)
                            os.remove(oclass.FilePath)
                    except Exception as ee:
                        db_session.rollback()
                        print(ee)
                        logger.error(ee)
                        return json.dumps({"code": "500", "message": "批记录模板删除报错"})
                db_session.commit()
                return json.dumps({"code": "200", "message": "删除成功！"})
            else:
                return json.dumps({"code": "200", "message": "id为空！"})
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "路由：/ManualDelete，说明书删除Error：" + str(e), current_user.Name)
            return json.dumps({"code": "500", "message": "批记录模板删除报错"})