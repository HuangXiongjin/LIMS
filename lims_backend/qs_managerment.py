import json
from datetime import datetime, date, timedelta

from flask import Blueprint, request

from tools.handle import MyEncoder, get_uuid
from common.lims_models import db_session, ClassifyTree, QualityStandardCenter, QualityStandard, CheckForm, \
    CheckProject, CheckLife, Distribute, ReportVerify

qs_manager = Blueprint('qs_manager', __name__)


def get_week_day(data):
    """获取本周的开始和结尾"""
    week_day_dict = {
        0: 1,
        1: 2,
        2: 3,
        3: 4,
        4: 5,
        5: 6,
        6: 7,
    }
    day = data.weekday()
    today_date = week_day_dict[day]
    week_start = "'" + (date.today() - timedelta(days=(today_date - 1))).strftime('%Y-%m-%d') + " 00:00:00'"
    week_end = "'" + (date.today() + timedelta(days=(7 - today_date))).strftime('%Y-%m-%d') + " 23:59:59'"
    up_week_start = "'" + ((date.today() - timedelta(days=(today_date - 1))) - timedelta(7)).strftime(
        '%Y-%m-%d') + " 00:00:00'"
    up_week_end = "'" + ((date.today() + timedelta(days=(7 - today_date))) - timedelta(7)).strftime(
        '%Y-%m-%d') + " 23:59:59'"
    return week_start, week_end, up_week_start, up_week_end


def last_day_of_month(any_day):
    """
    获取获得一个月中的最后一天
    :param any_day: 任意日期
    :return: string
    """
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)


