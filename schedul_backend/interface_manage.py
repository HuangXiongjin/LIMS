from flask import Blueprint
from sqlalchemy.orm import sessionmaker
from flask import request
import datetime
from flask_login import LoginManager
import re
from sqlalchemy import create_engine
from common.BSFramwork import AlchemyEncoder
from suds.client import Client
import common.Global
from common.batch_plan_model import ZYPlan, ZYPlanWMS, StapleProducts, WMSTrayNumber, MaterialBOM, SchedulingStock, \
    WMStatusLoad, Material, PlanManager, ProcessUnit, BatchMaterialInfo, ProductRule, ZYTask
from database.connect_db import CONNECT_DATABASE
from common import Global
import json

login_manager = LoginManager()
# 创建对象的基类
engine = create_engine(CONNECT_DATABASE)
Session = sessionmaker(bind=engine)
db_session = Session()

interface_manage = Blueprint('interface_manage', __name__)
from spyne import rpc
from spyne import ServiceBase
from spyne import Iterable, Integer, Unicode
import logging

class WMS_Interface(ServiceBase):
    '''
    接口服务端
    '''
    logging.basicConfig(level=logging.DEBUG)

    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(self, name, times):
        for i in range(times):
            yield u'Hello, %s' % name

    @rpc(Unicode, Unicode, _returns=Unicode())
    def WMS_OrderStatus(self, name, json_data):
        '''
       投料明细状态便跟接口
        '''
        try:
            dic = []
            jso = json.loads(json_data)
            for i in jso:
                BatchMaterialInfoID = i.get("BatchMaterialInfoID")
                EQPCode = i.get("EQPCode")
                EQPName = i.get("EQPName")
                status = i.get("status")
                if BatchMaterialInfoID != None:
                    zy = db_session.query(BatchMaterialInfo).filter(BatchMaterialInfo.ID == BatchMaterialInfoID).first()
                    if zy:#批次明细增加完成时间
                        if status == "End":
                            status = "投料系统已投料"
                        zy.ExcuteStatus = status
                        zy.FinishDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        db_session.commit()
                    else:
                        return json.dumps("没有此物料明细ID！")
                else:
                    continue
            return json.dumps("SUCCESS")
        except Exception as e:
            print("WMS调用WMS_OrderStatus接口报错！")
            return json.dumps(e)

    @rpc(Unicode, Unicode, _returns=Unicode())
    def WMS_ZYPlanStatus(self, name, json_data):
        '''
        投料段计划开始结束状态回传接口
        '''
        try:
            dic = []
            jso = json.loads(json_data)
            for i in jso:
                PlanNo = i.get("PlanNo")
                BatchID = i.get("BatchID")
                BrandCode = i.get("BrandCode")
                status = i.get("status")
                if PlanNo != None:
                    # oclas = db_session.query(PlanManager).filter(PlanManager.ID == PlanNo).first()
                    zy = db_session.query(ZYPlan).filter(ZYPlan.BatchID == BatchID,
                                                         ZYPlan.BrandCode == BrandCode,ZYPlan.PUName == "投料").first()
                    if zy != None:
                        if status == "Start":
                            zy.ZYPlanStatus = common.Global.ZYPlanStatus.READY.value
                            zy.ActBeginTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        elif status == "End":
                            zy.ZYPlanStatus = common.Global.ZYPlanStatus.Clear.value
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


import requests
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    'Referer': 'https://httpbin.org/post',
    'Connection': 'keep-alive',
    'content-type': 'application/json'
    }
