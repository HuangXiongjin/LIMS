from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from backend import db
from backend.common.models import Users


class UserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Users
        sql_session = db.session
        # dump_only表示id字段是只读字段(只允许从Model序列化为字典，不允许反序列)
        id = fields.Integer()
        username = fields.String()
        fullname = fields.String()
        # # load_only表示密码字段只能写入，不能读取
        password = fields.String()
        status = fields.String()
        created_time = fields.String()
