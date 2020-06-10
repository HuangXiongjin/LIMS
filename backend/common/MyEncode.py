import datetime
import decimal
import json
import types

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.collections import InstrumentedList


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data, ensure_ascii=False)
                    fields[field] = data
                except TypeError:  # 添加了对datetime的处理
                    if isinstance(data, InstrumentedList):
                        fields[field] = ''
                    elif isinstance(data, types.MethodType):
                        pass
                    elif isinstance(data, datetime.datetime):
                        fields[field] = data.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    elif isinstance(data, datetime.date):
                        fields[field] = data.strftime("%Y-%m-%d")
                    elif isinstance(data, decimal.Decimal):
                        fields[field] = float(data)
                    else:
                        pass
            return fields
        return json.JSONEncoder.default(self, obj)
