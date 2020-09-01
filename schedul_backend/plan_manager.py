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
            proclass = db_session.query(ProcessUnit).filter(ProcessUnit.BrandCode == ocalss.BrandCode).order_by("Seq").all()
            for i in proclass:
                zyplan = ZYPlan()
                zyplan.PlanDate = ocalss.PlanBeginTime
                zyplan.PlanNo = ocalss.SchedulePlanCode
                zyplan.BatchID = ocalss.BatchID
                zyplan.PlanSeq = i.Seq
                zyplan.PUCode = i.PUCode
                zyplan.PlanType = system_backend.Global.PLANTYPE.SCHEDULE.value
                zyplan.BrandCode = ocalss.BrandCode
                zyplan.BrandName = ocalss.BrandName
                zyplan.ERPOrderNo = ""
                zyplan.PlanQuantity = ocalss.PlanQuantity
                zyplan.Unit = ocalss.Unit
                zyplan.EnterTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                zyplan.PlanBeginTime = ocalss.PlanBeginTime
                zyplan.ZYPlanStatus = system_backend.Global.ZYPlanStatus.NEW.value
                zyplan.LockStatus = system_backend.Global.TASKLOCKSTATUS.UNLOCK.value
                zyplan.INFStatus = system_backend.Global.TASKSTATUS.NEW.value
                zyplan.WMSStatus = system_backend.Global.TASKSTATUS.NEW.value
                db_session.add(zyplan)
                iTaskSeq = 0
                for j in range(0, i.RelateTaskCount):
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
                    zytask.EnterTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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


from spyne import Application
from spyne import rpc
from spyne import ServiceBase
from spyne import Iterable, Integer, Unicode, Array, util, AnyDict, ModelBase
from spyne.protocol.soap import Soap11
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import logging

class WMS_Interface(ServiceBase):
    '''
    接口服务端
    '''
    logging.basicConfig(level=logging.DEBUG)
    @rpc(Unicode, Unicode, _returns=Unicode())
    def WMS_Order_Download(self, name, times):
        '''
        采购订单同步给WMS
        '''
        dic = []
        for i in range(0, 3):
            dic.append(appendStr(i))
        return json.dumps(dic)

    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(self, name, times):
        for i in range(times):
            yield u'Hello, %s' % name

    @rpc(Unicode, Unicode, _returns=Unicode())
    def WMS_OrderStatus(self, name, json_data):
        '''
        单据状态变更
        '''
        try:
            dic = []
            jso = json.loads(json_data)
            for i in jso:
                BillNo = i.get("BillNo")
                status = i.get("status")
                BrandID = i.get("BrandID")
                if BillNo != None:
                    # BatchID = BillNo[0:-1]
                    # BrandID = BillNo[-1:]
                    zy = db_session.query(ZYPlanWMS).filter(ZYPlanWMS.BatchID == BillNo ,ZYPlanWMS.BrandID == BrandID).first()
                    if zy:
                        zy.ExcuteStatus = status
                        db_session.commit()
                    else:
                        return json.dumps("没有此单据号！")
                else:
                    continue
            return json.dumps("SUCCESS")
        except Exception as e:
            print("WMS调用WMS_OrderStatus接口报错！")
            return json.dumps(e)

    @rpc(Unicode, Unicode, _returns=Unicode())
    def Sync_StapleProducts(self, name, json_data):
        '''
        WMS同步原料检验单
        '''
        try:
            dic = []
            jso = json.loads(json_data)
            for i in jso:
                sta = StapleProducts()
                sta.BillNo = i.get("BillNo")
                sta.BatchNo = i.get("BatchNo")
                sta.StoreDef_ID = i.get("StoreDef_ID")
                sta.btype = i.get("btype")
                sta.mid = i.get("mid")
                sta.Num = i.get("Num")
                sta.FinishNum = i.get("FinishNum")
                sta.IsRelevance = "0"
                sta.OperationDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                db_session.add(sta)
                db_session.commit()
            return json.dumps("SUCCESS")
        except Exception as e:
            print("WMS调用WMS_OrderStatus接口报错！")
            return json.dumps(e)

    @rpc(Unicode, Unicode, _returns=Unicode())
    def WMS_ZYPlanStatus(self, name, json_data):
        '''
        备料段计划开始结束状态WMS回传
        '''
        try:
            dic = []
            jso = json.loads(json_data)
            for i in jso:
                BatchID = i.get("BatchID")
                BrandName = i.get("BrandName")
                status = i.get("status")
                if BatchID != None:
                    zy = db_session.query(ZYPlan).filter(ZYPlan.BatchID == BatchID,
                                                         ZYPlan.BrandName == BrandName,ZYPlan.PUID == 1).first()
                    if zy != None:
                        if status == "1":
                            zy.ActBeginTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        elif status == "3":
                            zy.ActEndTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    db_session.commit()
                else:
                    continue
            return json.dumps("SUCCESS")
        except Exception as e:
            print("WMS调用WMS_ZYPlanStatus接口报错！")
            return json.dumps(e)

    @rpc(Unicode, Unicode, _returns=Unicode())
    def WMS_TrayNumber(self, name, json_data):
        '''
        WMS托盘信息回传
        '''
        try:
            dic = []
            jso = json.loads(json_data)
            for i in jso:
                BatchNo = i.get("BatchNo")
                TrayNum = i.get("TrayNum")
                MID = i.get("MID")
                PalletID = i.get("PalletID")
                FormulaID = i.get("FormulaID")
                MWeight = i.get("MWeight")
                zy = db_session.query(WMSTrayNumber).filter(WMSTrayNumber.BatchNo == BatchNo,
                                                            WMSTrayNumber.TrayNum == TrayNum,
                                                            WMSTrayNumber.MID == MID).first()
                if zy == None:
                    tn = WMSTrayNumber()
                    tn.BatchNo = BatchNo
                    tn.TrayNum = TrayNum
                    tn.MID = MID
                    tn.PalletID = PalletID
                    tn.FormulaID = FormulaID
                    tn.MWeight = MWeight
                    tn.UpdateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    db_session.commit()
                else:
                    continue
            return json.dumps("SUCCESS")
        except Exception as e:
            print("WMS调用WMS_TrayNumber接口报错！")
            return json.dumps(e)


