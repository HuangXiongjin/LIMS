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
    ZYPlanWMS, ProcessUnit, StapleProducts, WMSTrayNumber, MaterialBOM, SchedulingStock, WMStatusLoad, SchedulePlan
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
                PlanQuantity = data.get('PlanQuantity')  # 计划重量
                PlanDate = data.get('PlanDate')  # 计划生产日期
                BatchID = data.get('BatchID')  # 批次号
                BrandCode = data.get('BrandCode')
                BrandName = data.get('BrandName')  # 产品名称
                BrandCode = data.get("BrandCode")
                PLineName = data.get('PLineName')  # 生产线名字
                Unit = data.get('Unit') # d单位
                pm = PlanManager()
                pm.SchedulePlanCode = PlanDate
                pm.BatchID = BatchID
                pm.PlanQuantity = PlanQuantity
                pm.Unit = Unit
                pm.BrandCode = BrandCode
                pm.BrandName = BrandName
                pm.PlanStatus = system_backend.Global.PlanStatus.NEW.value
                pm.PlanBeginTime = datetime.datetime.now().strptime('%Y-%m-%d %H:%M:%S')
                pm.PlanEndTime = ""
                db_session.add(pm)
                sp = SchedulePlan()
                SchedulePlanCode = PlanDate
                Desc = system_backend.Global.SCHEDULETYPE.DAY.value
                dEndTime = datetime.strptime(PlanDate, '%Y-%m-%d') + timedelta(days=1)
                PlanBeginTime =str(PlanDate) + " " + system_backend.Global.GLOBAL_PLANSTARTTIME
                PlanEndTime = dEndTime.strftime('%Y-%m-%d') + " " + system_backend.Global.GLOBAL_PLANENDTIME
                Type = system_backend.Global.SCHEDULETYPE.DAY.value
                db_session.add(sp)
                db_session.commit()
                return json.dumps({"code": "200", "message": "OK"})
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "计划向导生成计划报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

@batch_plan.route('/checkPlanManager', methods=['POST', 'GET'])
def checkPlanManager():
    '''
    审核计划
    :return:
    '''
    if request.method == 'POST':
        data = request.values  # 返回请求中的参数和form
        try:
            jsonstr = json.dumps(data.to_dict())
            CheckStatus = data.get("CheckStatus")
            Describtion = data.get("Describtion")
            if len(jsonstr) > 10:
                jsonnumber = re.findall(r"\d+\.?\d*", jsonstr)
                for key in jsonnumber:
                    id = int(key)
                    try:
                        oclassplan = db_session.query(PlanManager).filter_by(ID=id).first()
                        if CheckStatus == "通过":
                            oclassplan.PlanStatus = system_backend.Global.PlanStatus.Checked.value
                        elif CheckStatus == "不通过":
                            oclassplan.PlanStatus = system_backend.Global.PlanStatus.UnChecked.value
                            oclassplan = Describtion
                        db_session.commit()
                    except Exception as ee:
                        db_session.rollback()
                        print(ee)
                        logger.error(ee)
                        insertSyslog("error", "生产管理部审核计划报错Error：" + str(ee), current_user.Name)
                        return json.dumps([{"status": "Error:" + str(ee)}], cls=AlchemyEncoder, ensure_ascii=False)
                return json.dumps({"code": "200", "message": "OK"})
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "生产管理部审核计划报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

@batch_plan.route('/createZYPlanZYtask', methods=['POST', 'GET'])
def createZYPlanZYtask():
    '''下发计划'''
    if request.method == 'GET':
        data = request.values  # 返回请求中的参数和form
        try:
            jsonstr = json.dumps(data.to_dict())
            if len(jsonstr) > 10:
                jsonnumber = re.findall(r"\d+\.?\d*", jsonstr)
                for key in jsonnumber:
                    id = int(key)
                    try:
                        returnmsg = makeZYPlanZYTask(id)
                        if (returnmsg == False):
                            return 'NO'
                        return "成功"
                        oclassplan = db_session.query(PlanManager).filter_by(ID=id).first()
                        oclassplan.PlanStatus = system_backend.Global.PlanStatus.Realse.value
                        oclassZYPlans = db_session.query(ZYPlan).filter(ZYPlan.BatchID == oclassplan.BatchID).all()
                        for zyp in oclassZYPlans:
                            zyp.ZYPlanStatus = system_backend.Global.ZYPlanStatus.Realse.value
                        oclassZYTasks = db_session.query(ZYTask).filter(ZYTask.BatchID == oclassplan.BatchID).all()
                        for task in oclassZYTasks:
                            task.TaskStatus = system_backend.Global.TASKSTATUS.Realse.value
                        userName = current_user.Name
                        oclassNodeColl = db_session.query(schedul_backend.node.NodeCollection).filter_by(oddNum=id,
                                                                                               name="计划下发").first()
                        oclassNodeColl.status = system_backend.node.NodeStatus.PASSED.value
                        oclassNodeColl.oddUser = userName
                        oclassNodeColl.opertionTime = datetime.datetime.now()
                        oclassNodeColl.seq = 2

                        #新加WMS仓库工艺段
                        wms = ZYPlanWMS()
                        wms.BatchID = oclassplan.BatchID
                        wms.BrandName = oclassplan.BrandName
                        wms.BrandID = oclassplan.BrandID
                        wms.PUIDName = 'WMS'
                        wms.ExcuteStatus = '0'
                        wms.IsSend = '0'
                        wms.OperationDate = datetime.datetime.now()
                        wms.OperationPeople = userName
                        db_session.add(wms)

                        db_session.commit()
                    except Exception as ee:
                        db_session.rollback()
                        print(ee)
                        logger.error(ee)
                        insertSyslog("error", "下发计划生成ZY计划、任务报错Error" + str(ee), current_user.Name)
                        return 'NO'
                return 'OK'
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "下发计划生成ZY计划、任务报错Error：" + str(e), current_user.Name)
            return 'NO'


