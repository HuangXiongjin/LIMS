from flask import Blueprint
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from flask import request
import json
import datetime
from flask_login import current_user,LoginManager
import re
from sqlalchemy import create_engine
from common.BSFramwork import AlchemyEncoder
from common.common_cuid import logger,insertSyslog
import os
from datetime import timedelta
from common import Global
from common.batch_plan_model import ProductUnit, PlanManager, ZYPlan, ZYTask, TaskNoGenerator, \
    ProcessUnit, SchedulePlan, \
    BatchModel, BatchUseModel, BatchMaterialInfo, EletronicBatchDataStore
from common.schedul_model import EquipmentBatchRunTime
from database.connect_db import CONNECT_DATABASE

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
                Description=""))
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
                zyplan.PlanSeq = i.Seq
                zyplan.PUCode = i.PUCode
                zyplan.PUName = i.PUName
                zyplan.PlanType = Global.PLANTYPE.SCHEDULE.value
                zyplan.BrandCode = ocalss.BrandCode
                zyplan.BrandName = ocalss.BrandName
                zyplan.ERPOrderNo = ""
                zyplan.PlanQuantity = ocalss.PlanQuantity
                zyplan.Unit = ocalss.Unit
                zyplan.EnterTime = ""
                zyplan.PlanBeginTime = ""
                zyplan.ZYPlanStatus = ""
                zyplan.LockStatus = Global.TASKLOCKSTATUS.UNLOCK.value
                zyplan.INFStatus = Global.TASKSTATUS.NEW.value
                zyplan.WMSStatus = Global.TASKSTATUS.NEW.value
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
                    zytask.PUName = i.PUName
                    zytask.PlanType = Global.PLANTYPE.SCHEDULE.value
                    zytask.BrandCode = ocalss.BrandCode
                    zytask.BrandName = ocalss.BrandName
                    zytask.PlanQuantity = ocalss.PlanQuantity
                    zytask.Unit = ocalss.Unit
                    zytask.EnterTime = ""
                    # zytask.SetRepeatCount = i.RelateTaskCount
                    zytask.TaskStatus = Global.TASKSTATUS.NEW.value
                    zytask.LockStatus = Global.TASKLOCKSTATUS.UNLOCK.value
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
                PlanEndTime = data.get("PlanEndTime")
                BrandCode = data.get("BrandCode")
                PlanBeginTime = data.get("PlanBeginTime")
                #批次号判重
                pcBatchID = db_session.query(PlanManager.BatchID).filter(PlanManager.BatchID == BatchID,
                                                                       PlanManager.BrandCode == BrandCode).first()
                if pcBatchID:
                    return json.dumps({"code": "201", "message": "批次号重复！"})
                pm = PlanManager()
                pm.SchedulePlanCode = data.get("SchedulePlanCode")
                pm.BatchID = BatchID
                pm.PlanQuantity = data.get("PlanQuantity")
                pm.PlanNum = data.get("PlanNum")
                pm.Unit = data.get("Unit")
                pm.BrandCode = BrandCode
                pm.BrandName = data.get("BrandName")
                pm.PlanStatus = Global.PlanStatus.NEW.value
                pm.PlanBeginTime = data.get("PlanBeginTime")
                pm.PlanEndTime = data.get("PlanEndTime")
                pm.BrandType = data.get("BrandType")
                pm.EqpCodes = data.get("EqpCodes")
                db_session.add(pm)
                sp = SchedulePlan()
                SchedulePlanCode = PlanEndTime[0:10]
                Description = Global.SCHEDULETYPE.DAY.value
                dEndTime = datetime.datetime.strptime(PlanEndTime[0:10], '%Y-%m-%d') + timedelta(days=1)
                PlanBeginTime = PlanBeginTime
                PlanEndTime = PlanEndTime
                Type = Global.SCHEDULETYPE.DAY.value
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
                    db_session.commit()
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
            Description = data.get("Describtion")
            ID = data.get("ID")
            oclassplan = db_session.query(PlanManager).filter_by(ID=ID).first()
            oclassplan.PlanStatus = PlanStatus
            oclassplan = Description
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
                if PlanStatus == "已下发":
                    returnmsg = makeZYPlanZYTask(ID)
                    if (returnmsg == False):
                        return json.dumps({"code": "500", "message": "下发失败！"})
                    oclassplan = db_session.query(PlanManager).filter_by(ID=ID).first()
                    oclassplan.PlanStatus = Global.PlanStatus.Realse.value
                    db_session.commit()
                    return json.dumps({"code": "200", "message": "下发成功！！"})
                elif PlanStatus == "撤回":
                    oclassplan = db_session.query(PlanManager).filter_by(ID=ID).first()
                    oclassplan.PlanStatus = Global.PlanStatus.Recall.value
                    db_session.commit()
                    return json.dumps({"code": "200", "message": "撤回成功！！"})
                else:
                    return json.dumps({"code": "200", "message": "批次计划状态不正确！"})
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
            Parameter = data.get("Parameter")
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
            bm.Parameter = Parameter
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
    '''查询批记录模版'''
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
                dir["BrandCode"] = oc.FileName
                dir["BrandName"] = oc.FileName
                dir["PUIDName"] = oc.FileName
                dir["PUCode"] = oc.PUCode
                dir["UserName"] = oc.UserName
                dir["Parameter"] = oc.Parameter
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
@batch_plan.route('/batchusemodelselect', methods=['GET', 'POST'])
def batchusemodelselect():
    '''查询批记录使用模版'''
    if request.method == 'GET':
        data = request.values
        try:
            PUCode = data.get("PUCode")
            BrandCode = data.get("BrandCode")
            PUIDName = data.get("PUIDName")
            BrandName = data.get("BrandName")
            BatchID = data.get("BatchID")
            oclass = db_session.query(BatchUseModel).filter(BatchUseModel.BrandCode ==
                                                            BrandCode, BatchUseModel.PUCode == PUCode,
                                                            BatchUseModel.BatchID == BatchID).first()
            dir = {}
            if not oclass:#初始化批记录模板
                bum = BatchUseModel()
                bum.BatchID = BatchID
                bum.BrandCode = BrandCode
                bum.BrandName = BrandName
                bum.PUCode = PUCode
                bum.PUIDName = PUIDName
                oclass = db_session.query(BatchModel).filter(BatchModel.BrandCode ==
                                                                BrandCode, BatchModel.PUCode == PUCode).first()
                bum.UseParameter = oclass.Parameter
                db_session.add(bum)
                db_session.commit()
                oc = db_session.query(BatchUseModel).filter(BatchUseModel.BrandCode ==
                                                                BrandCode, BatchUseModel.PUCode == PUCode,
                                                                BatchUseModel.BatchID == BatchID).first()
                dir["ID"] = oc.ID
                dir["BrandCode"] = oc.FileName
                dir["BrandName"] = oc.FileName
                dir["PUIDName"] = oc.FileName
                dir["PUCode"] = oc.PUCode
                dir["UseParameter"] = oc.Parameter
            else:
                dir["ID"] = oclass.ID
                dir["BrandCode"] = oclass.FileName
                dir["BrandName"] = oclass.FileName
                dir["PUIDName"] = oclass.FileName
                dir["PUCode"] = oclass.PUCode
                dir["UseParameter"] = oclass.UseParameter
            return json.dumps({"code": "200", "message": dir})
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "查询批记录使用模版报错Error：" + str(e), current_user.Name)
            return json.dumps({"code": "500", "message": "后端报错"})

