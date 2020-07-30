from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, ForeignKey, Table, Column, DateTime, Integer, String, Unicode, Float, BigInteger
from sqlalchemy.dialects.mssql.base import BIT
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
from flask_login import LoginManager
from database.connect_db import CONNECT_DATABASE

login_manager = LoginManager()
# 创建对象的基类
engine = create_engine(CONNECT_DATABASE)
Session = sessionmaker(bind=engine)
db_session = Session()
Base = declarative_base(engine)




# 电子批记录
class ElectronicBatch(Base):
    __tablename__ = 'ElectronicBatch'
    # id:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # id:
    TaskID = Column(Integer, primary_key=False, autoincrement=True, nullable=False)

    # 批次号:
    BatchID = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 工艺段编码:
    PDUnitRouteID = Column(Integer, nullable=False, primary_key=False)

    # 设备编码
    EQPID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 类型:
    OpcTagID = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)

    # 类型:
    BrandID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 类型:
    BrandName = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)

    # 采样值:
    SampleValue = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 采样时间:
    SampleDate = Column(DateTime, primary_key=False, autoincrement=False, nullable=True)

    # 重复次数：
    RepeatCount = Column(Integer, primary_key=False, autoincrement=False, nullable=True, default=0)

    # 描述:
    Description = Column(Unicode(200), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Type = Column(Unicode(200), primary_key=False, autoincrement=False, nullable=True)

    # 单位:
    Unit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

# BatchMaintain_START:
class BatchMaintainTask(Base):
    '''
    任务表
    '''
    __tablename__ = "BatchMaintainTask"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 工艺段:
    PuidName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 计划单号:
    PlanNum = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 批次号:
    BatchID = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 品名:
    BrandName = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)

    # 计划重量:
    PlanQuantity = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 水用量:
    WaterConsumption = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 汽用量:
    SteamConsumption = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 创建日期:
    CreateDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 生产日期:
    ProductionDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 开始时间:
    StartTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 结束时间:
    EndTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

class BrandMaintain(Base):
    '''品名维护表'''
    __tablename__ = "BrandMaintain"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=True)

    # 产品名称:
    BrandName = Column(Unicode(64), nullable=False, primary_key=False)

    # 产品编码:
    BrandCode = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 创建日期:
    CreateDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


class PUIDMaintain(Base):
    '''工艺维护表'''
    __tablename__ = "PUIDMaintain"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=True)

    # 工艺名称:
    PUIDName = Column(Unicode(64), nullable=False, primary_key=False)

    # 工艺编码:
    PUIDCode = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 产品名称:
    BrandName = Column(Unicode(64), nullable=False, primary_key=False)

    # 产品编码:
    BrandCode = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 创建日期:
    CreateDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# ZYPlan:
class ZYPlan(Base):
    __tablename__ = "ZYPlan"

    # ID:
    ID = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)

    # 计划日期:
    PlanDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 制药计划单号:
    PlanNo = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 批次号:
    BatchID = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 顺序号:
    PlanSeq = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 工艺段:
    PUID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 计划类型:
    PlanType = Column(Unicode(16), primary_key=False, autoincrement=False, nullable=True)

    # 品名:
    BrandID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 品名名称:
    BrandName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # ERP订单号:
    ERPOrderNo = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 计划重量:
    PlanQuantity = Column(Float(53), primary_key=False, autoincrement=False, nullable=True)

    # 实际重量:
    ActQuantity = Column(Float(53), primary_key=False, autoincrement=False, nullable=True)

    # 单位:
    Unit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 录入时间:
    EnterTime = Column(DateTime, primary_key=False, autoincrement=False, nullable=True)

    # 计划开始时间:
    PlanBeginTime = Column(DateTime, primary_key=False, autoincrement=False, nullable=True)

    PlanEndTime = Column(DateTime, primary_key=False, autoincrement=False, nullable=True)

    # 实际开始时间:
    ActBeginTime = Column(DateTime, primary_key=False, autoincrement=False, nullable=True)

    # 实际完成时间:
    ActEndTime = Column(DateTime, primary_key=False, autoincrement=False, nullable=True)

    # 计划状态:
    ZYPlanStatus = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 计划锁定状态:
    LockStatus = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 接口处理状态:
    INFStatus = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 仓储送料状态:
    WMSStatus = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# ZYTask:
