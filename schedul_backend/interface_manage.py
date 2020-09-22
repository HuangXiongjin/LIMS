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
from common.batch_plan_model import ZYPlan, ZYPlanWMS, StapleProducts, WMSTrayNumber, MaterialBOM, SchedulingStock, WMStatusLoad
from database.connect_db import CONNECT_DATABASE

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
    # @rpc(Unicode, Unicode, _returns=Unicode())
    # def WMS_Order_Download(self, name, times):
    #     '''
    #     采购订单同步给WMS
    #     '''
    #     dic = []
    #     for i in range(0, 3):
    #         dic.append(appendStr(i))
    #     return json.dumps(dic)

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
                PUCode = i.get("PUCode")
                if BatchID != None:
                    zy = db_session.query(ZYPlan).filter(ZYPlan.BatchID == BatchID,
                                                         ZYPlan.BrandName == BrandName,ZYPlan.PUCode == PUCode).first()
                    if zy != None:
                        if status == "1":
                            zy.ZYPlanStatus = common.Global.ZYPlanStatus.READY.value
                            zy.ActBeginTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        elif status == "3":
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


import json


# def http_post(url, data_json):
#     jdata = json.dumps(data_json)
#     req = urllib3.Request(url, jdata)
#     response = urllib3.urlopen(req)
#     return response.read()
#
#
# url = 'http://192.168.0.107:8000/medi_test'
# data_json = {'name': 'cuiyongyuan', 'job': 'hero'}
# resp = http_post(url, data_json)
# print(resp)


@interface_manage.route('/WMS_SendPlan', methods=['GET', 'POST'])
def WMS_SendPlan():
    '''发送备料计划到WMS'''
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
                        client = Client(common.Global.WMSurl)
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
@interface_manage.route('/WMS_SendSAPMatil', methods=['GET', 'POST'])
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
            client = Client(common.Global.WMSurl)
            ret = client.service.Mes_Interface("MatDetLoad", jsondic)
            if ret["Mes_InterfaceResult"] == "SUCCESS":
                return json.dumps({"code": "200", "message": "OK"})
            else:
                return json.dumps(ret["ErrData"])
        except Exception as e:
            print("调用WMS_SendPlan接口报错！")
            return json.dumps("调用WMS_SendPlan接口报错！")
@interface_manage.route('/WMS_ReceiveDetail', methods=['GET', 'POST'])
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
            client = Client(common.Global.WMSurl)
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

@interface_manage.route('/WMS_StockInfo', methods=['GET', 'POST'])
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
            client = Client(common.Global.WMSurl)
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

@interface_manage.route('/MStatusLoad', methods=['GET', 'POST'])
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
                        client = Client(common.Global.WMSurl)
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
