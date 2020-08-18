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

from common.electric_batch_record import ProductUnit, ProductRule, PlanManager, ZYPlan, ZYTask, TaskNoGenerator, \
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

erp_schedul = Blueprint('erp_schedul', __name__)

class SchedulingStatus(Enum):
    Locl = "1" #排产表批次已经生产则为锁定状态
    Unlock = "0" #批次还未生产


@erp_schedul.route('/systemManager_model/plantCalendarSchedulingSelect', methods=['GET', 'POST'])
def plantCalendarSchedulingSelect():
    '''
    工厂日历
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            re = []
            oclass = db_session.query(Scheduling).all()
            for oc in oclass:
                dir = {}
                dir['ID'] = oc.ID
                dir['start'] = oc.SchedulingTime
                dir['title'] = oc.PRName + ": 第" + oc.SchedulingNum[6:] + "批"
                dir['color'] = "#9FDABF"
                re.append(dir)
            ocl = db_session.query(plantCalendarScheduling).all()
            for o in ocl:
                dic = {}
                dic['ID'] = str(o.ID)
                dic['start'] = str(o.start)
                dic['title'] = o.title.split(":")[0]
                dic['color'] = o.color
                re.append(dic)
            return json.dumps(re, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            logger.error(e)
            insertSyslog("error", "工厂日历查询报错Error：" + str(e), current_user.Name)
            return json.dumps("工厂日历查询报错", cls=AlchemyEncoder, ensure_ascii=False)

@erp_schedul.route('/systemManager_model/planScheduling', methods=['GET', 'POST'])
def planScheduling():
    '''
    计划排产
    :return:
    '''
    if request.method == 'POST':
        data = request.values
        try:
            plan_id = data['plan_id']
            oc = db_session.query(product_plan).filter(product_plan.plan_id == plan_id).first()
            month = data['month']
            mou = month.split("-")
            monthRange = calendar.monthrange(int(mou[0]), int(mou[1]))
            PRName = db_session.query(ERPproductcode_prname.PRName).filter(ERPproductcode_prname.product_code == oc.product_code).first()[0]
            sch = db_session.query(SchedulingStandard).filter(SchedulingStandard.PRName == PRName).first()
            batchnums = int(oc.plan_quantity)
            days = batchnums/int(sch.DayBatchNumS) #这批计划要做多少天
            re = timeChange(mou[0], mou[1], monthRange[1])

            #不能排产的时间
            if int(mou[1])<10:
                mou = mou[0]+"-0"+mou[1]
            else:
                mou = mou[0] + "-" + mou[1]
            schdays = db_session.query(plantCalendarScheduling.start).filter(plantCalendarScheduling.start.like("%" + mou + "%"),
                                    ~plantCalendarScheduling.title.like("%安全库存%")).all()#----查询休息的天数排产去除员工不上班的时间
            undays = []
            if schdays != None:
                for i in schdays:
                    undays.append(i[0])

            # 删除上一次排产同品名同月份的数据
            solds = db_session.query(Scheduling).filter(Scheduling.PRName == PRName, Scheduling.SchedulingTime.like("%"+mou+"%")).all()
            for old in solds:
                sql = "DELETE FROM Scheduling WHERE ID = "+str(old.ID)
                db_session.execute(sql)#删除同意品名下的旧的排产计划
            plans = db_session.query(plantCalendarScheduling).filter(plantCalendarScheduling.title.like(PRName), plantCalendarScheduling.start.like("%"+mou+"%")).all()
            for pl in plans:
                sql = sql1 = "DELETE FROM plantCalendarScheduling WHERE ID = " + str(pl.ID)
                db_session.execute(sql)#删除同意品名下的安全库存信息
            db_session.commit()

            # 去掉不能排产的时间，只剩可以排产的时间
            daySchedulings = list(set(re).difference(set(undays)))
            daySchedulings = list(daySchedulings)
            daySchedulings.sort()

            # 排产数据写入数据库
            dayBatchNum = db_session.query(SchedulingStandard.DayBatchNumS).filter(SchedulingStandard.PRName == PRName).first()[0]
            j = 1
            k = 1
            for day in daySchedulings:
                if k > days:#当这个计划所有的批次做完跳出循环
                    break
                for r in range(0, int(dayBatchNum)):
                    s = Scheduling()
                    s.SchedulingTime = day
                    s.PRName = PRName
                    s.BatchNumS = sch.DayBatchNumS
                    if j < 10:
                        s.SchedulingNum = day.replace("-", "")[2:6] + "600" + str(j)
                    else:
                        s.SchedulingNum = day.replace("-", "")[2:6] + "60" + str(j)
                    db_session.add(s)
                    j = j+1
                k = k + 1
            db_session.commit()
            return 'OK'
        except Exception as e:
            print(e)
            db_session.rollback()
            logger.error(e)
            insertSyslog("error", "计划排产报错Error：" + str(e), current_user.Name)
            return json.dumps("计划排产报错", cls=AlchemyEncoder, ensure_ascii=False)
def timeChange(year,month,days):
    i = 0
    da = []
    while i < days:
        if i < 9:
            i = i + 1
            date = str(year) + "-" + str(mon(month)) + "-" + str(0) + str(i)
            da.append(date)
        else:
            i = i + 1
            date = str(year)  + "-" + str(mon(month))  + "-" +  str(i)
            da.append(date)
    return da
def mon(month):
    if int(month)<10:
        return "0"+month
    else:
        return month
@erp_schedul.route('/systemManager_model/plantSchedulingAddBatch', methods=['GET', 'POST'])
def plantSchedulingAddBatch():
    '''
    计划排产增加批次
    :return:
    '''
    if request.method == 'POST':
        data = request.values
        try:
            PRName = data['title']
            code = db_session.query(ERPproductcode_prname.product_code).filter(ERPproductcode_prname.PRName ==
                                                                               PRName).first()[0]
            plan_id = db_session.query(product_plan.plan_id).filter(product_plan.product_code == code).order_by(
                desc("plan_id")).first()
            if plan_id != None:
                plan_id = plan_id[0]
            else:
                return "请先同步ERP计划！"
            date = data['start']
            #添加排产数据
            sch = db_session.query(Scheduling).filter(Scheduling.PRName == PRName).order_by(desc("SchedulingNum")).first()
            if sch == None:
                return "请先进行排产！"
            count = db_session.query(Scheduling).filter(Scheduling.SchedulingTime == sch.SchedulingTime).count()
            SchedulingTime = sch.SchedulingTime
            if int(sch.BatchNumS) == count or sch.BatchNumS == "1":
                spls = str(sch.SchedulingTime)[8:10]
                spls = str(int(spls) + 1)
                SchedulingTime = str(sch.SchedulingTime)[0:8] + spls
                ishas = db_session.query(plantCalendarScheduling).filter(plantCalendarScheduling.start == SchedulingTime).first()
                while ishas != None:
                    i = 1
                    spls = str(int(spls) + i)
                    SchedulingTime = str(sch.SchedulingTime)[0:8] + spls
                    ishas = db_session.query(plantCalendarScheduling).filter(plantCalendarScheduling.start == SchedulingTime).first()
                    i = i + 1
            sc = Scheduling()
            sc.PRName = sch.PRName
            sc.SchedulingStatus = SchedulingStatus.Unlock.value
            sc.SchedulingTime = SchedulingTime
            sc.BatchNumS = sch.BatchNumS
            sc.SchedulingNum = str(int(sch.SchedulingNum) + 1)
            sc.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db_session.add(sc)
            db_session.commit()
            return 'OK'
        except Exception as e:
            logger.error(e)
            insertSyslog("error", "计划排产增加批次报错Error：" + str(e), current_user.Name)
            return json.dumps("计划排产增加批次报错", cls=AlchemyEncoder, ensure_ascii=False)

@erp_schedul.route('/addscheduledates', methods=['GET', 'POST'])
def addscheduledates():
    '''
    添加工作日休息日
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            month = data['month']
            count = db_session.query(scheduledate).filter(scheduledate.WorkDate.like("%"+month+"%")).count()
            if count < 20:
                mou = month.split("-")
                monthRange = calendar.monthrange(int(mou[0]), int(mou[1]))
                re = timeChange(mou[0], str(int(mou[1])), monthRange[1])
                lis = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日', ]
                dic = dict(enumerate(lis))
                for i in re:
                    ymr = i.split("-")
                    w = datetime.date(int(ymr[0]), int(ymr[1]), int(ymr[2]))
                    xq = dic[w.weekday()]
                    if xq == "星期六" or xq == "星期日":
                        # dc = db_session.query(scheduleDateType).filter(scheduleDateType.DateTypeName == "周末").first()
                        DateType = "周末"
                        color = "#FA7D00"
                    else:
                        DateType = "工作日"
                        color = "#00CAFA"
                    sc = scheduledate()
                    sc.WorkDate = i
                    sc.DateType = DateType
                    sc.comment = xq
                    sc.color = color
                    db_session.add(sc)
                    db_session.commit()
                db_session.close_all()
            return 'OK'
        except Exception as e:
            db_session.rollback()
            logger.error(e)
            insertSyslog("error", "添加工作日休息日报错Error：" + str(e), current_user.Name)
            return json.dumps("添加工作日休息日报错", cls=AlchemyEncoder, ensure_ascii=False)

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

@erp_schedul.route('/createZYPlanZYtask', methods=['POST', 'GET'])
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

