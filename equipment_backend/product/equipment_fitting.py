import datetime
import json
import time

from flask import Blueprint, request

from common.system import db_session, User
from common.BSFramwork import AlchemyEncoder
from equipment_backend import db
from common.equipment_models import Fitting, EquipmentBaseData, InstructionsCenter, Instructions, FittingInto, FittingOut
from equipment_backend.tools.handle import MyEncoder

equipment = Blueprint('equipment', __name__)


@equipment.route('/', methods=['GET'])
def index():
    user = db_session.query(User).all()
    equipments = EquipmentBaseData.query.all()
    return json.dumps({'equipments': equipments, 'user': user}, cls=MyEncoder, ensure_ascii=False)


@equipment.route('/input', methods=['GET', 'POST'])
def add_data():
    """设备配件说明书数据录入"""
    if request.values.get('foo') == 'equipment':
        result = request.get_json()
        # file = request.files.get('instruction')
        # 检查文件类型
        # if not is_allowed_type(file.content_type):
        #     return json.dumps({'code': 100001, 'message': '文件类型错误'})
        equipment_data = EquipmentBaseData(workshop_no=result.get('workshop_no'), equipment_no=result.get('equipment_no'),
                                   name=result.get('name'), model=result.get('model'), type=result.get('type'),
                                   manufacturer=result.get('manufacturer'), sap=result.get('sap'),
                                   fixed_assets_no=result.get('fixed_assets_no'),
                                   fixed_assets_name=result.get('fixed_assets_name'),
                                   status=result.get('status'), area=result.get('area'),
                                   into_time=result.get('into_time')
                                   )
        center_table = InstructionsCenter(no=result.get('equipment_no'))
        db.session.add_all([equipment_data, center_table])
        db.session.commit()
        # 生成文件名和文件路径
        # ext = file.filename.split('.')[-1]  # 文件后缀
        # filename = generate_filename()
        # full_filename = f'{filename}.{ext}'
        # 绑定中间表id
        item = InstructionsCenter.query.filter_by(no=result.get('equipment_no')).first()
        instruction = Instructions(no='filename', type='设备', detail='full_filename', center_id=item.id)
        db.session.add(instruction)
        db.session.commit()
        # file_path = get_root_path()
        # file.save(os.path.join(file_path, full_filename))
        return "this equipment page"
    elif request.values.get('foo') == 'fitting':
        result = request.get_json()
        # file = request.files.get('instruction')
        # 检查文件类型
        # if not is_allowed_type(file.content_type):
        #     return json.dumps({'code': 100001, 'message': '文件类型错误'})
        fitting_data = Fitting(fitting_no=result.get('fitting_no'), equipment_no=result.get('equipment_no'),
                               name=result.get('name'), model=result.get('model'), type=result.get('type'),
                               manufacturer=result.get('manufacturer'), time=result.get('into_time')
                               )
        center_table = InstructionsCenter(no=result.get('fitting_no'))
        db.session.add_all([fitting_data, center_table])
        db.session.commit()
        # 生成文件名和文件路径
        # ext = file.filename.split('.')[-1]  # 文件后缀
        # filename = generate_filename()
        # full_filename = f'{filename}.{ext}'
        # 绑定中间表id
        item = InstructionsCenter.query.filter_by(no=result.get('fitting_no')).first()
        instruction = Instructions(no='filename', type='配件', detail='full_filename', center_id=item.id)
        db.session.add(instruction)
        db.session.commit()
        # file_path = get_root_path()
        # file.save(os.path.join(file_path, full_filename))
        return "this fitting page"
    else:
        return "未知错误"


@equipment.route('/stock', methods=['GET', 'POST'])
def stock():
    """库存统计"""
    query_data = Fitting.query.filter_by(status='未使用').all()
    model_data = set(item.model for item in query_data)
    print(model_data)
    data = []
    for item in model_data:
        query = Fitting.query.filter_by(status='未使用').filter_by(model=item).all()
        result = {'fitting': query, 'count': len(query)}
        data.append(result)
    return json.dumps({'code': '10000', 'message': '请求成功', 'data': data}, cls=MyEncoder, ensure_ascii=False)


@equipment.route('/fitting', methods=['GET', 'POST'])
def fitting_into_out():
    """配件出入库单"""
    if request.values.get('foo') == 'into':
        json_data = request.get_json()
        fitting_into = FittingInto(no=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
                                   fitting_no=json_data.get('fitting_no'),
                                   fitting_number=json_data.get('fitting_number'), status=json_data.get('status'),
                                   worker=json_data.get('worker'), time=json_data.get('time'))
        db.session.add(fitting_into)
        db.session.commit()
    if request.values.get('foo') == 'out':
        json_data = request.get_json()
        fitting_into = FittingOut(no=str(round(time.time() * 1000)), fitting_no=json_data.get('fitting_no'),
                                  fitting_number=json_data.get('fitting_number'),
                                  out_worker=json_data.get('out_worker'),
                                  use_worker=json_data.get('use_worker'), time=json_data.get('time'))
        db.session.add(fitting_into)
        db.session.commit()
    return json.dumps({'code': '10000', 'message': '操作成功'})
