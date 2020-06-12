
#AA_START:
class AA(Base):
	__tablename__ = "AA" 
	
	#ID:
	ID = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
	
	#123:
	bb = Column(Unicode(32), primary_key = 否, autoincrement = 是, nullable = 是)
	
	#123:
	aa = Column(Unicode(32), primary_key = 否, autoincrement = 否, nullable = 否)
	
#AA_END:

# 生成表单的执行语句_START
Base.metadata.create_all(engine)

# 生成表单的执行语句_END