class ZYTask(Base):
    __tablename__ = "ZYTask"

    # ID:
    ID = Column(BigInteger, primary_key=True, autoincrement=True, nullable=True)

    # 设备ID:
    EquipmentID = Column(Unicode(30), primary_key=False, autoincrement=True, nullable=True)

    # 计划日期:
    PlanDate = Column(Unicode(50), primary_key=False, autoincrement=False, nullable=True)

    # 制药任务单号:
    TaskID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 批次号:
    BatchID = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 顺序号:
    PlanSeq = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 工艺段:
    PUID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 工艺路线名称:
    PDUnitRouteName = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 计划类型:
    PlanType = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 牌号编码:
    BrandID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 牌号名称:
    BrandName = Column(Unicode(50), primary_key=False, autoincrement=False, nullable=True)

    # 计划重量:
    PlanQuantity = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 实际重量:
    ActQuantity = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 单位:
    Unit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 录入时间:
    EnterTime = Column(DateTime, primary_key=False, autoincrement=False, nullable=True)

    # 实际开始时间:
    ActBeginTime = Column(DateTime, primary_key=False, autoincrement=False, nullable=True)

    # 实际完成时间:
    ActEndTime = Column(DateTime, primary_key=False, autoincrement=False, nullable=True)

    # 设定重复次数:
    SetRepeatCount = Column(Integer, primary_key=False, autoincrement=False, nullable=True, default=1)

    # 当前重复次数:
    CurretnRepeatCount = Column(Integer, primary_key=False, autoincrement=False, nullable=True, default=0)

    # 实际罐号:
    ActTank = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 任务状态:
    TaskStatus = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 任务锁定状态:
    LockStatus = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# ProductLine:
class ProductLine(Base):
    __tablename__ = "ProductLine"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=True)

    # 生产线编码:
    PLineCode = Column(Unicode(50), primary_key=False, autoincrement=False, nullable=True)

    # 生产线名称:
    PLineName = Column(Unicode(50), primary_key=False, autoincrement=False, nullable=True)

    # 车间ID:
    AreaID = Column(Integer, ForeignKey("Area.ID"), nullable=False, primary_key=False)

    # 描述:
    Desc = Column(Unicode(50), primary_key=False, autoincrement=False, nullable=True)

    # 产线能力:
    PLineCapacity = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 单位:
    Unit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 计划类型:
    Seq = Column(Integer, primary_key=False, autoincrement=False, nullable=True)


# ProcessUnit:
class ProcessUnit(Base):
    __tablename__ = "ProcessUnit"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=True)

    # 工艺段编码:
    PUCode = Column(Unicode(50), primary_key=False, autoincrement=False, nullable=True)

    # 工艺段名称:
    PUName = Column(Unicode(50), primary_key=False, autoincrement=False, nullable=True)

    # 生产线ID:
    PLineID = Column(Integer, ForeignKey("ProductLine.ID"), nullable=False, primary_key=False)

    # 描述:
    Desc = Column(Unicode(50), primary_key=False, autoincrement=False, nullable=True)

    # 工艺段额定生产能力:
    PURateCapacity = Column(Unicode(30), primary_key=False, autoincrement=False, nullable=True)

    # 工艺段计划生产能力:
    PUPLanCapacity = Column(Unicode(30), primary_key=False, autoincrement=False, nullable=True)

    # 工艺段顺序号:
    Seq = Column(Unicode(30), primary_key=False, autoincrement=False, nullable=True)

    # 能力单位:
    CapacityUnit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 静置时间:
    PlaceTime = Column(Unicode(30), primary_key=False, autoincrement=False, nullable=True)

    # 时间单位:
    TimeUnit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 批次运行时间:
    BatchRunTime = Column(Unicode(30), primary_key=False, autoincrement=False, nullable=True)


