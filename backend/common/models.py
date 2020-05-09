import datetime

from backend import db


class Users(db.Model):
    __tablename__ = 'users'
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    # 用户名 唯一索引
    username = db.Column(db.String(128), unique=True, nullable=False)
    # 密码 必填字段
    password = db.Column(db.String(512), nullable=False)
    # 姓名 创建索引，加快查询
    fullname = db.Column(db.String(128), index=True, nullable=False)
    # 状态 (1: 生效 0: 禁用)
    status = db.Column(db.SmallInteger, default=1, nullable=False)
    # 创建时间 默认当前时间
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, index=True)

    def __repr__(self):
        return 'username=%s' % self.username