@interface_manage.route('/WMS_SendPlan', methods=['GET', 'POST'])
def WMS_SendPlan():
    '''发送投料任务到WMS'''
    if request.method == 'POST':
        data = request.values
        try:
            jsonstr = json.dumps(data.to_dict())
            if len(jsonstr) > 10:
                jsonnumber = re.findall(r"\d+\.?\d*", jsonstr)
                dic = []
                for key in jsonnumber:
                    id = int(key)
                    plan = db_session.query(PlanManager).filter(PlanManager.ID == id).first()
                    oclass = db_session.query(ZYTask).filter(ZYTask.BatchID == plan.BatchID,
                                                             ZYTask.BrandCode == plan.BrandCode,
                                                             ZYTask.PUName.like("%提取%")).all()
                    for oc in oclass:
                        dic.append({"PlanNo": plan.ID, "BrandCode": oc.BrandCode,
                                    "BrandName": oc.BrandName, "BatchID": oc.BatchID,
                                    "Weight": oc.PlanQuantity, "Unit": oc.Unit, "EQPCode": oc.EQPCode, "EQPName":oc.EQPName})
                    plan.PlanStatus = Global.PlanStatus.FSWMS.value
                    db_session.commit()
                url = Global.WMSurl + "api/WbeApi/RecvTransInfon"
                dir = {}
                dir["zyplan_list"] = dic
                dir = json.dumps(dir)
                resp = requests.post(url, json=dir, headers=headers)
                responjson = json.loads(resp.content)
                responjson = eval(responjson)
                if responjson.get("code") != "0":
                    db_session.rollback()
                    return json.dumps({"code": "500", "message": "调用WMS_SendPlan接口报错！" + responjson.get("msg")})
                return json.dumps({"code": "200", "message": "OK"})
        except Exception as e:
            db_session.rollback()
            print("调用WMS_SendPlan接口报错！")
            return json.dumps("调用WMS_SendPlan接口报错！")
@interface_manage.route('/WMS_SendMatils', methods=['GET', 'POST'])
def WMS_SendMatils():
    '''备料明细发送投料系统接口'''
    if request.method == 'POST':
        data = request.values
        try:
            jsonstr = json.dumps(data.to_dict())
            if len(jsonstr) > 10:
                jsonnumber = re.findall(r"\d+\.?\d*", data.get("sendData"))
                PlanID = data.get("PlanID")
                pmoc = db_session.query(PlanManager).filter(PlanManager.ID == PlanID).first()
                dic = []
                for key in jsonnumber:
                    id = int(key)
                    oclass = db_session.query(BatchMaterialInfo).filter(BatchMaterialInfo.ID == id).first()
                    # zypla = db_session.query(ZYPlan).filter(ZYPlan.BatchID == oclass.BatchID, ZYPlan.BrandCode == oclass.BrandCode, ZYPlan.PUName.like("%提取%")).first()
                    dic.append({"BatchMaterialInfoID": oclass.ID, "BrandCode": pmoc.BrandCode, "BrandName": pmoc.BrandName,
                                "BatchID": oclass.BatchID, "FlagCode": oclass.BucketNum,
                                "Weight": oclass.BucketWeight, "Unit": oclass.Unit, "Flag": oclass.Flag, "FeedingSeq": oclass.FeedingSeq,
                                "EQPCode": oclass.EQPCode, "EQPName":oclass.EQPName, "TYPE":"备料"})
                    oclass.SendFlag = "投料系统已接收"
                    oclass.OperationDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # zypla.TaskStatus = "已发送"
                    db_session.commit()
                if len(dic)>0:
                    url = Global.WMSurl + "api/WbeApi/RecvContanerInfon"
                    dir = {}
                    dir["batchmaterial_list"] = dic
                    dir = json.dumps(dir)
                    resp = requests.post(url, json=dir, headers=headers)
                    responjson = json.loads(resp.content)
                    responjson = eval(responjson)
                    if responjson.get("code") != "0":
                        db_session.rollback()
                        return json.dumps({"code": "500", "message": "调用WMS_SendPlan接口报错！" + responjson.get("msg")})
                pmoc.PlanStatus = data.get("PlanStatus")
                db_session.commit()
                return json.dumps({"code": "200", "message": "OK"})
        except Exception as e:
            db_session.rollback()
            print("调用WMS_SendPlan接口报错！")
            return json.dumps("调用WMS_SendPlan接口报错！")