@batch_plan.route('/BatchMaterialInfoselect', methods=['GET', 'POST'])
def BatchMaterialInfoselect():
    '''物料明细查询'''
    if request.method == 'GET':
        data = request.values
        try:
            BrandCode = data.get("BrandCode")
            BatchID = data.get("BatchID")
            SendFlag = data.get("SendFlag")
            pages = data.get("offset")
            rowsnumber = data.get("limit")
            inipage = int(pages) * int(rowsnumber) + 0  # 起始页
            endpage = int(pages) * int(rowsnumber) + int(rowsnumber)  # 截止页
            if SendFlag == "" or SendFlag == None:
                count = db_session.query(BatchMaterialInfo).filter(BatchMaterialInfo.BrandCode ==
                                                            BrandCode, BatchMaterialInfo.BatchID == BatchID).count()
                oclass = db_session.query(BatchMaterialInfo).filter(BatchMaterialInfo.BrandCode ==
                                                            BrandCode, BatchMaterialInfo.BatchID == BatchID).all()[inipage:endpage]
            else:
                count = db_session.query(BatchMaterialInfo).filter(BatchMaterialInfo.BrandCode ==
                                                                    BrandCode, BatchMaterialInfo.SendFlag == SendFlag,
                                                                    BatchMaterialInfo.BatchID == BatchID).count()
                oclass = db_session.query(BatchMaterialInfo).filter(BatchMaterialInfo.BrandCode ==
                                                                    BrandCode, BatchMaterialInfo.SendFlag == SendFlag,
                                                                    BatchMaterialInfo.BatchID == BatchID).all()[inipage:endpage]
            dir_list = []
            for oc in oclass:
                dir = {}
                dir["ID"] = oc.ID
                dir["BatchID"] = oc.BatchID
                dir["BrandCode"] = oc.BrandCode
                dir["BrandName"] = oc.BrandName
                dir["FeedingSeq"] = oc.FeedingSeq
                dir["BucketNum"] = oc.BucketNum
                dir["BucketWeight"] = oc.BucketWeight
                dir["Flag"] = oc.Flag
                dir["Unit"] = oc.Unit
                dir["Description"] = oc.Description
                dir["SendFlag"] = oc.SendFlag
                dir_list.append(dir)
            return json.dumps({"code": "200", "message": "请求成功", "data": {"total": count, "rows": dir_list}},
                              cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "物料明细查询报错Error：" + str(e), current_user.Name)
            return json.dumps({"code": "500", "message": "后端报错"})


