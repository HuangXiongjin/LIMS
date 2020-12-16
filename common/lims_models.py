from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, DateTime, Integer, Unicode
from flask_login import LoginManager
from database.connect_db import CONNECT_DATABASE

login_manager = LoginManager()
# 创建对象的基类
engine = create_engine(CONNECT_DATABASE)
Session = sessionmaker(bind=engine)
db_session = Session()
Base = declarative_base(engine)


class WorkRecord(Base):
    """检测分发指定"""
    __tablename__ = 'WorkRecord'
    Id = Column(Integer, autoincrement=True, primary_key=True)
    # 标识
    CheckProjectNO = Column(Unicode(32), nullable=True)
    # 员工编号
    No = Column(Unicode(16), nullable=True)
    # 被分发的人
    Name = Column(Unicode(16), nullable=True)
    # 被分发的内容
    Content = Column(Unicode(16), nullable=True)


class Record(Base):
    """检验记录"""
    __tablename__ = 'Record'
    Id = Column(Integer, autoincrement=True, primary_key=True)
    # 标识
    CheckProjectNO = Column(Unicode(32), nullable=True)
    # 品名
    Product = Column(Unicode(16), nullable=True)
    # 批号
    ProductNumber = Column(Unicode(32), nullable=True)
    # 规格
    Specs = Column(Unicode(32), nullable=True)
    # 请验部门
    CheckDepartment = Column(Unicode(32), nullable=True)
    # 剂型(片剂、药膏)
    Type = Column(Unicode(32), nullable=True)
    # 批数量
    Number = Column(Unicode(32), nullable=True)
    # 取样日期
    SampleTime = Column(Unicode(32), nullable=True, default='')
    # 检验日期
    CheckTime = Column(Unicode(32), nullable=True, default='')
    # 检验依据
    Basis = Column(Unicode(128), nullable=True, default='')


class Worker(Base):
    """实验室组员"""
    __tablename__ = 'Worker'
    Id = Column(Integer, autoincrement=True, primary_key=True)
    # 员工编号
    No = Column(Unicode(32), nullable=True)
    # 姓名
    Name = Column(Unicode(16), nullable=True)
    # 组别(产品组-微生物组-物料组)
    Group = Column(Unicode(16), nullable=True)
    # 岗位(理化分析-仪器分析-样品管理-微生物分析)
    Post = Column(Unicode(16), nullable=True)


class CheckLife(Base):
    """请验生命周期"""
    __tablename__ = 'CheckLife'
    Id = Column(Integer, autoincrement=True, primary_key=True)
    # 品名唯一标识
    No = Column(Unicode(32), nullable=True)
    # 品名
    Product = Column(Unicode(16), nullable=True)
    # 类型
    ProductType = Column(Unicode(16), nullable=True)
    # 操作人
    User = Column(Unicode(16), nullable=True)
    # 操作（申请-审核-取样-接收-分发-质检中-报告-审核-放行）
    Status = Column(Unicode(16), nullable=True)
    # 时间
    OperationTime = Column(Unicode(32), nullable=True, default='')
    # 操作内容
    Work = Column(Unicode(32), nullable=True)


class QualityStandard(Base):
    """质量维护表"""
    __tablename__ = 'QualityStandard'
    Id = Column(Integer, autoincrement=True, primary_key=True)
    # 品名唯一标识
    No = Column(Unicode(32), nullable=True)
    # 品名
    Product = Column(Unicode(64), nullable=True)
    # 维护内容
    Describe = Column(Unicode(1024), nullable=True)
    # 质量类型（Character-性状， Discern-鉴别，检查-检查，Content-含量测定，Microbe-微生物限度）
    Type = Column(Unicode(16), nullable=True)
    # 法定标准
    Statutory = Column(Unicode(1024), nullable=True)


class QualityStandardCenter(Base):
    """质量标准样品表"""
    __tablename__ = 'QualityStandardCenter'
    Id = Column(Integer, autoincrement=True, primary_key=True)
    # 品名唯一标识
    No = Column(Unicode(64), nullable=True)
    # 物料名称
    Product = Column(Unicode(182), nullable=True)
    # 物料代码
    Code = Column(Unicode(64), nullable=True)
    # 物料类型
    Type = Column(Unicode(64), nullable=True)
    # 单位
    Unit = Column(Unicode(32), nullable=True)
    # 录入时间
    IntoTime = Column(Unicode(32), default='')
    # 录入人
    IntoUser = Column(Unicode(32), nullable=True, default='')
    # 上次修改时间
    AlterTime = Column(Unicode(32), nullable=True, default='')
    # 修改人
    AlterUser = Column(Unicode(32), nullable=True, default='')
    # 项目(标准要求)
    Project = Column(Unicode(128), nullable=True)
    # 标准来源
    Source = Column(Unicode(512), nullable=True)


