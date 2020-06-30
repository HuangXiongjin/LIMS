from flask import Blueprint, request

from backend import db
from backend.common.models import RepairPlan, LubricationPlan, Plan

work_order = Blueprint('work_order', __name__)


@work_order.route('/input', methods=['GET', 'POST'])
def add_data():
    json_data = request.get_json()
    if request.args.get('foo') == 'bjw':
        data = RepairPlan(equipment_no=json_data.get('equipment_no'), plan_no=json_data.get('plan_no'),
                          position=json_data.get('position'), tools=json_data.get('tools'),
                          material=json_data.get('material'), plan=json_data.get('plan'),
                          standard=json_data.get('standard'), period=json_data.get('period'),
                          department=json_data.get('department'), type=json_data.get('type')
                          )
        db.session.add(data)
        db.session.commit()
    elif request.args.get('foo') == 'r':
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
        return 'this one'
    return 'this two'


@work_order.route('/', methods=['GET'])
def index():
    return 'this work_order'