@batch_plan.route('/saveEQPCode', methods=['POST', 'GET'])
def saveEQPCode():
    '''生产调度添加设备'''
    if request.method == 'POST':
        data = request.values  # 返回请求中的参数和form
        try:
            jsonstr = json.dumps(data.to_dict())
            if len(jsonstr) > 10:
                ID = data.get('ID')
                oclass = db_session.query(PlanManager).filter(PlanManager.ID == ID).first()
                PUName = data.get("PUName")
                PUCode = data.get("PUCode")
                eqList = json.loads(data.get('eqList'))
                # for el in eqList:  # 为查询设备是否是已经使用过的做添加数据
                #     ert = EquipmentBatchRunTime()
                #     ert.BatchID = oclass.BatchID
                #     ert.EQPCode = el.get("EQPCode")
                #     ert.EQPName = el.get("EQPName")
                #     ert.BrandCode = oclass.BrandCode
                #     ert.BrandName = oclass.BrandName
                #     ert.PUCode = PUName
                #     ert.PUName = PUCode
                #     ert.StartTime = el.get("StartTime")
                #     ert.EndTime = el.get("EndTime")
                #     ert.WorkTime = el.get("workTime")
                #     ert.WaitTime = el.get("waitTime")
                #     db_session.add(ert)
                oclasstasks = db_session.query(ZYTask).filter(ZYTask.PUCode == PUCode,
                                                              ZYTask.BrandCode == oclass.BrandCode,
                                                              ZYTask.BatchID == oclass.BatchID).all()
                for i in range(len(oclasstasks)):
                    oclasstasks[i].EQPCode = eqList[i % len(eqList)]
                    oclasstasks[i].TaskStatus = Global.TASKSTATUS.Confirm.value
                db_session.commit()
                oclasstasks = db_session.query(ZYTask).filter(ZYTask.BatchID == oclass.BatchID,
                                                              ZYTask.PUCode == PUCode,
                                                              ZYTask.BrandCode == oclass.BrandCode).all()
                flag = "TRUE"
                for task in oclasstasks:
                    if (task.TaskStatus != Global.TASKSTATUS.Confirm.value):
                        flag = "FALSE"
                if (flag == "TRUE"):
                    zyplanc = db_session.query(ZYPlan).filter(ZYPlan.BatchID == oclass.BatchID,
                                                              ZYPlan.PUCode == PUCode,
                                                              ZYPlan.BrandCode == oclass.BrandCode).first()
                    zyplanc.ZYPlanStatus = Global.ZYPlanStatus.Confirm.value
                    db_session.commit()

                return json.dumps({"code": "200", "message": "添加设备成功！"})
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "生产调度添加设备报错Error：" + str(e), current_user.Name)
            return json.dumps({"code": "500", "message": "生产调度添加设备报错"})

# 所有工艺段保存查询操作
@batch_plan.route('/allUnitDataMutual', methods=['POST', 'GET'])
def allUnitDataMutual():
    if request.method == 'POST':
        data = request.values
        data = data.to_dict()
        try:
            for key in data.keys():
                if key == "BrandID":
                    continue
                if key == "PUCode":
                    continue
                if key == "BatchID":
                    continue
                val = data.get(key)
                addUpdateEletronicBatchDataStore(data.get("BrandID"), data.get("PUCode"), data.get("BatchID"), key, val)
            return 'OK'
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "所有工艺段保存查询操作报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder,
                              ensure_ascii=False)
    if request.method == 'GET':
        data = request.values
        try:
            json_str = json.dumps(data.to_dict())
            if len(json_str) > 2:
                PUCode = data['PUCode']
                BatchID = data['BatchID']
                BrandID = data.get("BrandID")
                oclasss = db_session.query(EletronicBatchDataStore).filter(EletronicBatchDataStore.BrandID == BrandID, EletronicBatchDataStore.PUCode == PUCode,
                                                                           EletronicBatchDataStore.BatchID == BatchID).all()
                dic = {}
                for oclass in oclasss:
                    dic[oclass.Content] = oclass.OperationpValue
            return json.dumps(dic, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "所有工艺段保存查询操作报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder,
                              ensure_ascii=False)


def addUpdateEletronicBatchDataStore(BrandID, PUCode, BatchID, ke, val):
    try:
        oc = db_session.query(EletronicBatchDataStore).filter(EletronicBatchDataStore.BrandID == BrandID,
                                                              EletronicBatchDataStore.PUCode == PUCode,
                                                              EletronicBatchDataStore.BatchID == BatchID,
                                                              EletronicBatchDataStore.Content == ke).first()
        if oc == None:
            db_session.add(EletronicBatchDataStore(BrandID=BrandID, BatchID=BatchID, PUCode=PUCode, Content=ke, OperationpValue=val,
                                                   Operator=current_user.Name))
        else:
            oc.Content = ke
            oc.OperationpValue = val
            oc.Operator = current_user.Name
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(e)
        logger.error(e)
        insertSyslog("error", "保存更新EletronicBatchDataStore报错：" + str(e), current_user.Name)
        return json.dumps("保存更新EletronicBatchDataStore报错", cls=AlchemyEncoder,
                          ensure_ascii=False)