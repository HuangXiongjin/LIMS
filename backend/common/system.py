from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, ForeignKey, Table, Column, DateTime, Integer, String, Unicode, Float
from sqlalchemy.dialects.mssql.base import BIT
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import LoginManager

from backend.database.connect_db import CONNECT_DATABASE

login_manager = LoginManager()
# 创建对象的基类
engine = create_engine(CONNECT_DATABASE, deprecate_large_types=True)
Session = sessionmaker(bind=engine)
db_session = Session()
Base = declarative_base(engine)




# 页面路由配置
class PageRoute(Base):
    __tablename__ = 'PageRoute'
    # id:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 页面路由配置:
    SetRoute = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 页面路径名（XX.html）:
    PageRouteName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 路由:
    Route = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)



# 数据库建表配置
class CreateTableSet(Base):
    __tablename__ = 'CreateTableSet'
    # id:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 表名:
    TableName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 表的描述:
    TableDescrip = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # # 表类型（分页表/下拉框数据表）:
    # TableType = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 是否在第一列显示多选框（checkbox）:
    ISFirstCheckBox = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 是否实现单选，设为true则复选框只能选择一行:
    SingleSelect = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 是否显示添加按钮:
    IsAdd = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 是否显示修改按钮:
    IsUpdate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 是否显示删除按钮:
    IsDelete = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # ID字段:
    TableID = Column(Unicode(32), default="ID", primary_key=False, autoincrement=False, nullable=True)


# 4.表字段配置：选择一个表，将此表的数据（字段）显示出来（新表只有ID）
# 字段表表头
class FieldSet(Base):
    __tablename__ = 'FieldSet'
    # id:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 表名称:
    TableName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # title字段名称（名字）:
    TitleName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # field字段名（name）:
    FieldName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # isedit是否做添加修改操作（默认否）:
    Isedit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # edittype输入类型，输入框/下拉框/时间选择框（满足上一条可做编辑操作，默认输入框）:
    Edittype = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # downtable下拉框的数据表（满足上一条选择下拉框，选择一个表）:
    Downtable = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # sortable该列是否排序,表头显示双箭头(默认false):
    Sortable = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # order该列排序方式，满足上条可排序，默认asc( asc/desc):
    Order = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # visible该列是否可见(默认true):
    Visible = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # VARCHAR长度:
    length = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 字段类型:
    type = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 字段注释:
    comment = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 是否为主键（默认False）:
    primarykey = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 是否自增（默认False）:
    autoincrement = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 是否为空（默认True）:
    nullable = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 列宽:
    width = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# 是否
class ISFlag(Base):
    __tablename__ = 'ISFlag'
    # id:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 标识:
    Flag = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Description = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# 是否
class InputTypeTable(Base):
    __tablename__ = 'InputTypeTable'
    # id:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 类型:
    Type = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 名称:
    Title = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# 表字段类型
class FieldType(Base):
    __tablename__ = 'FieldType'
    # id:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 类型:
    Type = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Description = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# 审计追踪
class AuditTrace(Base):
    __tablename__ = 'AuditTrace'
    # id:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 操作:
    Operation = Column(Unicode(300), primary_key=False, autoincrement=False, nullable=True)

    # 详细信息:
    DeitalMSG = Column(Unicode(800), primary_key=False, autoincrement=False, nullable=True)

    # 修改日期
    ReviseDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 操作表:
    TableName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 用户:
    User = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 其他:
    Other = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


class SysLog(Base):
    __tablename__ = "SysLog"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=True)

    # IP:
    IP = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 计算机名称:
    ComputerName = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 操作用户:
    UserName = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 操作日期:
    OperationDate = Column(DateTime, primary_key=False, autoincrement=False, nullable=True)

    # 操作内容:
    OperationContent = Column(Unicode(2048), primary_key=False, autoincrement=False, nullable=True)

    # 类型:
    OperationType = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)


# User_START:
class User(Base):
    __tablename__ = "User"

    # id:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 用户名:
    Name = Column(Unicode(64), primary_key=False, autoincrement=False, nullable=True)

    # 密码:
    Password = Column(Unicode(150), primary_key=False, autoincrement=False, nullable=True)

    # 工号:
    WorkNumber = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 所属岗位:
    StationName = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 登录状态:
    Status = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # session_id:
    session_id = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 所属部门:
    OrganizationName = Column(Unicode(50), primary_key=False, autoincrement=False, nullable=True)

    # 所属厂区:
    FactoryName = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 上次登录时间:
    LastLoginTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 创建时间:
    CreateTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 创建用户:
    Creater = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 是否锁定:
    IsLock = Column(BIT, primary_key=False, autoincrement=False, nullable=True)

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute')

    # 定义password字段的写方法，我们调用generate_password_hash将明文密码password转成密文Shadow
    # @password.setter
    def password(self, password):
        self.Password = generate_password_hash(password)
        return self.Password

    # 定义验证密码的函数confirm_password
    def confirm_password(self, password):
        return check_password_hash(self.Password, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.ID)  # python 3


# User_END:



# 生成表单的执行语句
Base.metadata.create_all(engine)