class WorkerBook(Base):
    """员工工作台账"""
    __tablename__ = 'WorkerBook'
    Id = Column(Integer, autoincrement=True, primary_key=True)
    # 姓名
    Name = Column(Unicode(32), nullable=True)
    # 工号
    WorkNo = Column(Unicode(32), nullable=True)
    # 检验工序
    CheckProcedure = Column(Unicode(32), nullable=True)
    # 样品名称
    SampleName = Column(Unicode(32), nullable=True)
    # 批号
    SampleNumber = Column(Unicode(32), nullable=True)
    # 检测开始时间
    CheckStartTime = Column(Unicode(32), default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 检测完成时间
    CheckEndTime = Column(Unicode(32), default='')
    # 备注
    Comment = Column(Unicode(32), nullable=True)


class CheckForm(Base):
    """请验单"""
    __tablename__ = 'CheckForm'
    Id = Column(Integer, autoincrement=True, primary_key=True)
    # 样本分发接收编号
    No = Column(Unicode(32), nullable=True)
    # 请验单号
    CheckNumber = Column(Unicode(32), nullable=True)
    # 样品类别
    ProductType = Column(Unicode(32), nullable=True)
    # 品名
    Name = Column(Unicode(32), nullable=True)
    # 规格
    Specs = Column(Unicode(32), nullable=True)
    # 供货单位
    Supplier = Column(Unicode(32), nullable=True, default='无')
    # 来料批号
    ProductNumber = Column(Unicode(32), nullable=True)
    # 批号（物料代码）
    Number = Column(Unicode(32), nullable=True)
    # 数量
    Amount = Column(Unicode(16), nullable=True)
    # 单位
    Unit = Column(Unicode(8), nullable=True)
    # 请验工序
    CheckProcedure = Column(Unicode(32), nullable=True)
    # 请验项目标识
    CheckProjectNO = Column(Unicode(32), nullable=True)
    # 请验部门
    CheckDepartment = Column(Unicode(32), nullable=True)
    # 请验时间
    CheckDate = Column(Unicode(32), default=datetime.now().strftime('%Y-%m-%d'))
    # 请验人
    CheckUser = Column(Unicode(16), nullable=True, default='')
    # 审核人
    VerifyUser = Column(Unicode(16), nullable=True, default='')
    # 审核时间
    VerifyDate = Column(Unicode(32), nullable=True, default='')
    # 请验单类型（标准请验，小样请验）
    Type = Column(Unicode(16), nullable=True, default='标准请验')
    # 小样请验单审核状态（待审核，未通过，已通过）
    Status = Column(Unicode(16), nullable=True, default='待审核')
    # 请验单生命周期
    Life = Column(Unicode(16), nullable=True, default='待审核')
    # 取样人
    SampleUser = Column(Unicode(16), nullable=True, default='')
    # 取样日期
    SampleTime = Column(Unicode(16), nullable=True, default='')
    # 送样人
    SongUser = Column(Unicode(16), nullable=True, default='')
    # 接收人
    IntoUser = Column(Unicode(16), nullable=True, default='')
    # 检测分发人
    OutUser = Column(Unicode(16), nullable=True, default='')
    # 留样人
    LUser = Column(Unicode(16), nullable=True, default='')
    # 留样分发量
    LAccount = Column(Unicode(16), nullable=True, default='')
    # 复查分发量
    FAccount = Column(Unicode(16), nullable=True, default='')
    # 复查留样人
    FUser = Column(Unicode(16), nullable=True, default='')
    # 检测分发量
    JAccount = Column(Unicode(16), nullable=True, default='')
    # 分发动作（J:检验-F:复查-L:留样）
    Action = Column(Unicode(16), nullable=True, default='')
    # 实验室组长
    LaboratoryUser = Column(Unicode(16), nullable=True, default='')
    # 备注
    Comment = Column(Unicode(32), nullable=True)


class CheckProject(Base):
    """请验项目明细"""
    __tablename__ = 'CheckProject'
    Id = Column(Integer, autoincrement=True, primary_key=True)
    # 品名唯一标识
    No = Column(Unicode(32), nullable=True)
    # 品名
    Product = Column(Unicode(64), nullable=True)
    # 维护内容
    Describe = Column(Unicode(1024), nullable=True)
    # 质量类型（Character-性状， Discern-鉴别，检查-检查，Content-含量测定，Microbe-微生物限度）
    Type = Column(Unicode(16), nullable=True)
    # 法定标准
    Statutory = Column(Unicode(1024), nullable=True)
    # 全局唯一地址
    CheckProjectNO = Column(Unicode(128), nullable=True)


class Distribute(Base):
    """样品分发"""
    __tablename__ = 'Distribute'
    Id = Column(Integer, autoincrement=True, primary_key=True)
    # 请验项目标识
    CheckProjectNO = Column(Unicode(32), nullable=True)
    # 分发人
    User = Column(Unicode(32), nullable=True)
    # 分发编号
    No = Column(Unicode(32), nullable=True)
    # 分配数量
    Number = Column(Unicode(32), nullable=True, default='')
    # 分配组
    Group = Column(Unicode(32), nullable=True, default='')
    # 指派人
    GroupUser = Column(Unicode(32), nullable=True, default='')
    # 分发时间
    Time = Column(Unicode(32), nullable=True, default='')


class WordForm(Base):
    """文档维护"""
    __tablename__ = 'WordForm'
    Id = Column(Integer, autoincrement=True, primary_key=True)
    # 文档名称
    FileName = Column(Unicode(64), nullable=True)
    # 品名
    Product = Column(Unicode(64), nullable=True)
    # 路径
    FilePath = Column(Unicode(64), nullable=True)


class ConclusionRecord(Base):
    """报告完成记录"""
    __tablename__ = 'ConclusionRecord'
    Id = Column(Integer, autoincrement=True, primary_key=True)
    # 检验编号
    CheckNumber = Column(Unicode(32), nullable=True)
    # 请验单日期
    TestDate = Column(Unicode(32), default='')
    # 实际送样时间
    ActualTime = Column(Unicode(32), default='')
    # 检验日期
    CheckDate = Column(Unicode(32), default='')
    # 产品名称
    Name = Column(Unicode(32), nullable=True)
    # 产品批号
    ProductNumber = Column(Unicode(32), nullable=True)
    # 送样部门
    SampleDepartment = Column(Unicode(32), nullable=True)
    # 类别(成品、药膏、中间产品、原料、辅料)
    Type = Column(Unicode(32), nullable=True)
    # 药剂类型
    medicine = Column(Unicode(32), nullable=True)
    # 规格
    Specs = Column(Unicode(32), nullable=True)
    # 大小样
    BigLevel = Column(Unicode(32), nullable=True)
    # 药膏
    ointment = Column(Unicode(32), nullable=True)
    # 检验项目
    CheckProject = Column(Unicode(32), nullable=True)
    # 法定标准
    StatutoryStandards = Column(Unicode(32), nullable=True)
    # 内验标准
    InnerStandards = Column(Unicode(32), nullable=True)
    # 检验结果
    Comment = Column(Unicode(32), nullable=True)
    # 判定
    Judge = Column(Unicode(32), nullable=True)
    # 检验人
    CheckName = Column(Unicode(32), nullable=True)


class ProductSave(Base):
    """产品留样单"""
    __tablename__ = 'ProductSave'
    Id = Column(Integer, autoincrement=True, primary_key=True)
    # 请样标识
    CheckProjectNO = Column(Unicode(32), nullable=True)
    # 留样标识
    ProductSaveNo = Column(Unicode(32), nullable=True)
    # 产品名称
    Name = Column(Unicode(32), nullable=True)
    # 规格
    Specs = Column(Unicode(32), nullable=True)
    # 包装规格
    PackSpecs = Column(Unicode(32), nullable=True)
    # 产品批号
    ProductNumber = Column(Unicode(32), nullable=True)
    # 理论产量
    TheoreticalYield = Column(Unicode(32), nullable=True)
    # 留样数量
    BatchAmount = Column(Unicode(32), nullable=True)
    # 留样部门
    BatchDepartment = Column(Unicode(32), nullable=True)
    # 留样人
    BatchName = Column(Unicode(32), nullable=True)
    # 留样日期
    BatchTime = Column(Unicode(32), nullable=True, default='')
    # 经手人
    Handler = Column(Unicode(32), nullable=True)
    # 生产日期
    ProductionDate = Column(Unicode(32), nullable=True, default='')
    # 有效日期
    ValidityDate = Column(Unicode(32), nullable=True, default='')
    # 备注
    Comment = Column(Unicode(32), nullable=True)


class ProductSaveSurvey(Base):
    """产品留样观察表"""
    __tablename__ = 'ProductSaveSurvey'

    Id = Column(Integer, autoincrement=True, primary_key=True)
    # 品名
    Name = Column(Unicode(32), nullable=True)
    # 温度
    Temperature = Column(Unicode(32), nullable=True)
    # 相对湿度
    RH = Column(Unicode(32), nullable=True)
    # 留样位置
    position = Column(Unicode(32), nullable=True)
    # 留样批号
    BatchNumber = Column(Unicode(32), nullable=True)
    # 留样日期
    BatchDate = Column(Unicode(32), nullable=True, default=datetime.now().strftime('%Y-%m-%d'))
    # 规格
    Specs = Column(Unicode(32), nullable=True)
    # 留样量
    BatchAmount = Column(Unicode(32), nullable=True)
    # 经手人
    Handler = Column(Unicode(32), nullable=True)
    # 观察项目
    Project = Column(Unicode(32), nullable=True)
    # 观察结果（按月统计）
    # 6个月
    SixMonth = Column(Unicode(32), nullable=True)
    # 12个月
    TwelveMonth = Column(Unicode(32), nullable=True)
    # 18个月
    EighteenMonth = Column(Unicode(32), nullable=True)
    # 24个月
    TwentyFourMonth = Column(Unicode(32), nullable=True)
    # 30个月
    ThirtyMonth = Column(Unicode(32), nullable=True)
    # 36个月
    ThirtySix = Column(Unicode(32), nullable=True)
    # 48个月
    FortyEight = Column(Unicode(32), nullable=True)
    # 结论
    Conclude = Column(Unicode(32), nullable=True)
    # 备注
    Comment = Column(Unicode(32), nullable=True)


# class Instrument(Base):
#     """仪器表"""
#     __tablename__ = 'Instrument'

class KeepPlan(Base):
    """仪器保养计划表"""
    __tablename__ = 'KeepPlan'

    ID = Column(Integer, autoincrement=True, primary_key=True)
    # 工单号
    No = Column(Unicode(128), nullable=True, default=datetime.now().strftime('%Y%m%d%H%M%S'))
    # 仪器编码
    InstrumentCode = Column(Unicode(128), nullable=True)
    # 制定计划人
    Worker = Column(Unicode(32), nullable=True)
    # 工单状态
    Status = Column(Unicode(32), default="待保养")
    # 制定计划时间
    ApplyTime = Column(Unicode(32), nullable=True, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 保养班组
    # Group = Column(Unicode(32), nullable=True)
    # 任务开始时间（递增）
    StartTime = Column(Unicode(32), nullable=True)
    # 计划描述
    Describe = Column(Unicode(128), nullable=True)
    # 工作周期
    WeekTime = Column(Unicode(128), nullable=True)
    # 工作类型
    Type = Column(Unicode(32), nullable=True)
    # 工作时间
    WorkTime = Column(Unicode(128), nullable=True)


class KeepTask(Base):
    """保养任务表"""
    __tablename__ = 'KeepTask'

    ID = Column(Integer, autoincrement=True, primary_key=True)
    # 工单号
    No = Column(Unicode(128), nullable=True, default=datetime.now().strftime('%Y%m%d%H%M%S'))
    # 仪器编码
    InstrumentCode = Column(Unicode(128), nullable=True)
    # 制定计划人
    Worker = Column(Unicode(32), nullable=True)
    # 保养班组
    Group = Column(Unicode(32), nullable=True)
    # 工单状态
    Status = Column(Unicode(32), nullable=True)
    # 制定计划时间
    ApplyTime = Column(Unicode(32), nullable=True, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 保养确认人
    # KeepWorker = Column(Unicode(32), nullable=True)
    # 任务开始时间（递增）
    StartTime = Column(Unicode(32), nullable=True, default='尚未接单')
    # 计划描述
    Describe = Column(Unicode(128), nullable=True)
    # 工作周期
    WeekTime = Column(Unicode(128), nullable=True)
    # 工作类型
    Type = Column(Unicode(32), nullable=True)
    # 工作时间
    WorkTime = Column(Unicode(128), nullable=True)


class KeepRecord(Base):
    """保养记录表"""
    __tablename__ = 'KeepRecord'

    ID = Column(Integer, autoincrement=True, primary_key=True)
    # 工单号
    No = Column(Unicode(128), nullable=True, default=datetime.now().strftime('%Y%m%d%H%M%S'))
    # 仪器编码
    InstrumentCode = Column(Unicode(128), nullable=True)
    # 制定计划人
    Worker = Column(Unicode(32), nullable=True)
    # 保养班组
    Group = Column(Unicode(32), nullable=True)
    # 工单状态
    Status = Column(Unicode(32), default="已完成")
    # 制定计划时间
    ApplyTime = Column(Unicode(32), nullable=True, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 保养确认人
    KeepWorker = Column(Unicode(32), nullable=True)
    # 任务开始时间（递增）
    StartTime = Column(Unicode(32), nullable=True)
    # 计划描述
    Describe = Column(Unicode(128), nullable=True)
    # 保养内容
    Content = Column(Unicode(128), nullable=True)
    # 工作周期
    WeekTime = Column(Unicode(128), nullable=True)
    # 完成时间
    EndTime = Column(Unicode(32), nullable=True)
    # 工作类型
    Type = Column(Unicode(32), nullable=True)


class Repair(Base):
    """维修申请表"""
    __tablename__ = 'Repair'

    ID = Column(Integer, autoincrement=True, primary_key=True)
    # 工单号
    No = Column(Unicode(128), nullable=True, default=datetime.now().strftime('%Y%m%d%H%M%S'))
    # 仪器编码
    InstrumentCode = Column(Unicode(128), nullable=True)
    # 申请人
    Worker = Column(Unicode(32), nullable=True)
    # 故障阐述
    FaultExpound = Column(Unicode(128), nullable=True)
    # 工单状态（待接单，已接单）
    Status = Column(Unicode(32), default="待接单")
    # 申请时间
    ApplyTime = Column(Unicode(32), nullable=True, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 接单人
    ReceiveWorker = Column(Unicode(32), nullable=True, default='')
    # 接单时间
    ReceiveTime = Column(Unicode(32), nullable=True, default='尚未接单')


class RepairTask(Base):
    """维修任务表"""
    __tablename__ = 'RepairTask'

    ID = Column(Integer, autoincrement=True, primary_key=True)
    # 工单号
    No = Column(Unicode(128), nullable=True)
    # 仪器编码
    InstrumentCode = Column(Unicode(128), nullable=True)
    # 仪器名称
    # Name = Column(Unicode(32), nullable=True)
    # 申请人
    Worker = Column(Unicode(32), nullable=True)
    # 维修人
    ReceiveWorker = Column(Unicode(32), nullable=True)
    # 工单状态（维修完成）
    Status = Column(Unicode(32), default="维修完成")
    # 维修内容
    Content = Column(Unicode(128), nullable=True)
    # 申请时间
    ApplyTime = Column(Unicode(32), nullable=True)
    # 接单时间
    ReceiveTime = Column(Unicode(32), nullable=True)
    # 完成时间
    EndTime = Column(Unicode(32), nullable=True)


class LimsError(Base):
    """实验室管理系统运行错误 """
    __tablename__ = 'LimsError'
    Id = Column(Integer, autoincrement=True, primary_key=True)
    # 时间
    Time = Column(Unicode(32), default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 操作人
    User = Column(Unicode(32), nullable=True)
    # ip
    IP = Column(Unicode(32), nullable=True)
    # 调用函数
    Func = Column(Unicode(32), nullable=True)
    # 错误信息
    Error = Column(Unicode(64), nullable=True)


class ClassifyTree(Base):
    """分类维护表"""
    __tablename__ = "ClassifyTree"
    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # tag点编号
    TagCode = Column(Unicode(100), nullable=True)
    # tag点名称
    TagName = Column(Unicode(100), nullable=True)
    # 上级tag点
    ChildrenTag = Column(Unicode(100), nullable=True)
    # 父节点
    ParentTag = Column(Unicode(100), nullable=True)


# 生成表单的执行语句
Base.metadata.create_all(engine)
