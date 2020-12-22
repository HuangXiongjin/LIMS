import json

from flask import Blueprint, request
from sqlalchemy import MetaData, Table
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
            page = int(request.values.get('Page'))
            # 每页记录数
            per_page = int(request.values.get('PerPage'))
            table_name = request.values.get('TableName')
            obj = Base.classes.get(table_name)
            newTable = Table(table_name, metadata, autoload=True, autoload_with=engine)
            data = db_session.query(obj).all()
            print(data)
            sql = f"select * from {table_name} order by Id offset {(page - 1) * per_page} rows fetch next {page * per_page} rows only"
            results = db_session.execute(sql).fetchall()
            data = [dict(zip(result.keys(), result)) for result in results]
            # pass
            print(data)
            return json.dumps({'code': '1000', 'msg': '成功', 'data': data, 'total': 'len(results)'}, cls=MyEncoder,
                              ensure_ascii=False)
            return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder)
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)}, cls=MyEncoder)
