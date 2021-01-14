# class Equipment(Base):
#     __tablename__ = "Equipment"
#     # ID:
#     ID = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
#     # 设备名称
#     EquipmentName = Column(Unicode(128), nullable=True)
#     # 设备编号
#     EquipmentCode = Column(Unicode(128), nullable=True)
#     # 资产编号
#     AssetCode = Column(Unicode(128), nullable=True)
#     # 出厂编号
#     LeaveFactoryCode = Column(Unicode(128), nullable=True)
#     # 电子标签码
#     ElectronicCode = Column(Unicode(128), nullable=True)
#     # 设备类别
#     EquipmentType = Column(Unicode(64), nullable=True)
#     # 品牌
#     Brand = Column(Unicode(64), nullable=True)
#     # 规格
#     Specs = Column(Unicode(64), nullable=True)
#     # 单位
#     Unit = Column(Unicode(32), nullable=True)
#     # 设备来源
#     Source = Column(Unicode(128), nullable=True)
#     # 供应商
#     Manufacturer = Column(Unicode(128), nullable=True)
#     # 设备状态（运行中，维修中）
#     Status = Column(Unicode(128), default="运行中", nullable=True)
#     # 购置时间
#     PurchaseTime = Column(Unicode(128), nullable=True, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#     # 购置金额
#     PurchaseMoney = Column(Unicode(64), nullable=True)
#     # 保修期
#     WarrantyTime = Column(Unicode(128), nullable=True, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#     # 投产时间
#     UseTime = Column(Unicode(128), nullable=True, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#     # 预计报废时间
#     ScrapTime = Column(Unicode(128), nullable=True, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#     # 设备等级
#     Grade = Column(Unicode(64), nullable=True)
#     # 负责人
#     Director = Column(Unicode(64), nullable=True)
#     # 所属部门
#     Department = Column(Unicode(128), nullable=True)
#     # 放置位置
#     Position = Column(Unicode(128), nullable=True)
#     # 是否计量设备
#     IsCalculate = Column(Unicode(32), nullable=True)
#     # 是否折旧设备
#     IsDepreciation = Column(Unicode(32), nullable=True)
#     # 当前净值
#     NetValue = Column(Unicode(64), nullable=True)
#     # 是否折旧设备
#     TechnicalParameter = Column(Unicode(128), nullable=True)
#     # 备注
#     Comment = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)
