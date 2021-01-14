import json
import os
from datetime import datetime

from flask import Blueprint, request, current_app, send_from_directory

from tools.handle import MyEncoder, log, get_short_id, generate_filename, get_root_path
from common.lims_models import db_session, ClassifyTree, QualityStandardCenter, WordForm, QualityStandard

system_interface = Blueprint('system_interface', __name__)


@system_interface.route('/ClassifyTree', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def classify_tree():
    """分类树操作"""
    if request.method == 'GET':
        # factory = db_session.query(AreaMaintain).first()
        sql = "select ID,ChildrenTag from ClassifyTree"
        parent_tags = db_session.execute(sql).fetchall()
        tags_list = set(item[1] for item in parent_tags)
        children = []
        i = 1
        for item in tags_list:
            # 通过一级节点获取所有对应节点下的值
            children2 = []
            children1 = {"id": i, "label": item, "children": children2}
            query_data = db_session.query(ClassifyTree).filter_by(ChildrenTag=item).all()
            # parent_tag2 = set(item.ParentTag for item in query_data)
            i += 1
            for data in query_data:
                rank2_data = {"id": data.TagCode, "label": data.TagName, "ParentTagCode": "1"}
                children2.append(rank2_data)
            children.append(children1)
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
        # 当前页码
        page = int(request.values.get('Page'))
        # 每页记录数
        per_page = int(request.values.get('PerPage'))
        tag = db_session.query(ClassifyTree).filter_by(TagCode=code).first()
        results = db_session.query(QualityStandardCenter).order_by(QualityStandardCenter.ID.asc()).filter_by(
            Type=tag.TagName).all()
        data = results[(page - 1) * per_page:page * per_page]
        return json.dumps({'code': '1000', 'msg': '成功', 'data': data, 'total': len(results)}, cls=MyEncoder,
                          ensure_ascii=False)
    data = ''
    if request.method == 'POST':
        # 当前节点下品名的增加-修改
        if request.values.get('Action') == 'add':
            data = QualityStandardCenter()
            data.No = get_short_id()
        #     data.Product = request.values.get('Product')
        #     data.Type = request.values.get('Type')
        #     data.Code = request.values.get('Code')
        #     data.Source = request.values.get('Source')
        #     data.Project = request.values.get('Project')
        #     data.Unit = request.values.get('Unit')
        #     data.IntoUser = request.values.get('IntoUser')
        #     data.IntoTime = request.values.get('IntoTime')
        #     db_session.add(data)
        #     db_session.commit()
        if request.values.get('Action') == 'update':
            No = request.values.get('No')
            data = db_session.query(QualityStandardCenter).filter_by(No=No).first()
        data.Product = request.values.get('Product')
        data.Type = request.values.get('Type')
        data.Code = request.values.get('Code')
        data.Source = request.values.get('Source')
        data.Project = request.values.get('Project')
        data.Unit = request.values.get('Unit')
        data.IntoUser = request.values.get('IntoUser')
        data.IntoTime = request.values.get('IntoTime')
        data.AlterTime = request.values.get('AlterTime')
        data.AlterUser = request.values.get('AlterUser')
        db_session.add(data)
        db_session.commit()
        return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)
    if request.method == 'DELETE':
        items = request.json.get('Id')
        for item in items:
            data = db_session.query(QualityStandardCenter).get(int(item))
            quality_standard = db_session.query(QualityStandard).filter_by(No=data.No).all()
            for i in quality_standard:
                db_session.delete(i)
                db_session.commit()
            db_session.delete(data)
            db_session.commit()
    return json.dumps({'code': '1000', 'msg': '操作成功'}, cls=MyEncoder, ensure_ascii=False)


