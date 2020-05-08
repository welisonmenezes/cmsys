from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from app import app

ma = Marshmallow(app)


class BlacklistSchema(ma.Schema):
    class Meta:
        fields = ('id', 'type', 'value', 'target')


class CapabilitySchema(ma.Schema):
    roles = fields.Nested('RoleSchema', many=True, exclude=('capabilities',))
    class Meta:
        fields = ('id', 'description', 'type', 'target_id', 'can_write', 'can_write', 'can_read', 'can_delete', 'roles')


class MediaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'type', 'origin', 'created', 'user_id')


class RoleSchema(ma.Schema):
    capabilities = fields.Nested('CapabilitySchema', many=True, exclude=('roles',))
    class Meta:
        fields = ('id', 'name', 'description', 'can_access_admin', 'capabilities')


class UserSchema(ma.Schema):
    role = fields.Nested('RoleSchema', many=False, exclude=('capabilities',))
    class Meta:
        fields = ('id', 'login', 'password', 'nickname', 'first_name', 'last_name', 'email', 'registered', 'status', 'role_id', 'avatar_id', 'page_id', 'role')


class VariableSchema(ma.Schema):
    class Meta:
        fields = ('id', 'key', 'value')