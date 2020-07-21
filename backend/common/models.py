import datetime

from backend import db


class Equipment(db.Model):
    """设备数据"""
    __tablename__ = 'equipment'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 车间号
    workshop_no = db.Column(db.Unicode(128), nullable=True)
    # 设备号
    equipment_no = db.Column(db.Unicode(128), nullable=False)
    # 设备名称
    name = db.Column(db.Unicode(32), nullable=False)
    # 设备型号
    model = db.Column(db.Unicode(128), nullable=True)
    # 设备类型
    type = db.Column(db.Unicode(32), nullable=True)
    # 生产商
    manufacturer = db.Column(db.Unicode(32), nullable=False)
    # SAP号
    sap = db.Column(db.Unicode(64), nullable=True)
    # 固定资产编号
    fixed_assets_no = db.Column(db.Unicode(128), nullable=True)
    # 固定资产名称
    fixed_assets_name = db.Column(db.Unicode(32), nullable=True)
    # 设备状态(1:良好 0：异常)
    status = db.Column(db.Unicode(16), default='良好', nullable=False)
    # 区域
    area = db.Column(db.Unicode(32), nullable=True)
    # 进厂日期
    into_time = db.Column(db.Unicode(32), nullable=True, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 中间表ID
    # center_id = db.Column(db.Integer, primary_key=True)


class InstructionsCenter(db.Model):
    """说明书中间表"""
    __tablename__ = 'instructionsCenter'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 设备/配件编号
    no = db.Column(db.Unicode(32), nullable=False)
    # 说明书ID
    instructions = db.relationship("Instructions", backref='instructionsCenter')


class Instructions(db.Model):
    """设备/配件说明书"""
    __tablename__ = 'instructions'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 说明书编号
    no = db.Column(db.Unicode(128), nullable=False)
    # 说明书类型
    type = db.Column(db.Unicode(32), nullable=False)
    # 说明书详情
    detail = db.Column(db.Unicode(256), nullable=False)
    # 中间表id
    center_id = db.Column(db.Integer, db.ForeignKey('instructionsCenter.id'))


class Fitting(db.Model):
    """配件数据"""
    __tablename__ = 'fitting'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 设备号
    equipment_no = db.Column(db.Unicode(128), nullable=True)
    # 配件编号
    fitting_no = db.Column(db.Unicode(128), nullable=False)
    # 配件名称
    name = db.Column(db.Unicode(64), nullable=False)
    # 配件型号
    model = db.Column(db.Unicode(128), nullable=False)
    # 配件类型
    type = db.Column(db.Unicode(32), nullable=False)
    # 使用状态
    status = db.Column(db.Unicode(8), default="未使用")
    # 生产商
    manufacturer = db.Column(db.Unicode(64), nullable=True)
    # 进厂日期
    time = db.Column(db.Unicode(32), nullable=True, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 中间表ID
    # center_id = db.Column(db.Integer, primary_key=True)


class FittingInto(db.Model):
    """配件入库"""
    __tablename__ = 'fitting_into'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 入库单号
    no = db.Column(db.Unicode(256), nullable=False)
    # 配件编号
    fitting_no = db.Column(db.Unicode(1024), nullable=False)
    # 配件数量
    fitting_number = db.Column(db.Unicode(256), nullable=False)
    # 验收状态
    status = db.Column(db.Unicode(8), default="否")
    # 验收人员
    worker = db.Column(db.Unicode(128), nullable=False)
    # 入库时间
    time = db.Column(db.Unicode(32), nullable=True, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class FittingOut(db.Model):
    """配件出库"""
    __tablename__ = 'fitting_out'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 出库单号
    no = db.Column(db.Unicode(256), nullable=False)
    # 配件编号
    fitting_no = db.Column(db.Unicode(1024), nullable=False)
    # 配件数量
    fitting_number = db.Column(db.Unicode(256), nullable=False)
    # 出库人员
    out_worker = db.Column(db.Unicode(128), nullable=False)
    # 领用人员
    use_worker = db.Column(db.Unicode(128), nullable=False)
    # 出库时间
    time = db.Column(db.Unicode(32), nullable=True, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class Stock(db.Model):
    """库存统计"""
    __tablename__ = 'stock'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 配件型号
    type = db.Column(db.Unicode(64), nullable=False)
    # 使用数量
    use_count = db.Column(db.Unicode(64), nullable=True)
    # 剩余数量
    stock_count = db.Column(db.Unicode(64), nullable=True)
    # 清点人员
    worker = db.Column(db.Unicode(128), nullable=False)
    # 清点时间
    time = db.Column(db.Unicode(32), nullable=True, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 库存预警
    status = db.Column(db.Unicode(32), default="库存充足")


class WorkOrder(db.Model):
    """工单记录"""
    __tablename__ = 'work_order'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 工单号
    no = db.Column(db.Unicode(256), nullable=False)
    # 设备号
    equipment_no = db.Column(db.Unicode(256), nullable=False)
    # 车间号
    workshop_no = db.Column(db.Unicode(128), nullable=False)
    # 员工号
    worker_no = db.Column(db.Unicode(128), nullable=False)
    # 姓名
    name = db.Column(db.Unicode(32), nullable=False)
    # 工单状态（待处理，待审核，执行中，已完成）
    status = db.Column(db.Unicode(32), default="待处理")
    # 工单类型（维修，保养，润滑，巡检）
    type = db.Column(db.Unicode(32), nullable=True)
    # 开始时间
    start_time = db.Column(db.Unicode(32), nullable=True, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 结束时间
    end_time = db.Column(db.Unicode(32), nullable=True, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class Scheduling(db.Model):
    """排班表"""
    __tablename__ = 'scheduling'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 设备号
    equipment_no = db.Column(db.Unicode(256), nullable=False)
    # 车间号
    workshop_no = db.Column(db.Unicode(128), nullable=False)
    # 工单号
    no = db.Column(db.Unicode(256), nullable=False)
    # 班组号
    work_no = db.Column(db.Unicode(64), nullable=False)
    # 班次号
    work_group = db.Column(db.Unicode(64), nullable=False)


class FaultRepair(db.Model):
    """故障报修"""
    __tablename__ = 'fault_repair'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 设备号
    equipment_no = db.Column(db.Unicode(256), nullable=False)
    # 车间号
    workshop_no = db.Column(db.Unicode(128), nullable=False)
    # 工单号
    no = db.Column(db.Unicode(256), nullable=False)
    # 员工号
    worker_no = db.Column(db.Unicode(128), nullable=False)
    # 姓名
    name = db.Column(db.Unicode(32), nullable=False)
    # 故障原因
    reason = db.Column(db.Unicode(128), nullable=False)
    # 故障图片
    picture = db.Column(db.Unicode(128), nullable=False)
    # 申请时间
    time = db.Column(db.Unicode(32), nullable=True, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class Record(db.Model):
    """保润检记录表"""
    __tablename__ = "record"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 设备号
    equipment_no = db.Column(db.Unicode(256), nullable=False)
    # 工单号
    no = db.Column(db.Unicode(256), nullable=False)
    # 员工号
    worker_no = db.Column(db.Unicode(128), nullable=False)
    # 姓名
    name = db.Column(db.Unicode(32), nullable=False)
    # 工单类型（维修，保养，润滑，巡检）
    type = db.Column(db.Unicode(32), nullable=True)
    # 设备状态（良好,异常）
    status = db.Column(db.Unicode(32), default="良好")
    # 工作时间
    time = db.Column(db.Unicode(32), nullable=True, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class RepairRecord(db.Model):
    """维修记录表"""
    __tablename__ = 'repair_record'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 设备号
    equipment_no = db.Column(db.Unicode(256), nullable=False)
    # 工单号
    no = db.Column(db.Unicode(256), nullable=False)
    # 员工号
    worker_no = db.Column(db.Unicode(128), nullable=False)
    # 设备状态（良好，异常）
    status = db.Column(db.Unicode(12), default="良好")
    # 故障原因
    fault_reason = db.Column(db.Unicode(128), nullable=False)
    # 维修材料
    repair_material = db.Column(db.Unicode(128), nullable=False)
    # 修复验收(是， 否)
    repair_status = db.Column(db.Unicode(12), default="否")
    # 故障等级(一级， 二级， 三级)
    fault_rank = db.Column(db.Unicode(12), default="一级")
    # 维修知识
    knowledge = db.Column(db.Unicode(256), nullable=False)
    # 工作时间
    time = db.Column(db.Unicode(32), nullable=True, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class RepairPlan(db.Model):
    """维保检方案"""
    __tablename__ = 'repair_plan'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 设备号
    equipment_no = db.Column(db.Unicode(256), nullable=False)
    # 方案编号
    plan_no = db.Column(db.Unicode(128), nullable=False)
    # 部位
    position = db.Column(db.Unicode(64), nullable=False)
    # 工具
    tools = db.Column(db.Unicode(64), nullable=False)
    # 材料
    material = db.Column(db.Unicode(64), nullable=False)
    # 方法
    plan = db.Column(db.Unicode(64), nullable=False)
    # 标准
    standard = db.Column(db.Unicode(32), nullable=False)
    # 周期
    period = db.Column(db.Unicode(32), nullable=False)
    # 实施部门
    department = db.Column(db.Unicode(32), nullable=False)
    # 工单类型（维修，保养，巡检）
    type = db.Column(db.Unicode(32), nullable=True)


class LubricationPlan(db.Model):
    """润滑方案"""
    __tablename__ = 'lubrication_plan'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 设备号
    equipment_no = db.Column(db.Unicode(256), nullable=False)
    # 方案编号
    plan_no = db.Column(db.Unicode(128), nullable=False)
    # 润滑部位
    position = db.Column(db.Unicode(64), nullable=False)
    # 润滑油品
    oils = db.Column(db.Unicode(32), nullable=False)
    # 润滑方式
    way = db.Column(db.Unicode(32), nullable=False)
    # 换油数量
    changes_amount = db.Column(db.Unicode(32), nullable=False)
    # 换油周期
    oils_changes_period = db.Column(db.Unicode(32), nullable=False)
    # 加油数量
    add_amount = db.Column(db.Unicode(32), nullable=False)
    # 加油周期
    oils_add_period = db.Column(db.Unicode(32), nullable=False)
    # 实施部门
    department = db.Column(db.Unicode(32), nullable=False)


class OrderVerify(db.Model):
    """工单审核"""
    __tablename__ = 'orderVerify'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 工单号
    no = db.Column(db.Unicode(256), nullable=False)
    # 审核人
    name = db.Column(db.Unicode(32), nullable=False)
    # 审核状态（待审核，审核通过）
    verify_status = db.Column(db.Unicode(32), default="待审核")
    # 审核时间
    verify_time = db.Column(db.Unicode(32), nullable=True, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 计划表
    # plan = db.relationship("Plan", backref='orderVerify')


class Plan(db.Model):
    """维保润检计划表"""
    __tablename__ = 'plan'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 设备号
    equipment_no = db.Column(db.Unicode(256), nullable=False)
    # 车间号
    workshop_no = db.Column(db.Unicode(128), nullable=False)
    # 工单号
    no = db.Column(db.Unicode(256), nullable=False)
    # 创建员工号
    worker_no = db.Column(db.Unicode(128), nullable=False)
    # 创建人姓名
    name = db.Column(db.Unicode(32), nullable=False)
    # 工单状态（待处理，待审核，执行中，已完成）
    no_status = db.Column(db.Unicode(32), default="待处理")
    # 审核状态（待审核，审核通过）
    verify_status = db.Column(db.Unicode(32), default="待审核")
    # 提醒状态（待提醒，已提醒）
    remind_status = db.Column(db.Unicode(32), default="待提醒")
    # 工单类型（维修，保养，润滑，巡检）
    type = db.Column(db.Unicode(32), nullable=True)
    # 预工作时间
    work_time = db.Column(db.Unicode(32), nullable=True, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 创建时间
    found_time = db.Column(db.Unicode(32), nullable=True, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 方案编号
    plan_no = db.Column(db.Unicode(128), nullable=False)
    # 审核人
    # verify_id = db.Column(db.Integer, db.ForeignKey('orderVerify.id'))


class Task(db.Model):
    """任务表"""
    __tablename__ = 'task'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 设备号
    equipment_no = db.Column(db.Unicode(128), nullable=False)
    # 车间号
    workshop_no = db.Column(db.Unicode(128), nullable=False)
    # 工单号
    no = db.Column(db.Unicode(256), nullable=False)
    # 发放人
    name = db.Column(db.Unicode(32), nullable=False)
    # 工单状态（待处理，待审核，执行中，已完成）
    no_status = db.Column(db.Unicode(32), default="待处理")
    # 工单类型（维修，保养，润滑，巡检）
    type = db.Column(db.Unicode(32), nullable=True)
    # 工时要求
    work_require = db.Column(db.Unicode(32), nullable=True)
    # 下发时间
    found_time = db.Column(db.Unicode(32), nullable=True, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class Monitor(db.Model):
    """设备实时监测数据"""
    __tablename__ = 'monitor'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 设备号
    equipment_no = db.Column(db.Unicode(128), nullable=False)
    # 当前状态（1：良好 0：异常）
    status = db.Column(db.SmallInteger, default=1, nullable=False)
    # 运行总时间
    total_time = db.Column(db.Unicode(64), nullable=True)
    # 停机总时间
    stop_time = db.Column(db.Unicode(64), nullable=True)
    # 维修时间
    repair_time = db.Column(db.Unicode(64), nullable=True)
    # 故障次数
    stop_count = db.Column(db.Unicode(64), nullable=True)


class Kpi(db.Model):
    """设备KPI"""
    __tablename__ = 'kpi'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 设备编号
    equipment_no = db.Column(db.Unicode(128), nullable=False)
    # 设备完好率
    whl = db.Column(db.Unicode(64), nullable=True)
    # 设备故障率
    gzl = db.Column(db.Unicode(64), nullable=True)
    # 维修费用率
    wxfyl = db.Column(db.Unicode(64), nullable=True)
    # 故障停机率
    gztjl = db.Column(db.Unicode(64), nullable=True)
    # 维修完成率
    wxwcl = db.Column(db.Unicode(64), nullable=True)
    # 全局设备率
    qjsbl = db.Column(db.Unicode(64), nullable=True)
    # 故障发生次数
    count = db.Column(db.Unicode(64), nullable=True)