import urllib2
import json


def http_post(url, data_json):
    jdata = json.dumps(data_json)
    req = urllib2.Request(url, jdata)
    response = urllib2.urlopen(req)
    return response.read()


url = 'http://192.168.0.107:8000/medi_test'
data_json = {'name': 'cuiyongyuan', 'job': 'hero'}
resp = http_post(url, data_json)
print(resp)


@batch_plan.route('/WMS_SendPlan', methods=['GET', 'POST'])
def WMS_SendPlan():
    '''发送投料计划到WMS'''
    if request.method == 'POST':
        data = request.values
        try:
            jsonstr = json.dumps(data.to_dict())
            if len(jsonstr) > 10:
                jsonnumber = re.findall(r"\d+\.?\d*", jsonstr)
                for key in jsonnumber:
                    id = int(key)
                    try:
                        dic = []
                        oclass = db_session.query(ZYPlanWMS).filter(ZYPlanWMS.ID == id).first()
                        # IsSend = str(int(oclass.IsSend)+1)
                        if oclass.IsSend == "10":
                            return json.dumps("数据已发送过WMS！")
                        oclss = db_session.query(MaterialBOM).filter(MaterialBOM.ProductRuleID == oclass.BrandID).all()
                        for ocl in oclss:
                            # StoreDef_ID = "1"
                            # if ocl.MATID in ("100005", "100009", "2120"):
                            #     StoreDef_ID = "2"
                            num = str(float(ocl.BatchTotalWeight)*float(ocl.BatchPercentage))
                            dic.append({"BillNo":str(oclass.BatchID)+str(oclass.BrandID),"BatchNo":str(oclass.BatchID),"btype":"203","StoreDef_ID":"1","mid":ocl.MATID,"num":num})
                        jsondic = json.dumps(dic, cls=AlchemyEncoder, ensure_ascii=False)
                        client = Client(system_backend.Global.WMSurl)
                        ret = client.service.Mes_Interface("billload", jsondic)
                        if ret[0] != "SUCCESS":
                            return json.dumps("调用WMS_SendPlan接口报错！"+ret[1])
                        oclass.IsSend = "10"
                        db_session.commit()
                        return json.dumps({"code": "200", "message": "OK"})
                    except Exception as ee:
                        return json.dumps("调用WMS_SendPlan接口报错！")
        except Exception as e:
            print("调用WMS_SendPlan接口报错！")
            return json.dumps("调用WMS_SendPlan接口报错！")
