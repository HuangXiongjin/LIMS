import json
from datetime import datetime

from flask import Blueprint, request

# from system import User
from tools.handle import MyEncoder, log, get_short_id
from common.lims_models import db_session, ClassifyTree, QualityStandardCenter, QualityStandard

# from database.connect_db import conn
# from common.batch_plan_model import PlanManager

system_interface = Blueprint('system_interface', __name__)


@system_interface.route('/ClassifyTree', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def classify_tree():
    """分类树操作"""
    if request.method == 'GET':
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
            # parent_tag2 = set(item.ParentTag for item in query_data)
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
        return json.dumps({'code': '1000', 'msg': '成功', 'data': tree}, cls=MyEncoder, ensure_ascii=False)
    if request.method == 'POST':
        parent_name = request.values.get('ParentName')
        children_name = request.values.get('ChildrenName')
        code = datetime.now().strftime('%H%M%S%Y%m%d')
        db_session.add(ClassifyTree(TagCode=code, TagName=children_name, ChildrenTag=parent_name))
        db_session.commit()
        return json.dumps({'code': '1000', 'msg': '添加成功'}, cls=MyEncoder, ensure_ascii=False)
    if request.method == 'PATCH':
        code = request.values.get('Code')
        parent_name = request.values.get('ParentName')
        children_name = request.values.get('ChildrenName')
        new_type_name = "'" + request.values.get('ChildrenName') + "'"
        old_data = db_session.query(ClassifyTree).filter_by(TagCode=code).first()
        type_name = "'" + old_data.TagName + "'"
        sql = f'update QualityStandardCenter set Type={new_type_name} where Type={type_name}'
        db_session.execute(sql)
        data = db_session.query(ClassifyTree).filter_by(TagCode=code).first()
        data.TagName = children_name
        data.ChildrenTag = parent_name
        db_session.add(data)
        db_session.commit()
        return json.dumps({'code': '1000', 'msg': '修改成功'}, cls=MyEncoder, ensure_ascii=False)
    if request.method == 'DELETE':
        code = request.values.get('Code')
        children_name = "'" + request.values.get('ChildrenName') + "'"
        data = db_session.query(ClassifyTree).filter_by(TagCode=code).first()
        db_session.delete(data)
        db_session.commit()
        sql = f'delete from QualityStandardCenter where Type={children_name}'
        db_session.execute(sql)
        return json.dumps({'code': '1000', 'msg': '删除成功'}, cls=MyEncoder, ensure_ascii=False)


@system_interface.route('/QualityStandardCenter', methods=['GET', 'POST', 'DELETE'])
def product():
    """节点下品名的维护"""
    if request.method == 'GET':
        # 获取当前节点下的品名
        code = request.values.get('Code')
        tag = db_session.query(ClassifyTree).filter_by(TagCode=code).first()
        data = db_session.query(QualityStandardCenter).filter_by(Type=tag.TagName).all()
        return json.dumps({'code': '1000', 'msg': '成功', 'data': data}, cls=MyEncoder, ensure_ascii=False)
    if request.method == 'POST':
        # 当前节点下品名的增加-修改
        if request.values.get('Action') == 'add':
            data = QualityStandardCenter()
            data.No = get_short_id()
            data.Product = request.values.get('Product')
            data.Type = request.values.get('Type')
            data.Code = request.values.get('Code')
            data.Source = request.values.get('Source')
            data.Unit = request.values.get('Unit')
            data.IntoUser = request.values.get('IntoUser')
            data.IntoTime = request.values.get('IntoTime')
            db_session.add(data)
            db_session.commit()
        if request.values.get('Action') == 'update':
            no = request.values.get('No')
            data = db_session.query(QualityStandardCenter).filter_by(No=no).first()
            data.Product = request.values.get('Product')
            data.Type = request.values.get('Type')
            data.Code = request.values.get('Code')
            data.Source = request.values.get('Source')
            data.Unit = request.values.get('Unit')
            data.AlterTime = request.values.get('AlterTime')
            data.AlterUser = request.values.get('AlterUser')
            db_session.add(data)
            db_session.commit()
        return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)
    if request.method == 'DELETE':
        items = request.json.get('Id')
        for item in items:
            data = db_session.query(QualityStandardCenter).get(int(item))
            db_session.delete(data)
    return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)


# @system_interface.route('/QualityStandard', methods=['GET', 'POST'])
# def quality_standard():
#     """品名下质检的维护"""
#     if request.method == 'GET':
#         # 获取当前节点下的品名
#         no = request.values.get('No')
#         results = db_session.query(QualityStandard).filter_by(No=no).all()
#         return json.dumps({'code': '1000', 'msg': '成功', 'data': results}, cls=MyEncoder, ensure_ascii=False)
#     if request.method == 'POST':
#         # 当前品名下的质检维护
#         data = QualityStandard()
#         data.No = request.values.get('No')
#         data.Product = request.values.get('Product')
#         data.Project = request.values.get('Project')
#         data.Character = request.values.get('Character')
#         data.Discern = request.values.get('Discern')
#         data.Inspect = request.values.get('Inspect')
#         data.Content = request.values.get('Content')
#         data.Microbe = request.values.get('Microbe')
#         db_session.add(data)
#         db_session.commit()
#     if request.method == 'PATCH':
#         Id = request.values.get('Id')
#         data = db_session.query(QualityStandard).filter_by(Id=Id).first()
#         data.Product = request.values.get('Product')
#         data.Project = request.values.get('Project')
#         data.Character = request.values.get('Character')
#         data.Discern = request.values.get('Discern')
#         data.Inspect = request.values.get('Inspect')
#         data.Content = request.values.get('Content')
#         data.Microbe = request.values.get('Microbe')
#         if request.values.get('Action') == 'add':
#             data.No = get_short_id()
#             data.IntoUser = request.values.get('IntoUser')
#             data.IntoTime = request.values.get('IntoTime')
#         if request.values.get('Action') == 'update':
#             data.AlterTime = request.values.get('AlterTime')
#             data.AlterUser = request.values.get('AlterUser')
#         db_session.add(data)
#         db_session.commit()
#         return json.dumps({'code': '1000', 'msg': '添加成功'}, cls=MyEncoder, ensure_ascii=False)
#
