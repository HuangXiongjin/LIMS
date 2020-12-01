import json

import xlwt
from flask import Blueprint, make_response
from flask_login import current_user

from BSFramwork import AlchemyEncoder
from system import User
from tools.handle import MyEncoder, log
from common.lims_models import db_session, ClassifyTree
# from database.connect_db import conn
from common.batch_plan_model import PlanManager

system_interface = Blueprint('system_interface', __name__)


@system_interface.route('/ClassifyTree', methods=['GET'])
def classify_tree():
    """分类树形"""
    # factory = db_session.query(AreaMaintain).first()
    sql = "select ChildrenTag from ClassifyTree"
    parent_tags = db_session.execute(sql).fetchall()
    tags_list = set(str(item[0]) for item in parent_tags)
    children = []
    for item in tags_list:
        # 通过一级节点获取所有对应节点下的值
        children2 = []
        children1 = {"label": item, "children": children2}
        query_data = db_session.query(ClassifyTree).filter_by(ChildrenTag=item).all()
        parent_tag2 = set(item.ParentTag for item in query_data)
        for data in query_data:
            rank2_data = {"id": data.TagCode, "label": data.TagName, "ParentTagCode": "1"}
            children2.append(rank2_data)
        children.append(children1)
        # for result in parent_tag2:
        #     # children4 = []
        #     # 通过一级节点获取所有对应的二级节点
        #     if result:
        #         # 二级节点不为空
        #         children3 = []
        #         rank2_data = {"label": result, "children": children3}
        #         # children4.append(rank2_data)
        #         # last_data = db_session.query(Tags).filter_by(ParentTag=result).all()
        #         parent_tag_sql = 'select '
        #         # for data in last_data:
        #         #     # 循环获取最后节点的数据
        #         #
        #         #     rank3_data = {"id": data.TagCode, "label": data.TagName, "ParentTagCode": "1"}
        #         #     children3.append(rank3_data)
        #         # children2.append(rank2_data)
        #         # rank3 = {"label": result.ParentTag, "children": [{"id": result.TagCode, "label": result.TagName}]}
        #     else:
        #         for data in query_data:
        #             rank2_data = {"id": data.TagCode, "label": data.TagName, "ParentTagCode": "1"}
        #             children2.append(rank2_data)
        # children.append(children1)
    tree = [{"label": '希尔安药业', "children": children}]
    return json.dumps({'code': '20001', 'message': '成功', 'data': tree}, cls=AlchemyEncoder, ensure_ascii=False)
    pass