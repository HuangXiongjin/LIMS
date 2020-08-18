from typing import Optional, Any
from collections import Counter
import time

import self as self
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

import schedul_backend
from common.BSFramwork import AlchemyEncoder
from common.common_cuid import logger,insertSyslog,insert,delete,update,select
import os
import openpyxl
import suds
from suds.client import Client
from datetime import timedelta

from common.batch_plan_model import ProductUnit, ProductRule, PlanManager, ZYPlan, ZYTask, TaskNoGenerator, \
    ZYPlanWMS
from common.schedul_model import Scheduling, plantCalendarScheduling, ERPproductcode_prname, SchedulingStandard, \
    product_plan, scheduledate
from database.connect_db import CONNECT_DATABASE
from enum import Enum, IntEnum, unique

login_manager = LoginManager()
# 创建对象的基类
engine = create_engine(CONNECT_DATABASE)
Session = sessionmaker(bind=engine)
db_session = Session()

batch_plan = Blueprint('batch_plan', __name__)

def getTaskNo(self):
    bReturn = True
    qry = db_session.query(func.max(TaskNoGenerator.TaskNoInt)).all();
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
            productunit_class = db_session.query(ProductUnit).filter(ProductUnit.ProductRuleID == ocalss.ProductRuleID).order_by().first()
            for i in productunit_class:
                zyplan = ZYPlan()
                zyplan.PlanDate = i.PlanDate
                zyplan.PlanNo = i.PlanNo
                zyplan.BatchID = ocalss.BatchID
                zyplan.PlanSeq = i.Seq
                zyplan.PUID = i.PUID
                zyplan.PlanType = "调度计划"
                zyplan.BrandID = ocalss.BrandID
                zyplan.BrandName = ocalss.BrandName
                zyplan.ERPOrderNo = ""
                zyplan.PlanQuantity = ocalss.PlanQuantity
                zyplan.Unit = ocalss.Unit
                zyplan.EnterTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                zyplan.PlanBeginTime = ocalss.PlanBeginTime
                zyplan.ZYPlanStatus = schedul_backend.Global.ZYPlanStatus.NEW.value
                zyplan.LockStatus = schedul_backend.Global.TASKLOCKSTATUS.UNLOCK.value
                zyplan.INFStatus = schedul_backend.Global.TASKSTATUS.NEW.value
                zyplan.WMSStatus = schedul_backend.Global.TASKSTATUS.NEW.value
                db_session.add(zyplan)
                iTaskSeq = 0
                for j in range(0, i.RelateTaskCount):
                    iTaskSeq = iTaskSeq + 1
                    bReturn, strTaskNo = getTaskNo()
                    if bReturn == False:
                        return False
                    zytask = ZYTask()
                    zytask.PlanDate = i.PlanDate
                    zytask.TaskID = strTaskNo
                    zytask.BatchID = ocalss.BatchID
                    zytask.PlanSeq = iTaskSeq
                    zytask.PUID = i.PUID
                    zytask.PlanType = schedul_backend.Global.PLANTYPE.SCHEDULE.value
                    zytask.BrandID = ocalss.BrandID
                    zytask.BrandName = ocalss.BrandName
                    zytask.PlanQuantity = ocalss.PlanQuantity
                    zytask.Unit = ocalss.Unit
                    zytask.EnterTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    zytask.SetRepeatCount = i.RelateTaskCount
                    zytask.TaskStatus = schedul_backend.Global.TASKSTATUS.NEW.value
                    zytask.LockStatus = schedul_backend.Global.TASKLOCKSTATUS.UNLOCK.value
                    zytask.db_session.add(zytask)
            db_session.commit()
    except Exception as ee:
        db_session.rollback()
        print(ee)
        logger.error(ee)
        insertSyslog("error", "下发计划生成ZY计划、任务报错Error" + str(ee), current_user.Name)
        return 'NO'

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
                        oclassplan = db_session.query(PlanManager).filter_by(ID=id).first()
                        oclassplan.PlanStatus = schedul_backend.Global.PlanStatus.Realse.value
                        oclassZYPlans = db_session.query(ZYPlan).filter(ZYPlan.BatchID == oclassplan.BatchID).all()
                        for zyp in oclassZYPlans:
                            zyp.ZYPlanStatus = schedul_backend.Global.ZYPlanStatus.Realse.value
                        oclassZYTasks = db_session.query(ZYTask).filter(ZYTask.BatchID == oclassplan.BatchID).all()
                        for task in oclassZYTasks:
                            task.TaskStatus = schedul_backend.Global.TASKSTATUS.Realse.value
                        userName = current_user.Name
                        oclassNodeColl = db_session.query(schedul_backend.node.NodeCollection).filter_by(oddNum=id,
                                                                                               name="计划下发").first()
                        oclassNodeColl.status = schedul_backend.node.NodeStatus.PASSED.value
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
