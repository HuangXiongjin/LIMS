import json
from datetime import datetime

from flask import Blueprint, request

from tools.handle import MyEncoder, log, get_short_id
from common.lims_models import db_session, ClassifyTree, QualityStandardCenter, QualityStandard

check = Blueprint('check', __name__)


@check.route('/CheckForm', methods=['GET'])
def check_form():
    """样品请检"""
    try:
        No = request.values.get('No')
        results = db_session.query(QualityStandard).filter_by(No=No).all()
        project = []
        character = []
        discern = []
        inspect = []
        content = []
        microbe = []
        data = [
            {'编号': No, '项目': project, '性状': character, '鉴别': discern, '检查': inspect, '含量测定': content, '微生物限度': microbe}]
        for result in results:
            if result.Project is not None:
                project.append(result.Project)
            if result.Character is not None:
                character.append(result.Character)
            if result.Discern is not None:
                discern.append(result.Discern)
            if result.Inspect is not None:
                inspect.append(result.Inspect)
            if result.Content is not None:
                content.append(result.Content)
            if result.Microbe is not None:
                microbe.append(result.Microbe)
        return json.dumps({'code': '1000', 'msg': '成功', 'data': data}, ensure_ascii=False)
    except Exception as e:
        log(e)
        return json.dumps({'code': '2000', 'msg': str(e)})