# ProductRule:
class ProductRule(Base):
    __tablename__ = "ProductRule"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=True)

    # 产品定义编码:
    PRCode = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 产品定义名称:
    PRName = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 版本:
    Version = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Desc = Column(Unicode(200), primary_key=False, autoincrement=False, nullable=True)

    # 发布日期:
    Publish_date = Column(DateTime, primary_key=False, autoincrement=False, nullable=True)

    # 使用日期:
    Appy_date = Column(DateTime, primary_key=False, autoincrement=False, nullable=True)

    # 是否使用:
    IsUsed = Column(BIT, primary_key=False, autoincrement=False, nullable=True)


# ProductUnit:
class ProductUnit(Base):
    __tablename__ = "ProductUnit"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=True)

    # 产品段编码:
    PDUnitCode = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 产品段名称:
    PDUnitName = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Desc = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 持续时间:
    Duration = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 单位:
    Unit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 产品定义ID:
    ProductRuleID = Column(Integer, nullable=False, primary_key=False)

    # 工艺段ID:
    PUID = Column(Integer, nullable=False, primary_key=False)

    # 顺序号:
    Seq = Column(Integer, primary_key=False, autoincrement=False, nullable=True)


# ProductControlTask:
class ProductControlTask(Base):
    __tablename__ = "ProductControlTask"

    # ID:
    ID = Column(BigInteger, primary_key=True, autoincrement=True, nullable=True)

    # 产品段编码:
    PDCtrlTaskCode = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 产品段名称:
    PDCtrlTaskName = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Desc = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 低限:
    LowLimit = Column(Float(53), primary_key=False, autoincrement=False, nullable=True)

    # 高限:
    HighLimit = Column(Float(53), primary_key=False, autoincrement=False, nullable=True)

    # 相关任务数:
    RelateTaskCount = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 产品定义ID:
    ProductRuleID = Column(Integer, nullable=False, primary_key=False)

    # 工艺段ID:
    PUID = Column(Integer, nullable=False, primary_key=False)

    # 顺序号:
    Seq = Column(Integer, primary_key=False, autoincrement=False, nullable=True)


# ProductParameter:
class ProductParameter(Base):
    __tablename__ = "ProductParameter"

    # ID:
    ID = Column(BigInteger, primary_key=True, autoincrement=True, nullable=True)

    # 产品段工艺参数编码:
    PDParaCode = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 产品段工艺参数名称:
    PDParaName = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Desc = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 值:
    Value = Column(Float(53), primary_key=False, autoincrement=False, nullable=True)

    # 单位:
    Unit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 产品定义ID:
    ProductRuleID = Column(Integer, nullable=False, primary_key=False)

    # 工艺段ID:
    PUID = Column(Integer, nullable=False, primary_key=False)

    # 顺序号:
    Seq = Column(Integer, primary_key=False, autoincrement=False, nullable=True)


# ProductUnitRoute:
class ProductUnitRoute(Base):
    __tablename__ = "ProductUnitRoute"

    # ID:
    ID = Column(BigInteger, primary_key=True, autoincrement=True, nullable=True)

    # 工艺路线编码:
    PDUnitRouteCode = Column(Unicode(64), nullable=False, primary_key=False)

    # 工艺路线名称:
    PDUnitRouteName = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Desc = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 持续时间:
    Duration = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 单位:
    Unit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 产品定义ID:
    ProductRuleID = Column(Integer, nullable=False, primary_key=False)

    # 工艺段ID:
    PUID = Column(Integer, nullable=False, primary_key=False)

    # 顺序号:
    Seq = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

class PlanManager(Base):
	__tablename__ = "PlanManager"

	# ID:
	ID = Column(Integer, primary_key=True, autoincrement=True, nullable=True)

	# 调度编号:
	SchedulePlanCode = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)

	# 批次号:
	BatchID = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

	# 计划重量:
	PlanQuantity = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

	# 单位:
	Unit = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

	# 品名ID:
	BrandID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

	# 品名:
	BrandName = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

	# 计划状态:
	PlanStatus = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

	# 调度计划开始时间:
	PlanBeginTime = Column(DateTime, primary_key=False, autoincrement=False, nullable=True)

	# 计划完成时间:
	PlanEndTime = Column(DateTime, primary_key=False, autoincrement=False, nullable=True)

	# 调度类型:
	Type = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

	# # 序号:
	# Seq = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

	# PLineID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)
    #
	# PLineName = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)



# 生成表单的执行语句
Base.metadata.create_all(engine)
