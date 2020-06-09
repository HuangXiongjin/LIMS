# import datetime
#
from backend import db


class Users(db.Model):
    """用户基本数据"""
    __tablename__ = 'Users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 姓名
    name = db.Column(db.String(128), nullable=False)
    # 编号
    number = db.Column(db.String(128), nullable=False)
    # 电话
    phone = db.Column(db.String(32), nullable=False)
    # 地址
    address = db.Column(db.String(128), nullable=False)


#
#
# class Equipment(db.Model):
#     """设备基本数据"""
#     __tablename__ = 'Equipment'
#
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     # 车间编号
#     workshop_no = db.Column(db.String(128), nullable=False)
#     # 设备编号
#     number = db.Column(db.String(128), nullable=False)
#     # 设备名称
#     name = db.Column(db.String(32), nullable=False)
#     # 设备型号
#     model = db.Column(db.String(128), nullable=False)
#     # 设备类型
#     type = db.Column(db.String(32), nullable=False)
#     # 生产商
#     manufacturer = db.Column(db.String(32), nullable=False)
#     # SAP号
#     sap = db.Column(db.String(64), nullable=False)
#     # 固定资产编号
#     fixed_assets_no = db.Column(db.String(128), nullable=False)
#     # 固定资产名称
#     fixed_assets_name = db.Column(db.String(32), nullable=False)
#     # 设备状态(1:良好 0：异常)
#     status = db.Column(db.SmallInteger, default=1, nullable=False)
#     # 区域
#     area = db.Column(db.String(32), nullable=False)
#     # 进厂日期
#     into_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
#     # 中间表ID
#     center_id = db.Column(db.Integer, primary_key=True)
#
#
# class InstructionsCenter(db.Model):
#     """说明书中间表"""
#     __tablename__ = 'InstructionsCenter'
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     # 设备/器件编号
#     number = db.Column(db.String(32), nullable=False)
#     # 说明书ID
#     instructions = db.Column(db.Integer, primary_key=True)
#
#
# class Instructions(db.Model):
#     """设备/器件说明书"""
#     __tablename__ = 'Instructions'
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     # 说明书编号
#     number = db.Column(db.String(128), nullable=False)
#     # 说明书类型
#     type = db.Column(db.String(32), nullable=False)
#     # 说明书详情
#     detail = db.Column(db.String(256), nullable=False)
#
#
# class Device(db.Model):
#     """器件基本数据"""
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     # 车间编号
#     workshop_no = db.Column(db.String(128), nullable=False)
#     # 器件编号
#     number = db.Column(db.String(128), nullable=False)
#     # 器件名称
#     name = db.Column(db.String(32), nullable=False)
#     # 器件型号
#     model = db.Column(db.String(128), nullable=False)
#     # 器件类型
#     type = db.Column(db.String(32), nullable=False)
#     # 生产商
#     manufacturer = db.Column(db.String(32), nullable=False)
#     # 进厂日期
#     into_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
#     # 中间表ID
#     center_id = db.Column(db.Integer, primary_key=True)
#
#
# class Monitor(db.Model):
#     """设备实时监测"""
#     __tablename__ = 'monitor'
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     # 设备编号
#     number = db.Column(db.String(128), nullable=False)
#     # 当前状态（1：良好 0：异常）
#     status = db.Column(db.SmallInteger, default=1, nullable=False)
#     # 运行总时间
#     total_time = db.Column(db.String(128), nullable=True)
#     # 停机总时间
#     stop_time = db.Column(db.String(128), nullable=True)
#     # 时间
#
#
# class Users(db.Model):
#     __tablename__ = 'users'
#     # 主键
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     # 用户名 唯一索引
#     username = db.Column(db.String(128), unique=True, nullable=False)
#     # 密码 必填字段
#     password = db.Column(db.String(512), nullable=False)
#     # 姓名 创建索引，加快查询
#     fullname = db.Column(db.String(128), index=True, nullable=False)
#     # 状态 (1: 生效 0: 禁用)
#     status = db.Column(db.SmallInteger, default=1, nullable=False)
#     # 创建时间 默认当前时间
#     created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, index=True)
#
#     def __repr__(self):
#         return 'username=%s' % self.username
