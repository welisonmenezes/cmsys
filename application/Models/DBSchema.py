from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from app import app

ma = Marshmallow(app)

class VariableSchema(ma.Schema):
    id = fields.Integer()
    key = fields.String()
    value = fields.String()


class BlacklistSchema(ma.Schema):
    id = fields.Integer()
    type = fields.String()
    value = fields.String()
    target = fields.String()