@qs_manager.route('/FinishSituation', methods=['GET'])
def finish_situation():
    """统计分析接口"""
    global yuanliao_number, yuanliao_number2, zhongjian_number, zhongjian_number2, chengpin_number, chengpin_number2
    product_type = request.values.get('ProductType')
    # 本周完成情况
    count_time = get_week_day(date.today())
    print(count_time)
    # 周时间
    week_start = count_time[0]
    week_end = count_time[1]
    last_week_start = count_time[2]
    last_week_end = count_time[3]
    # 月时间
    month_start = "'" + date.today().strftime('%Y-%m-01') + " 00:00:00'"
    res = last_day_of_month(date.today())
    month_end = "'" + res.strftime('%Y-%m-%d') + " 23:59:59'"

    # 年时间
    year_start = "'" + date.today().strftime('%Y-01-01') + " 00:00:00'"
    year_end = "'" + date.today().strftime('%Y-12-31') + " 23:59:59'"

    finish_number = db_session.query(CheckForm).filter(CheckForm.ProductType == product_type, CheckForm.Status == '报告',
                                                       CheckForm.CheckDate.between(week_start, week_end)).all()
    total_number = db_session.query(CheckForm).filter(CheckForm.ProductType == product_type,
                                                      CheckForm.CheckDate.between(week_start, week_end)).all()
    week_data = [{"finish": len(finish_number), 'total': len(total_number)}]

    # 质检量
    number = ''
    if request.values.get('NumberTime') == '周':
        number = db_session.query(CheckForm).filter(CheckForm.ProductType == product_type,
                                                    CheckForm.Status == '报告',
                                                    CheckForm.CheckDate.between(week_start, week_end)).all()

    if request.values.get('NumberTime') == '月':
        number = db_session.query(CheckForm).filter(CheckForm.ProductType == product_type,
                                                    CheckForm.Status == '报告',
                                                    CheckForm.CheckDate.between(month_start, month_end)).all()
    if request.values.get('NumberTime') == '年':
        number = db_session.query(CheckForm).filter(CheckForm.ProductType == product_type,
                                                    CheckForm.Status == '报告',
                                                    CheckForm.CheckDate.between(year_start, year_end)).all()

    # 排名环比
    if request.values.get('ContrastTime') == '周':
        # 原料
        yuanliao_number = db_session.query(CheckForm).filter(CheckForm.ProductType == '原料',
                                                             CheckForm.Status == '报告',
                                                             CheckForm.CheckDate.between(week_start, week_end)).all()
        yuanliao_number2 = db_session.query(CheckForm).filter(CheckForm.ProductType == '原料',
                                                              CheckForm.Status == '报告',
                                                              CheckForm.CheckDate.between(last_week_start,
                                                                                          last_week_end)).all()
        # 中间品
        zhongjian_number = db_session.query(CheckForm).filter(CheckForm.ProductType == '中间品',
                                                              CheckForm.Status == '报告',
                                                              CheckForm.CheckDate.between(week_start, week_end)).all()
        zhongjian_number2 = db_session.query(CheckForm).filter(CheckForm.ProductType == '中间品',
                                                               CheckForm.Status == '报告',
                                                               CheckForm.CheckDate.between(last_week_start,
                                                                                           last_week_end)).all()
        # 成品
        chengpin_number = db_session.query(CheckForm).filter(CheckForm.ProductType == '成品',
                                                             CheckForm.Status == '报告',
                                                             CheckForm.CheckDate.between(week_start, week_end)).all()
        chengpin_number2 = db_session.query(CheckForm).filter(CheckForm.ProductType == '中间品',
                                                              CheckForm.Status == '报告',
                                                              CheckForm.CheckDate.between(last_week_start,
                                                                                          last_week_end)).all()
    if request.values.get('ContrastTime') == '月':
        # 原料
        yuanliao_number = db_session.query(CheckForm).filter(CheckForm.ProductType == '原料',
                                                             CheckForm.Status == '报告',
                                                             CheckForm.CheckDate.between(week_start, week_end)).all()
        yuanliao_number2 = []
        # yuanliao_number2 = db_session.query(CheckForm).filter(CheckForm.ProductType == '原料',
        #                                                       CheckForm.Status == '报告',
        #                                                       CheckForm.CheckDate.between(last_week_start,
        #                                                                                   last_week_end))
        # 中间品
        zhongjian_number = db_session.query(CheckForm).filter(CheckForm.ProductType == '中间品',
                                                              CheckForm.Status == '报告',
                                                              CheckForm.CheckDate.between(week_start, week_end)).all()
        zhongjian_number2 = []
        # zhongjian_number2 = db_session.query(CheckForm).filter(CheckForm.ProductType == '中间品',
        #                                                        CheckForm.Status == '报告',
        #                                                        CheckForm.CheckDate.between(last_week_start,
        #                                                                                    last_week_end))
        # 成品
        chengpin_number = db_session.query(CheckForm).filter(CheckForm.ProductType == '成品',
                                                             CheckForm.Status == '报告',
                                                             CheckForm.CheckDate.between(week_start, week_end)).all()
        chengpin_number2 = []
        # chengpin_number2 = db_session.query(CheckForm).filter(CheckForm.ProductType == '中间品',
        #                                                       CheckForm.Status == '报告',
        #                                                       CheckForm.CheckDate.between(last_week_start,
        #                                                                                   last_week_end))
    if request.values.get('ContrastTime') == '年':
        # 原料
        yuanliao_number = db_session.query(CheckForm).filter(CheckForm.ProductType == '原料',
                                                             CheckForm.Status == '报告',
                                                             CheckForm.CheckDate.between(year_start, year_end)).all()
        yuanliao_number2 = []
        # yuanliao_number2 = db_session.query(CheckForm).filter(CheckForm.ProductType == '原料',
        #                                                       CheckForm.Status == '报告',
        #                                                       CheckForm.CheckDate.between(year_start,
        #                                                                                   year_end))
        # 中间品
        zhongjian_number = db_session.query(CheckForm).filter(CheckForm.ProductType == '中间品',
                                                              CheckForm.Status == '报告',
                                                              CheckForm.CheckDate.between(year_start, year_end)).all()
        zhongjian_number2 = []
        # zhongjian_number2 = db_session.query(CheckForm).filter(CheckForm.ProductType == '中间品',
        #                                                        CheckForm.Status == '报告',
        #                                                        CheckForm.CheckDate.between(year_start,
        #                                                                                    year_end))
        # 成品
        chengpin_number2 = []
        chengpin_number = db_session.query(CheckForm).filter(CheckForm.ProductType == '成品',
                                                             CheckForm.Status == '报告',
                                                             CheckForm.CheckDate.between(year_start, year_end)).all()
        # chengpin_number2 = db_session.query(CheckForm).filter(CheckForm.ProductType == '中间品',
        #                                                       CheckForm.Status == '报告',
        #                                                       CheckForm.CheckDate.between(year_start,
        #                                                                                   year_end))
    contrast_data = [{"yuanliao": {"now_number": len(yuanliao_number), "up_number": len(yuanliao_number2)}},
                     {"zhongjian_number": {"now_number": len(zhongjian_number), "up_number": len(zhongjian_number2)}},
                     {"chengpin_number": {"now_number": len(chengpin_number), "up_number": len(chengpin_number2)}},
                     {"tuihuo_number": {"now_number": 0, "up_number": 0}}]

    data = [{'week_data': week_data, 'account_data': len(number), 'contrast_data': contrast_data}]
    return json.dumps({'code': '1000', 'msg': '成功', 'data': data}, cls=MyEncoder, ensure_ascii=False)
