# /******************************************************************************************
# ************* STK make model usage:
# ************* version: print python3.6.3  version
# ************* make: make Python file
# ************* STK makemodel.py 1.0.0
# ************* @author Xujin
# ************* @date 2019-08-09 15:58:36
# ************* @Model 
# ******************************************************************************************/

# 引入必要的类库
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, ForeignKey, Table, DateTime, Integer, String
from sqlalchemy import Column, DateTime, Float, Integer, String, Unicode, BigInteger
from sqlalchemy.dialects.mssql.base import BIT
from datetime import datetime
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

# 引入mssql数据库引擎
import pymssql

# 创建对象的基类
from backend import CONNECT_DATABASE

engine = create_engine(CONNECT_DATABASE, deprecate_large_types=True,
                       max_overflow=0,  # 超过连接池大小外最多创建的连接
                       pool_size=100,  # 连接池大小
                       pool_timeout=50,  # 池中没有线程最多等待的时间，否则报错
                       pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
                       # echo = True   #输出SQL
                       )
SessionFactory = sessionmaker(bind=engine)
session = SessionFactory()
Base = declarative_base(engine)

# Role_Menu_START:
# 菜单与角色关联表
Role_Menu = Table(
    "role_menu",
    Base.metadata,
    Column("Role_ID", Integer, ForeignKey("Role.ID"), nullable=False, primary_key=True),
    Column("Menu_ID", Integer, ForeignKey("Menu.ID"), nullable=False, primary_key=True)
)

# Role_Menu_END:


# DepartmentManager_START:
class DepartmentManager(Base):
    '''部门'''
    __tablename__ = "DepartmentManager"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 部门名称:
    DepartName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 部门编码:
    DepartCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 所属厂区:
    DepartLoad = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# DepartmentManager_END:

# MenuType_START:
class MenuType(Base):
    __tablename__ = "MenuType"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 类型名称:
    TypeName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 类型编码:
    TypeCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# MenuType_END:

# Role_START:
class Role(Base):
    '''角色'''
    __tablename__ = "Role"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 角色编码:
    RoleCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # RoleName:
    RoleName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # Description:
    Description = Column(Unicode(50), primary_key=False, autoincrement=False, nullable=True)

    # 所属部门:
    ParentNode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)
    # 查询权限
    menus = relationship("Menu", secondary=Role_Menu)




# Role_END:

# Menu_START:
# 模块菜单表
class Menu(Base):
    __tablename__ = 'Menu'
    # 模块ID
    ID = Column(Integer, primary_key=True, autoincrement=True)

    # 模块名称
    ModuleName = Column(Unicode(32), nullable=False)

    # 模块编码
    ModuleCode = Column(String(100),nullable=False)

    # 模块路由
    Url = Column(String(100), nullable=True)

    # 描述
    Description = Column(Unicode(1024), nullable=True)

    # 创建时间
    CreateDate = Column(DateTime, default=datetime.now, nullable=True)

    # 创建人
    Creator = Column(Unicode(50), nullable=True)

    # 父节点
    ParentNode = Column(Integer, nullable=True)

    # 查询角色
    roles = relationship("Role", secondary=Role_Menu)

# Menu_END:

# WaterEnergy_END:

# 生成表单的执行语句_START
Base.metadata.create_all(engine)

# 生成表单的执行语句_END
