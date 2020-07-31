from flask import Blueprint, render_template, request
import json
from flask_login import current_user, LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.BSFramwork import AlchemyEncoder
from common.system import Organization, Factory, DepartmentManager, Role, plantCalendarScheduling, ShiftsClass
from system_backend.SystemManagement.user_management import user_manage

from database.connect_db import CONNECT_DATABASE
login_manager = LoginManager()
# 创建对象的基类
engine = create_engine(CONNECT_DATABASE)
Session = sessionmaker(bind=engine)
db_session = Session()
cale = Blueprint('calender', __name__, template_folder='templates')

@cale.route('/plantcalender')
def plantcalender():
    return render_template('./calender.html')

@cale.route('/paiban')
def paiban():
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            StartClass = data.get("StartClass")
            Month = data.get("Month")
            sfs = db_session.query(ShiftsClass).filter().order_by(("ShiftsClassNum")).all()
            sum = None
            new_list = ""
            for sf in sfs:
                if sf.ShiftsClassName == StartClass:
                    sum = None if sf.ShiftsClassNum is None else float(sf.ShiftsClassNum)
            if sum:
                for i in sfs:
                    if (0 if sf.ShiftsClassNum is None else float(sf.ShiftsClassNum)) >= sum:
                        if i == 1:
                            new_list = i.ShiftsClassName
                        else:
                            new_list = new_list + "," + i.ShiftsClassName
                for i in sfs:
                    if (0 if sf.ShiftsClassNum is None else float(sf.ShiftsClassNum)) < sum:
                        new_list = new_list + "," + i.ShiftsClassName
            re_date = getMonthFirstDayAndLastDay(Month[0:4], int(Month[5:7]))
            for t in range(1, int(re_date[1][8:10])):
                rest = db_session.query(plantCalendarScheduling).filter(plantCalendarScheduling.start == Month + "-" + addzero(t),
                                                                        plantCalendarScheduling.title == "休息")
                if rest:
                    continue
                if t == 1:
                    pcs = plantCalendarScheduling()
                    pcs.color = "#FFA500"
                    pcs.title = new_list
                    pcs.start = Month + "-" + addzero(t)
                    pcs.end = ""
                    db_session.commit()
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            insertSyslog("error", "日历排班报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