@batch_plan.route('/WMS_SendSAPMatil', methods=['GET', 'POST'])
def WMS_SendSAPMatil():
    '''发送SAP物料信息到WMS'''
    if request.method == 'GET':
        data = request.values
        try:
            jsonstr = json.dumps(data.to_dict())
            jsonnumber = re.findall(r"\d+\.?\d*", jsonstr)
            dic = []
            for key in jsonnumber:
                id = int(key)
                oclass = db_session.query(MaterialBOM).filter(MaterialBOM.ID == id).first()
                dic.append(oclass)
            jsondic = json.dumps(dic, cls=AlchemyEncoder, ensure_ascii=False)
            client = Client(system_backend.Global.WMSurl)
            ret = client.service.Mes_Interface("MatDetLoad", jsondic)
            if ret["Mes_InterfaceResult"] == "SUCCESS":
                return json.dumps({"code": "200", "message": "OK"})
            else:
                return json.dumps(ret["ErrData"])
        except Exception as e:
            print("调用WMS_SendPlan接口报错！")
            return json.dumps("调用WMS_SendPlan接口报错！")
@batch_plan.route('/WMS_ReceiveDetail', methods=['GET', 'POST'])
def WMS_ReceiveDetail():
    '''获取备料计划WMS的流水'''
    if request.method == 'GET':
        data = request.values
        try:
            dic = []
            ID = data.get("ID")
            zyw = db_session.query(ZYPlanWMS).filter(ZYPlanWMS.ID == ID).first()
            dic.append({"BillNo":zyw.BatchID+zyw.BrandID+zyw.IsSend})
            jsondic = json.dumps(dic, cls=AlchemyEncoder, ensure_ascii=False)
            client = Client(system_backend.Global.WMSurl)
            re = client.service.Mes_Interface("WorkFlowLoad", jsondic)
            if re[0] == 'SUCCESS':
                jsondata = json.loads(re["json_data"])
                return '{"total"' + ":" + str(len(jsondata)) + ',"rows"' + ":\n" + json.dumps(jsondata,
                                                                                              cls=AlchemyEncoder,
                                                                                              ensure_ascii=False) + "}"
            else:
                return json.dumps(re[1])
        except Exception as e:
            print("调用WMS_SendPlan接口报错！")
            return json.dumps("调用WMS_SendPlan接口报错！")

@batch_plan.route('/WMS_StockInfo', methods=['GET', 'POST'])
def WMS_StockInfo():
    '''获取WMS库存信息'''
    if request.method == 'GET':
        data = request.values
        try:
            ic = []
            pages = int(data.get("offset"))  # 页数
            rowsnumber = int(data.get("limit"))  # 行数
            inipage = pages * rowsnumber + 0  # 起始页
            endpage = pages * rowsnumber + rowsnumber  # 截止页
            client = Client(system_backend.Global.WMSurl)
            re = client.service.Mes_Interface("StoreLoad")
            if re[0] == "SUCCESS":
                jsondata = json.loads(re[2])
                for i in jsondata:
                    product_code = i.get("MID")
                    num = i.get("num")
                    oclass = db_session.query(SchedulingStock).filter(
                        SchedulingStock.product_code == product_code).first()
                    if oclass != None:
                        oclass.StockHouse = num
                        db_session.commit()
            else:
                return json.dumps(re[1])
            count = db_session.query(SchedulingStock).count()
            oclass = db_session.query(SchedulingStock).all()[inipage:endpage]
            jsonoclass = json.dumps(oclass, cls=AlchemyEncoder, ensure_ascii=False)
            return '{"total"' + ":" + str(count) + ',"rows"' + ":\n" + jsonoclass + "}"
        except Exception as e:
            print("调用WMS_StockInfo接口报错！")
            return json.dumps("调用WMS_StockInfo接口报错！")

@batch_plan.route('/MStatusLoad', methods=['GET', 'POST'])
def MStatusLoad():
    '''检验单状态同步给WMS'''
    if request.method == 'GET':
        data = request.values
        try:
            jsonstr = json.dumps(data.to_dict())
            if len(jsonstr) > 10:
                jsonnumber = re.findall(r"\d+\.?\d*", jsonstr)
                for key in jsonnumber:
                    id = int(key)
                    try:
                        dic = []
                        oclass = db_session.query(WMStatusLoad).filter(WMStatusLoad.ID == id).first()
                        client = Client(system_backend.Global.WMSurl)
                        ret = client.service.Mes_Interface("MStatusLoad",json.dumps(dic))
                        if ret[0] == "SUCCESS":
                            return json.dumps({"code": "200", "message": "OK"})
                        else:
                            return json.dumps(ret[1])
                    except Exception as ee:
                        return json.dumps("调用MStatusLoad接口报错！")
        except Exception as e:
            print("调用MStatusLoad接口报错！")
            return json.dumps("调用MStatusLoad接口报错！")
