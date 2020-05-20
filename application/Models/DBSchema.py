from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from app import app

ma = Marshmallow(app)

exclude_post = ('user', 'language', 'parent', 'children', 'post_type', 'nests')
exclude_post_type = ('template', 'nests',)
exclude_user = ('role', 'socials', 'password', 'medias', 'avatar')
exclude_comment = ('parent', 'children', 'language', 'user', 'post')
exclude_menu_item = ('parent', 'children', 'menu')
exclude_grouper = ('parent', 'post')
exclude_field = ('post', 'grouper')

class BlacklistSchema(ma.Schema):
    class Meta:
        fields = ('id', 'type', 'value', 'target')


class CapabilitySchema(ma.Schema):
    roles = fields.Nested('RoleSchema', many=True, exclude=('capabilities',))
    class Meta:
        fields = ('id', 'description', 'type', 'target_id', 'can_write', 'can_write', 'can_read', 'can_delete', 'roles')


class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', many=False, exclude=exclude_user)
    language = fields.Nested('LanguageSchema', many=False)
    post = fields.Nested('PostSchema', many=False, exclude=exclude_post)
    parent = fields.Nested('CommentSchema', many=False, exclude=exclude_comment)
    children = fields.Nested('CommentSchema', many=True, exclude=exclude_comment)
    class Meta:
        fields = ('id', 'comment', 'status', 'origin_ip', 'origin_agent', 'created', 'post',
        'parent_id', 'user_id', 'post_id', 'language_id', 'user', 'language', 'parent', 'children')


class ConfigurationSchema(ma.Schema):
    language = fields.Nested('LanguageSchema', many=False)
    socials = fields.Nested('LanguageSchema', many=True)
    class Meta:
        fields = ('id', 'title', 'description', 'has_comments', 'email', 'language_id', 'language', 'socials')


class FieldSchema(ma.Schema):
    post = fields.Nested('PostSchema', many=False, exclude=('user', 'language', 'parent', 'children', 'post_type', 'nests', 'groupers'))
    grouper = fields.Nested('GrouperSchema', many=False, exclude=('parent', 'post', 'children'))
    class Meta:
        fields = ('id', 'name', 'description', 'type', 'order', 'grouper_id', 'post_id', 'post', 'grouper')


class FieldFileSchema(ma.Schema):
    class Meta:
        fields = ('id', 'field_id', 'grouper_id', 'post_id')


class GrouperSchema(ma.Schema):
    post = fields.Nested('PostSchema', many=False, exclude=exclude_post)
    parent = fields.Nested('CommentSchema', many=False, exclude=exclude_grouper)
    children = fields.Nested('CommentSchema', many=True, exclude=exclude_grouper)
    fields = fields.Nested('FieldSchema', many=True, exclude=exclude_field)
    class Meta:
        fields = ('id', 'name', 'description', 'order', 'parent_id', 'post_id', 'post', 'parent', 'children', 'fields')


class LanguageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'code', 'status', 'datetime_format')


class MediaSchema(ma.Schema):
    user = fields.Nested('UserSchema', many=False, exclude=exclude_user)
    class Meta:
        fields = ('id', 'name', 'description', 'type', 'extension', 'origin', 'created', 'user_id', 'user')


class MenuSchema(ma.Schema):
    language = fields.Nested('LanguageSchema', many=False)
    sectors = fields.Nested('SectorSchema', many=True, exclude=('menus',))
    items = fields.Nested('MenuItemSchema', many=True, exclude=('menu', 'parent', 'children'))
    class Meta:
        fields = ('id', 'name', 'order', 'description', 'language_id', 'language', 'sectors', 'items')


class MenuItemSchema(ma.Schema):
    parent = fields.Nested('MenuItemSchema', many=False, exclude=exclude_menu_item)
    children = fields.Nested('MenuItemSchema', many=True, exclude=exclude_menu_item)
    menu = fields.Nested('MenuSchema', many=False, exclude=('language',))
    class Meta:
        fields = ('id', 'type', 'behavior', 'url', 'target_id', 'title', 'order', 'parent_id', 'menu_id', 'parent', 'children', 'menu')


class NestSchema(ma.Schema):
    post_type = fields.Nested('PostTypeSchema', many=False, exclude=exclude_post_type)
    post = fields.Nested('PostSchema', many=False, exclude=exclude_post)
    class Meta:
        fields = ('id', 'name', 'description', 'limit', 'has_pagination', 'post_id', 'post_type_id', 'post', 'post_type')


class PostSchema(ma.Schema):
    user = fields.Nested('UserSchema', many=False, exclude=exclude_user)
    language = fields.Nested('LanguageSchema', many=False)
    parent = fields.Nested('PostSchema', many=False, exclude=exclude_post)
    children = fields.Nested('PostSchema', many=True, exclude=exclude_post)
    post_type = fields.Nested('PostTypeSchema', many=False)
    nests = fields.Nested('NestSchema', many=True, exclude=('post',))
    groupers = fields.Nested('GrouperSchema', many=True, exclude=('post', 'parent'))
    class Meta:
        fields = ('id', 'name', 'title', 'description', 'status', 'is_protected', 
        'has_comments', 'publish_on', 'expire_on', 'created', 'edited', 'parent_id', 
        'post_type_id', 'language_id', 'user_id', 'user', 'language', 'parent', 'children',
        'post_type', 'nests', 'groupers')


class PostTypeSchema(ma.Schema):
    template = fields.Nested('TemplateSchema', many=False)
    nests = fields.Nested('NestSchema', many=True, exclude=('post_type',))
    class Meta:
        fields = ('id', 'name', 'type', 'template_id', 'template', 'nests')


class RoleSchema(ma.Schema):
    capabilities = fields.Nested('CapabilitySchema', many=True, exclude=('roles',))
    class Meta:
        fields = ('id', 'name', 'description', 'can_access_admin', 'capabilities')

    
class SectorSchema(ma.Schema):
    menus = fields.Nested('MenuSchema', many=True, exclude=('sectors',))
    class Meta:
        fields = ('id', 'name', 'description', 'menus')


class SocialSchema(ma.Schema):
    user = fields.Nested('UserSchema', many=False, exclude=exclude_user)
    configuration = fields.Nested('ConfigurationSchema', many=False, exclude=('socials', 'language'))
    class Meta:
        fields = ('id', 'name', 'url', 'target', 'description', 'origin', 'configuration_id', 'user_id', 'user', 'configuration')


class TemplateSchema(ma.Schema):
    post_types = fields.Nested('PostTypeSchema', many=True, exclude=exclude_post_type)
    class Meta:
        fields = ('id', 'name', 'description', 'value', 'post_types')


class UserSchema(ma.Schema):
    role = fields.Nested('RoleSchema', many=False, exclude=('capabilities',))
    socials = fields.Nested('RoleSchema', many=True)
    medias = fields.Nested('MediaSchema', many=True, exclude=('user',))
    avatar = fields.Nested('MediaSchema', many=False, exclude=('user',))
    page = fields.Nested('PostSchema', many=False, exclude=exclude_post)
    class Meta:
        fields = ('id', 'login', 'password', 'nickname', 'first_name', 'last_name', 'email', 
        'registered', 'status', 'role_id', 'avatar_id', 'page_id', 'role', 'socials',
        'medias', 'page', 'avatar')


class VariableSchema(ma.Schema):
    class Meta:
        fields = ('id', 'key', 'value')