import json

from flask import Blueprint, request
from sqlalchemy import MetaData, Table, Column
from sqlalchemy.ext.automap import automap_base

from common.lims_models import engine, db_session
from tools.MyEncode import MyEncoder
from tools.handle import log

metadata = MetaData()
Base = automap_base()
Base.prepare(engine, reflect=True)

crud_interface = Blueprint('crud', __name__)


@crud_interface.route('/CRUD', methods=['GET', 'POST', 'DELETE', 'UPDATE'])
def operation():
    try:
        if request.method == 'GET':
            # 当前页码
            # page = int(request.values.get('Page') if request.values.get('Page') is not None else '1')
            # # 每页记录数
            # per_page = int(request.values.get('PerPage') if request.values.get('PerPage') is not None else '100')
            # # 开始时间
            # start_time = "'" + request.values.get('StartTime') + "'"
            # end_time = "'" + request.values.get('EndTime') + "'"
            # # 字符串转表名
            # table_name = Table(request.values.get('TableName'), metadata, autoload=True, autoload_with=engine)
            # column_name = Table(request.values.get('TableName'), metadata, autoload=True, autoload_with=engine)
            # # 精确查询
            # if request.values.get('Query') == 'accurate':
            #
            #     # 是否存在分页查询
            #     if page is None or per_page is None:
            #
            #         query_data = db_session.query(table_name).filter_by().all()
            #         results = [dict(zip(item.keys(), item)) for item in query_data]
            #         print(results)
            #     else:
            #         pass
            # # 模糊查询
            # if request.values.get('Query') == 'Vague':
            #
            #     pass
            # # 当前页码
            # page = int(request.values.get('Page'))
            # # 每页记录数
            # per_page = int(request.values.get('PerPage'))
            # table_name = request.values.get('TableName')
            # # obj = Base.classes.get(table_name)
            # newTable = Table(table_name, metadata, autoload=True, autoload_with=engine)
            # newTable_data = db_session.query(newTable).filter_by().all()
            # # obj_data = db_session.query(obj).filter_by().all()
            # results = [dict(zip(item.keys(), item)) for item in newTable_data]
            # print(results)
            # return json.dumps({'code': '1000', 'msg': '成功', 'data': results, 'total': 'len(results)'}, cls=MyEncoder,
            #                   ensure_ascii=False)
            # sql = f"select * from {table_name} order by Id offset {(page - 1) * per_page} rows fetch next {page * per_page} rows only"
            # results = db_session.execute(sql).fetchall()
            # data = [dict(zip(result.keys(), result)) for result in results]
            # # pass
            # print(data)
            # return json.dumps({'code': '1000', 'msg': '成功', 'data': data, 'total': 'len(results)'}, cls=MyEncoder,
            #                   ensure_ascii=False)
            # return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder)
            pass
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)}, cls=MyEncoder)