@interface_manage.route('/WMS_SendTouLMatils', methods=['GET', 'POST'])
def WMS_SendTouLMatils():
    '''投料计划发送投料系统接口'''
    if request.method == 'POST':
        data = request.values
        try:
            jsonstr = json.dumps(data.to_dict())
            if len(jsonstr) > 10:
                jsonnumber = re.findall(r"\d+\.?\d*", data.get("sendData"))
                PlanID = data.get("PlanID")
                pmoc = db_session.query(PlanManager).filter(PlanManager.ID == PlanID).first()
                dic = []
                for key in jsonnumber:
                    id = int(key)
                    oclass = db_session.query(BatchMaterialInfo).filter(BatchMaterialInfo.ID == id).first()
                    # zypla = db_session.query(ZYPlan).filter(ZYPlan.BatchID == oclass.BatchID, ZYPlan.BrandCode == oclass.BrandCode, ZYPlan.PUName.like("%提取%")).first()
                    dic.append({"BatchMaterialInfoID": oclass.ID, "BrandCode": pmoc.BrandCode, "BrandName": pmoc.BrandName,
                                "BatchID": oclass.BatchID, "FlagCode": oclass.BucketNum,
                                "Weight": oclass.BucketWeight, "Unit": oclass.Unit, "Flag": oclass.Flag, "FeedingSeq": oclass.FeedingSeq,
                                "EQPCode": oclass.EQPCode, "EQPName":oclass.EQPName, "TYPE":"投料"})
                    oclass.SendFlag = "投料系统已接收"
                    oclass.OperationDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # zypla.TaskStatus = "已发送"
                    db_session.commit()
                if len(dic)>0:
                    url = Global.WMSurl + "api/WbeApi/RecvContanerInfon"
                    dir = {}
                    dir["batchmaterial_list"] = dic
                    dir = json.dumps(dir)
                    resp = requests.post(url, json=dir, headers=headers)
                    responjson = json.loads(resp.content)
                    responjson = eval(responjson)
                    if responjson.get("code") != "0":
                        db_session.rollback()
                        return json.dumps({"code": "500", "message": "调用WMS_SendPlan接口报错！" + responjson.get("msg")})
                pmoc.PlanStatus = data.get("PlanStatus")
                db_session.commit()
                return json.dumps({"code": "200", "message": "OK"})
        except Exception as e:
            db_session.rollback()
            print("调用WMS_SendPlan接口报错！")
            return json.dumps("调用WMS_SendPlan接口报错！")
@interface_manage.route('/WMS_SendReturnMaterialInfo', methods=['GET', 'POST'])
def WMS_SendReturnMaterialInfo():
    '''发送退料信息到WMS'''
    if request.method == 'POST':
        data = request.values
        try:
            jsonstr = json.dumps(data.to_dict())
            if len(jsonstr) > 10:
                jsonnumber = re.findall(r"\d+\.?\d*", jsonstr)
                dic = []
                for key in jsonnumber:
                    id = int(key)
                    oclass = db_session.query(BatchMaterialInfo).filter(BatchMaterialInfo.ID == id).first()
                    dic.append({"BatchMaterialInfoID": oclass.ID, "BrandCode": oclass.BrandCode, "BrandName": oclass.BrandName,
                                "BatchID": oclass.BatchID, "FlagCode": oclass.BucketNum,
                                "Weight": oclass.BucketWeight, "Unit": oclass.Unit, "Flag": oclass.Flag})
                    oclass.SendFlag = "投料系统已接收退料"
                    oclass.OperationDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                url = Global.WMSurl + "api/WbeApi/RecvTransInfon"
                dir = {}
                dir["zyplan_list"] = dic
                dir = json.dumps(dir)
                resp = requests.post(url, json=dir, headers=headers)
                responjson = json.loads(resp.content)
                responjson = eval(responjson)
                if responjson.get("code") != "0":
                    db_session.rollback()
                    return json.dumps({"code": "500", "message": "调用WMS_SendReturnMaterialInfo接口报错！" + responjson.get("msg")})
                return json.dumps({"code": "200", "message": "OK"})
        except Exception as e:
            db_session.rollback()
            print("调用WMS_SendPlan接口报错！")
            return json.dumps("调用WMS_SendPlan接口报错！")

