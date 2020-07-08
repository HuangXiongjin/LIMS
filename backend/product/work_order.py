import datetime
import json

from flask import Blueprint, request

from backend import db
from backend.common.models import RepairPlan, LubricationPlan, Plan, RepairRecord, Record, FaultRepair, OrderVerify, \
    Task
from backend.tools.handle import MyEncoder, get_time_stamp

work_order = Blueprint('work_order', __name__)


@work_order.route('/input', methods=['GET', 'POST'])
def add_data():
    """工单等表录入数据"""
    json_data = request.get_json()
    if request.args.get('foo') == 'bjw_plan':
        data = RepairPlan(equipment_no=json_data.get('equipment_no'), plan_no=json_data.get('plan_no'),
                          position=json_data.get('position'), tools=json_data.get('tools'),
                          material=json_data.get('material'), plan=json_data.get('plan'),
                          standard=json_data.get('standard'), period=json_data.get('period'),
                          department=json_data.get('department'), type=json_data.get('type')
                          )
        db.session.add(data)
        db.session.commit()
    elif request.args.get('foo') == 'r_plan':
        data = LubricationPlan(equipment_no=json_data.get('equipment_no'), plan_no=json_data.get('plan_no'),
                               position=json_data.get('position'), oils=json_data.get('oils'),
                               way=json_data.get('way'), changes_amount=json_data.get('changes_amount'),
                               oils_changes_period=json_data.get('oils_changes_period'),
                               add_amount=json_data.get('add_amount'), oils_add_period=json_data.get('oils_add_period'),
                               department=json_data.get('department')
                               )
        db.session.add(data)
        db.session.commit()
    elif request.args.get('foo') == 'plan':
        data = Plan(equipment_no=json_data.get('equipment_no'), no=json_data.get('no'),
                    worker_no=json_data.get('worker_no'), name=json_data.get('name'),
                    no_status=json_data.get('no_status'), verify_status=json_data.get('verify_status'),
                    remind_status=json_data.get('remind_status'), work_time=json_data.get('work_time'),
                    found_time=json_data.get('found_time'), plan_no=json_data.get('plan_no'),
                    type=json_data.get('type')
                    )
        db.session.add(data)
        db.session.commit()
    elif request.args.get('foo') == 'repair_record':
        data = RepairRecord(equipment_no=json_data.get('equipment_no'),
                            no=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
                            worker_no=json_data.get('worker_no'), name=json_data.get('name'),
                            status=json_data.get('status'), fault_reason=json_data.get('fault_reason'),
                            repair_material=json_data.get('repair_material'), fault_rank=json_data.get('fault_rank'),
                            knowledge=json_data.get('knowledge'), time=json_data.get('time')
                            )
        data = RepairRecord(data)
        db.session.add(data)
        db.session.commit()
    elif request.args.get('foo') == 'brj_record':
        data = Record(equipment_no=json_data.get('equipment_no'),
                      no=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
                      worker_no=json_data.get('worker_no'), name=json_data.get('name'),
                      status=json_data.get('status'), type=json_data.get('type'), time=json_data.get('time')
                      )
        db.session.add(data)
        db.session.commit()
    elif request.args.get('foo') == 'fault_repair':
        # file = request.files.get('picture')
        # 检查文件类型
        # if file and not is_allowed_type(file.content_type):
        #     return json.dumps({'code': 100001, 'message': '文件类型错误'})
        # 生成文件名和文件路径
        # ext = file.filename.split('.')[-1]  # 文件后缀
        # filename = generate_filename()
        # full_filename = f'{filename}.{ext}'
        # file_path = get_root_path()
        # file.save(os.path.join(file_path, full_filename))
        data = FaultRepair(equipment_no=json_data.get('equipment_no'), workshop_no=json_data.get('workshop_no'),
                           no=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
                           worker_no=json_data.get('worker_no'), name=json_data.get('name'),
                           reason=json_data.get('reason'), picture='full_filename', time=json_data.get('time')
                           )
        db.session.add(data)
        db.session.commit()
        return 'this one'
    return 'this two'


@work_order.route('/verify', methods=['GET', 'POST'])
def verify():
    """工单审核"""
    if request.method == 'GET':
        plan = Plan.query.filter_by(verify_status='待审核').all()
        return json.dumps({'code': '1000', 'message': '请求成功', 'data': plan}, cls=MyEncoder, ensure_ascii=True)
    if request.method == 'POST':
        json_data = request.get_json()
        data = OrderVerify(no=json_data.get('no'), verify_status=json_data.get('verify_status'),
                           name='name', verify_time=json_data.get('verify_time'))
        db.session.add(data)
        db.session.commit()
        return json.dumps({'code': '1000', 'message': '操作成功'}, cls=MyEncoder, ensure_ascii=True)


@work_order.route('/plan', methods=['GET', 'POST'])
def plan():
    """任务表添加任务"""
    query_data = Plan.query.filter_by(verify_status='待处理').all()
    if request.method == 'GET':
        return json.dumps({'code': '1000', 'message': '操作成功', 'data': query_data}, cls=MyEncoder, ensure_ascii=True)
    elif request.method == 'POST':
        # query_list = [item if get_time_stamp(item.work_time) else '' for item in query_data]
        # query_list = []
        for item in query_data:
            if get_time_stamp(item.work_time):
                task = Task(no=item.no, equipment_no=item.equipment_no, workshop_no=item.workshop_no,
                            name=item.name, type=item.type, no_status=item.no_status, work_require='工作要求',
                            found_time='下发时间')
                db.session.add(task)
                db.session.commit()
                # query_list.append(item)
            else:
                pass
        return json.dumps({'code': '1000', 'message': '操作成功'}, cls=MyEncoder, ensure_ascii=True)


@work_order.route('/', methods=['GET'])
def index():
    return 'this work_order'
