import json
from io import BytesIO

import pymssql
import xlwt
from flask import Blueprint, make_response
from flask_login import current_user

from BSFramwork import AlchemyEncoder
from system import User
from tools.handle import MyEncoder, log
from common.lims_models import db_session
# from database.connect_db import conn
from common.batch_plan_model import PlanManager

t1 = Blueprint('t123', __name__)


@t1.route('/index', methods=['GET'])
def index1():
    try:
        data = [{'原提取车间': ['蒸气表']}, {'前处理车间': ['蒸气表']}, {'提取二车间': ['灭菌柜蒸气表', '喷雾车间蒸气表',
                                                                   '管式灭菌蒸气表', '单号提取罐蒸气表', '双号提取罐蒸气表', '单/双效浓缩蒸气表']},
                {'综合车间': ['120带干蒸汽表',
                          '单号提取蒸汽表', '双号提取蒸气表', '双效浓缩蒸汽表', '二次浓缩（刮板浓缩）蒸汽表', '醇提车间（醇提+浓缩）蒸汽表',
                          '流化床制粒蒸汽表	']}, {'固体制剂车间': ['蒸气表']}, {'办公楼\食堂': ['蒸气表']}, {'GMP车间': ['蒸气表']}]
        # data = db_session.query(PlanManager).all()
        return json.dumps({'code': '200', 'msg': '接收成功', 'data': data}, cls=MyEncoder, ensure_ascii=False)
    except Exception as e:
        log(e, 'current_user.Name')

#
# @t1.route('/export', methods=['GET'])
# def export_excel():
#     # 方式一：游标语句查询
#     conn = pymssql.connect(user='sa', host='192.168.7.100', port='1433', password='xea@123', charset='utf8')
#     cur = conn.cursor()  # 获取游标
#     sql = 'select Name, session_id from LIMS.dbo.[User]'
#     cur.execute(sql)  # 游标查询
#     data1 = cur.fetchall()
#     print(data1)
#
#     # # 方式二：Session查询
#     data2 = db_session.execute(sql).fetchall()  # Session查询
#     print(data2)
#     #
#     # # 方式三：ORM查询
#     # data3 = db_session.query(User).all()
#     # print(data3)
#     return json.dumps({'data': data2}, cls=AlchemyEncoder, ensure_ascii=False)
    #
    # fields = ['姓名', '验证码']  # 设置自己需要的Excel表头
    #
    # book = xlwt.Workbook(encoding='utf-8')   # 获取excel对象
    #
    # sheet = book.add_sheet('用户信息')  # 设置excel的sheet名称
    #
    # for col, field in enumerate(fields):  # 写入excel表头
    #     sheet.write(0, col, field)
    #
    # row = 1
    # for data in data3:  # 根据数据写入excel，col-单元格行标，field-单元格列标
    #     for col, field in enumerate(data):
    #         sheet.write(row, col, field)
    #     row += 1
    #
    # # 使用BytesIO将数据转为字节串在发送给浏览器
    # sio = BytesIO()
    # book.save(sio)  # 将数据存储为bytes
    # sio.seek(0)
    # response = make_response(sio.getvalue())
    # response.headers['Content-type'] = 'application/vnd.ms-excel'  # 响应头告诉浏览器发送的文件类型为excel
    # response.headers['Content-Disposition'] = 'attachment; filename=data.xlsx'  # 浏览器打开/保存的对话框，data.xlsx-设定的文件名
    # return response
