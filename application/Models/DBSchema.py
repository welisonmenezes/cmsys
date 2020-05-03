from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from app import app

ma = Marshmallow(app)


class BlacklistSchema(ma.Schema):
    id = fields.Integer()
    type = fields.String()
    value = fields.String()
    target = fields.String()


class CapabilitySchema(ma.Schema):
    id = fields.Integer()
    description = fields.String()
    type = fields.String()
    target_id = fields.Integer()
    can_write = fields.Integer()
    can_read = fields.Integer()
    can_delete = fields.Integer()


class RoleSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    can_access_admin = fields.Integer()


class VariableSchema(ma.Schema):
    id = fields.Integer()
    key = fields.String()
    value = fields.String()