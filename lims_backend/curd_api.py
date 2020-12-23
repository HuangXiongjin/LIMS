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
    global sql
    try:
        if request.method == 'GET':
            # 当前页码
            page = int(request.values.get('Page') if request.values.get('Page') is not None else '1')
            # 每页记录数
            per_page = int(request.values.get('PerPage') if request.values.get('PerPage') is not None else '100')
            # 查询时间
            start_time = request.values.get('StartTime')
            end_time = request.values.get('EndTime')
            # 查询参数1
            query_column_value1 = request.values.get('QueryColumnValue')
            query_column_name1 = request.values.get('QueryColumnName')
            # 查询参数2
            query_column_value2 = request.values.get('QueryColumnValue2')
            query_column_name2 = request.values.get('QueryColumnName2')
            # 表名
            time_column_name = request.values.get('TimeColumn')
            table_name = Table(request.values.get('TableName'), metadata, autoload=True, autoload_with=engine)
            # 精确查询
            if request.values.get('Query') == 'Accurate':
                column1 = table_name.columns._data[query_column_name1]
                if time_column_name is not None:
                    time_column = table_name.columns._data[time_column_name]
                    if query_column_name2 is not None:
                        column2 = table_name.columns._data[query_column_name2]
                        sql = f"select * from {table_name} where {column1}='{query_column_value1}' and {column2}='{query_column_value2}' and {time_column} between '{start_time}' and '{end_time}' order by Id desc offset {(page - 1) * per_page} rows fetch next {page * per_page} rows only "
                    else:
                        sql = f"select * from {table_name} where {column1}='{query_column_value1}' and {time_column} between '{start_time}' and '{end_time}' order by Id desc offset {(page - 1) * per_page} rows fetch next {page * per_page} rows only "
                else:
                    sql = f"select * from {table_name} where {column1}='{query_column_value1}' order by Id desc offset {(page - 1) * per_page} rows fetch next {page * per_page} rows only "
                query_data = db_session.execute(sql).fetchall()
                results = [dict(zip(item.keys(), item)) for item in query_data]
                return json.dumps({'code': '1000', 'msg': '成功', 'data': results, 'total': len(results)}, cls=MyEncoder,
                                  ensure_ascii=False)
            else:
                query_data = db_session.query(table_name).order_by(table_name.columns._data['Id'].desc()).all()
                results = [dict(zip(item.keys(), item)) for item in query_data]
                data = results[(page - 1) * per_page:page * per_page]
                return json.dumps({'code': '1000', 'msg': '成功', 'data': data, 'total': len(results)}, cls=MyEncoder,
                                  ensure_ascii=False)
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)}, cls=MyEncoder)
