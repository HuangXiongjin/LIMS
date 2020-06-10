from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from backend import db
from backend.common.models import Users


class UserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Users
        sql_session = db.session
    id = fields.Integer()
    name = fields.String()
    number = fields.String()
    phone = fields.String()
    address = fields.String()