@system_interface.route('/QualityStandard', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def quality_standard():
    """品名下质检的维护"""
    if request.method == 'GET':
        # 获取当前节点下的品名
        No = request.values.get('No')
        # q = request.values.get('TableName')
        # result = f'select * from {q} where No={No}'
        # dara = db_session.execute(result).fetchall()
        qs_center = db_session.query(QualityStandardCenter).filter_by(No=No).first()
        character = []
        discern = []
        inspect = []
        content = []
        microbe = []
        data = [
            {'No': No, 'Project': qs_center.Project, 'Source': qs_center.Source, 'Character': character,
             'Discern': discern, 'Inspect': inspect, 'Content': content, 'Microbe': microbe}]
        character_data = db_session.query(QualityStandard).filter_by(Product=qs_center.Product,
                                                                     Type='Character').all()
        for result in character_data:
            character.append({'ID': result.ID, 'value': result.Describe})
        discern_data = db_session.query(QualityStandard).filter_by(Product=qs_center.Product, Type='Discern').all()
        for result in discern_data:
            discern.append({'ID': result.ID, 'value': result.Describe})
        inspect_data = db_session.query(QualityStandard).filter_by(Product=qs_center.Product, Type='Inspect').all()
        for result in inspect_data:
            inspect.append({'ID': result.ID, 'value': result.Describe})
        content_data = db_session.query(QualityStandard).filter_by(Product=qs_center.Product, Type='Content').all()
        for result in content_data:
            content.append({'ID': result.ID, 'value': result.Describe})
        microbe_data = db_session.query(QualityStandard).filter_by(Product=qs_center.Product, Type='Microbe').all()
        for result in microbe_data:
            microbe.append({'ID': result.ID, 'value': result.Describe})
        return json.dumps({'code': '1000', 'msg': '成功', 'data': data}, cls=MyEncoder, ensure_ascii=False)
    if request.method == 'POST':
        # 当前品名下的质检维护
        No = request.values.get('No')
        Product = request.values.get('Product')
        data = request.values.get('Data')
        Type = request.values.get('Type')
        db_session.add(QualityStandard(No=No, Product=Product, Describe=data, Type=Type))
        db_session.commit()
        return json.dumps({'code': '1000', 'msg': '添加成功'}, cls=MyEncoder, ensure_ascii=False)
    if request.method == 'PATCH':
        ID = request.values.get('ID')
        data = db_session.query(QualityStandard).filter_by(ID=ID).first()
        data.Describe = request.values.get('Data')
        db_session.add(data)
        db_session.commit()
        return json.dumps({'code': '1000', 'msg': '修改成功'}, cls=MyEncoder, ensure_ascii=False)
    if request.method == 'DELETE':
        ID = request.values.get('ID')
        data = db_session.query(QualityStandard).filter_by(ID=ID).first()
        db_session.delete(data)
        db_session.commit()
        return json.dumps({'code': '1000', 'msg': '删除成功'}, cls=MyEncoder, ensure_ascii=False)


@system_interface.route('/Tree', methods=['GET'])
def tree():
    """请验分类树"""
    if request.method == 'GET':
        sql = "select ChildrenTag from ClassifyTree"
        parent_tags = db_session.execute(sql).fetchall()
        # 获取一级节点的名称
        tags_list = set(str(item[0]) for item in parent_tags)
        children = []
        for item in tags_list:
            # 通过一级节点获取所有对应二级子节点下的名称
            tree2_children2 = []
            tree1_children1 = {"label": item, "children": tree2_children2}
            query_data = db_session.query(ClassifyTree).filter_by(ChildrenTag=item).all()
            parent_tag2 = [(item.TagCode, item.TagName) for item in query_data]
            for data in parent_tag2:
                tree3_data = db_session.query(QualityStandardCenter).filter_by(Type=data[1]).all()
                tree3_set_data = [(item.No, item.Product) for item in tree3_data]
                tree3 = [{"id": i[0], "label": i[1]} for i in tree3_set_data]
                rank2_data = {"id": data[0], "label": data[1], "children": tree3}
                tree2_children2.append(rank2_data)
            children.append(tree1_children1)
        return json.dumps({'code': '1000', 'msg': '成功', 'data': children}, cls=MyEncoder, ensure_ascii=False)


@system_interface.route('/Upload', methods=['POST'])
def upload_file():
    """上传质检文档"""
    file = request.files.get('file')
    product_name = request.values.get('Product')
    filename = file.filename
    print(product_name)
    print(file.content_type)
    # 生成文件名和文件路径
    # ext = file.filename.split('.')[-1]
    # filename = generate_filename()
    # user = Users.query.get(user_id)
    # full_filename = filename + '.' + ext
    root_path = get_root_path()
    file_path = os.path.join(root_path, file.filename)
    db_session.add(WordForm(FileName=filename, Product=product_name, FilePath=file_path))
    db_session.commit()
    # filepath = current_app.config['UPLOAD_PATH']
    # 保存
    file.save(os.path.join(root_path, file.filename))
    return json.dumps({'code': '1000', 'msg': '上传成功'}, cls=MyEncoder, ensure_ascii=False)


@system_interface.route('/GetFile', methods=['GET', 'DELETE'])
def get_file():
    if request.method == 'GET':
        product_name = request.values.get('Product')
        # pic_path = '%s.%s' % (filename.split('.')[0], filename.split('.')[-1])
        print(product_name)
        # root_path = get_root_path()
        # filepath = os.path.join(root_path, current_app.config['UPLOAD_PATH'])
        # print(root_path)
        data = db_session.query(WordForm).filter_by(Product=product_name).all()
        return json.dumps({'code': '1000', 'msg': '请求成功', 'data': data}, cls=MyEncoder, ensure_ascii=False)
        # return send_from_directory(root_path, pic_path)
    if request.method == 'DELETE':
        no = request.values.get('ID')
        data = db_session.query(WordForm).filter_by(ID=no).first()
        db_session.delete(data)
        db_session.commit()
        return json.dumps({'code': '1000', 'msg': '删除成功'}, cls=MyEncoder, ensure_ascii=False)
