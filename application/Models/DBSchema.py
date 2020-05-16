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


class ConfigurationSchema(ma.Schema):
    language = fields.Nested('LanguageSchema', many=False)
    socials = fields.Nested('LanguageSchema', many=True)
    class Meta:
        fields = ('id', 'title', 'description', 'has_comments', 'email', 'language_id', 'language', 'socials')


class LanguageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'code', 'status', 'datetime_format')


class MediaSchema(ma.Schema):
    user = fields.Nested('UserSchema', many=False, exclude=('role', 'password'))
    class Meta:
        fields = ('id', 'name', 'description', 'type', 'extension', 'origin', 'created', 'user_id', 'user')


class PostSchema(ma.Schema):
    user = fields.Nested('UserSchema', many=False, exclude=('role', 'password'))
    language = fields.Nested('LanguageSchema', many=False)
    parent = fields.Nested('PostSchema', many=False, exclude=('user', 'language', 'parent', 'children'))
    children = fields.Nested('PostSchema', many=True, exclude=('user', 'language', 'parent', 'children'))
    post_type = fields.Nested('PostTypeSchema', many=False)
    class Meta:
        fields = ('id', 'name', 'title', 'description', 'status', 'is_protected', 
        'has_comments', 'publish_on', 'expire_on', 'created', 'edited', 'parent_id', 
        'post_type_id', 'language_id', 'user_id', 'user', 'language', 'parent', 'children',
        'post_type')


class PostTypeSchema(ma.Schema):
    template = fields.Nested('TemplateSchema', many=False)
    class Meta:
        fields = ('id', 'name', 'type', 'template_id', 'template')


class RoleSchema(ma.Schema):
    capabilities = fields.Nested('CapabilitySchema', many=True, exclude=('roles',))
    class Meta:
        fields = ('id', 'name', 'description', 'can_access_admin', 'capabilities')


class SocialSchema(ma.Schema):
    user = fields.Nested('UserSchema', many=False, exclude=('role', 'socials', 'password'))
    configuration = fields.Nested('ConfigurationSchema', many=False, exclude=('socials', 'language'))
    class Meta:
        fields = ('id', 'name', 'url', 'target', 'description', 'origin', 'configuration_id', 'user_id', 'user', 'configuration')


class TemplateSchema(ma.Schema):
    post_types = fields.Nested('PostTypeSchema', many=True, exclude=('template',))
    class Meta:
        fields = ('id', 'name', 'description', 'value', 'post_types')


class UserSchema(ma.Schema):
    role = fields.Nested('RoleSchema', many=False, exclude=('capabilities',))
    socials = fields.Nested('RoleSchema', many=True)
    medias = fields.Nested('MediaSchema', many=True, exclude=('user',))
    avatar = fields.Nested('MediaSchema', many=False, exclude=('user',))
    page = fields.Nested('PostSchema', many=False, exclude=('user', 'language', 'parent', 'children', 'post_type'))
    class Meta:
        fields = ('id', 'login', 'password', 'nickname', 'first_name', 'last_name', 'email', 
        'registered', 'status', 'role_id', 'avatar_id', 'page_id', 'role', 'socials',
        'medias', 'page', 'avatar')


class VariableSchema(ma.Schema):
    class Meta:
        fields = ('id', 'key', 'value')