from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, Table, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

now = datetime.datetime.now()


Post_Term = Table('Post_Term', Base.metadata,
    Column('post_id', Integer, ForeignKey('Post.id'), nullable=False),
    Column('term_id', Integer, ForeignKey('Term.id'), nullable=False)
)


Post_Type_Taxonomy = Table('Post_Type_Taxonomy', Base.metadata,
    Column('post_type_id', Integer, ForeignKey('Post_Type.id'), nullable=False),
    Column('taxonomy_id', Integer, ForeignKey('Taxonomy.id'), nullable=False)
)


Sector_Menu = Table('Sector_Menu', Base.metadata,
    Column('sector_id', Integer, ForeignKey('Sector.id'), nullable=False),
    Column('menu_id', Integer, ForeignKey('Menu.id'), nullable=False)
)


Capability_Role = Table('Capability_Role', Base.metadata,
    Column('capability_id', Integer, ForeignKey('Capability.id'), nullable=False),
    Column('role_id', Integer, ForeignKey('Role.id'), nullable=False)
)


class Template(Base):
    __tablename__ = 'Template'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    value = Column(Text(4294000000), nullable=False) # will have a json configuration structure
    # relationships
    post_types = relationship('PostType', back_populates='template')


class PostType(Base):
    __tablename__ = 'Post_Type'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    type = Column(String(50), nullable=False) # if the page will be to nest, user, tax, post, static, etc.
    # foreignKeys
    template_id = Column(Integer, ForeignKey('Template.id'))
    # relationships
    taxonomies = relationship('Taxonomy', secondary=Post_Type_Taxonomy, back_populates='post_types')
    template = relationship('Template', back_populates='post_types', foreign_keys='PostType.template_id')
    posts = relationship('Post', back_populates='post_type')
    pt_nests = relationship('Nest', back_populates='post_type')
    

class Post(Base):
    __tablename__ = 'Post'
    id = Column(Integer, primary_key=True)
    slug = Column(String(255), nullable=False, unique=True) # unique name/url path
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(15), nullable=False)
    is_protected = Column(Boolean, nullable=False) # if will be accessable to read without login
    has_comments = Column(Boolean, nullable=False)
    created = Column(DateTime, default=now, nullable=False)
    edited = Column(DateTime, default=now, onupdate=now, nullable=False)
    # foreignKeys
    parent_id = Column(Integer, ForeignKey('Post.id'), nullable=True)
    post_type_id = Column(Integer, ForeignKey('Post_Type.id'), nullable=False)
    language_id = Column(Integer, ForeignKey('Language.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    # relationships
    terms = relationship('Term', secondary=Post_Term, back_populates='posts')
    parent = relationship('Post', back_populates='children', foreign_keys='Post.parent_id')
    children = relationship('Post', back_populates='parent', remote_side='Post.id')
    post_type = relationship('PostType', back_populates='posts', foreign_keys='Post.post_type_id')
    nests = relationship('Nest', back_populates='post')
    term = relationship('Term', back_populates='page')
    groupers = relationship('Grouper', back_populates='post')
    language = relationship('Language', back_populates='posts', foreign_keys='Post.language_id')
    comments = relationship('Comment', back_populates='post')
    page_owner = relationship('User', back_populates='page', foreign_keys='User.page_id')
    user = relationship('User', back_populates='posts', foreign_keys='Post.user_id')


class Nest(Base):
    __tablename__ = 'Nest'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    limit = Column(Integer, nullable=False, default=0)
    has_pagination = Column(Boolean, nullable=False)
    # foreignKeys
    post_id = Column(Integer, ForeignKey('Post.id'), nullable=False)
    post_type_id = Column(Integer, ForeignKey('Post_Type.id'), nullable=False)
    # relationships
    post = relationship('Post', back_populates='nests', foreign_keys='Nest.post_id')
    post_type = relationship('PostType', back_populates='pt_nests', foreign_keys='Nest.post_type_id')


class Term(Base):
    __tablename__ = 'Term'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(100), nullable=True)
    description = Column(String(255), nullable=True)
    # foreignKeys
    parent_id = Column(Integer, ForeignKey('Term.id'), nullable=True)
    page_id = Column(Integer, ForeignKey('Post.id'), nullable=True) # the term's custom page
    taxonomy_id = Column(Integer, ForeignKey('Taxonomy.id'), nullable=False)
    language_id = Column(Integer, ForeignKey('Language.id'), nullable=False)
    # relationships
    posts = relationship('Post', secondary=Post_Term, back_populates='terms')
    parent = relationship('Term', back_populates='children', foreign_keys='Term.parent_id')
    children = relationship('Term', back_populates='parent', remote_side='Term.id')
    page = relationship('Post', back_populates='term', foreign_keys='Term.page_id')
    taxonomy = relationship('Taxonomy', back_populates='terms', foreign_keys='Term.taxonomy_id')
    language = relationship('Language', back_populates='terms', foreign_keys='Term.language_id')


class Taxonomy(Base):
    __tablename__ = 'Taxonomy'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    has_child = Column(Boolean, nullable=False) # if will have hierarchy
    # relationships
    post_types = relationship('PostType', secondary=Post_Type_Taxonomy, back_populates='taxonomies')
    terms = relationship('Term', back_populates='taxonomy')


class Grouper(Base):
    __tablename__ = 'Grouper'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    order = Column(Integer, nullable=False)
    # foreignKeys
    parent_id = Column(Integer, ForeignKey('Grouper.id'), nullable=True)
    post_id = Column(Integer, ForeignKey('Post.id'), nullable=False)
    # relationships
    parent = relationship('Grouper', back_populates='children', foreign_keys='Grouper.parent_id')
    children = relationship('Grouper', back_populates='parent', remote_side='Grouper.id')
    post = relationship('Post', back_populates='groupers', foreign_keys='Grouper.post_id')
    fields = relationship('Field', back_populates='grouper')


class Field(Base):
    __tablename__ = 'Field'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    type = Column(String(15), nullable=False) # can be content, text and file
    order = Column(Integer, nullable=False)
    # foreignKeys
    grouper_id = Column(Integer, ForeignKey('Grouper.id'), nullable=False)
    # relationships
    grouper = relationship('Grouper', back_populates='fields', foreign_keys='Field.grouper_id')
    contents = relationship('FieldContent', back_populates='field')
    texts = relationship('FieldText', back_populates='field')
    files = relationship('FieldFile', back_populates='field')


class FieldContent(Base):
    __tablename__ = 'Field_Content'
    id = Column(Integer, primary_key=True)
    content = Column(Text(4294000000), nullable=False)
    # foreignKeys
    field_id = Column(Integer, ForeignKey('Field.id'), nullable=False)
    # relationships
    field = relationship('Field', back_populates='contents', foreign_keys='FieldContent.field_id')


class FieldText(Base):
    __tablename__ = 'Field_Text'
    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    # foreignKeys
    field_id = Column(Integer, ForeignKey('Field.id'), nullable=False)
    # relationships
    field = relationship('Field', back_populates='texts', foreign_keys='FieldText.field_id')


class FieldFile(Base):
    __tablename__ = 'Field_File'
    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    # foreignKeys
    field_id = Column(Integer, ForeignKey('Field.id'), nullable=False)
    media_id = Column(Integer, ForeignKey('Media.id'), nullable=False)
    # relationships
    field = relationship('Field', back_populates='files', foreign_keys='FieldFile.field_id')
    media = relationship('Media', back_populates='field_files', foreign_keys='FieldFile.media_id')


class Media(Base):
    __tablename__ = 'Media'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    type = Column(String(100), nullable=False)
    file = Column(LargeBinary, nullable=False)
    origin = Column(String(50), nullable=False) # where came from (post, user avatar, configuration, etc...)
    # foreignKeys
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    # relationships
    field_files = relationship('FieldFile', back_populates='media')
    user = relationship('User', back_populates='medias', foreign_keys='Media.user_id')
    avatar_owner = relationship('User', back_populates='avatar', foreign_keys='User.avatar_id')


class Sector(Base):
    __tablename__ = 'Sector'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    # relationships
    menus = relationship('Menu', secondary=Sector_Menu, back_populates='sectors')


class Menu(Base):
    __tablename__ = 'Menu'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    order = Column(Integer, nullable=False)
    description = Column(String(255), nullable=True)
    # foreignKeys
    language_id = Column(Integer, ForeignKey('Language.id'), nullable=False)
    # relationships
    sectors = relationship('Sector', secondary=Sector_Menu, back_populates='menus')
    items = relationship('MenuItem', back_populates='menu')
    language = relationship('Language', back_populates='menus', foreign_keys='Menu.language_id')


class MenuItem(Base):
    __tablename__ = 'Menu_Item'
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False) # can be anchor, external link, link, etc...
    behavior = Column(String(50), nullable=False) # what window will be opened
    url = Column(String(255), nullable=True)
    target_id = Column(Integer, nullable=True)
    title = Column(String(255), nullable=False)
    order = Column(Integer, nullable=False)
    # foreignKeys
    parent_id = Column(Integer, ForeignKey('Menu_Item.id'), nullable=True)
    menu_id = Column(Integer, ForeignKey('Menu.id'), nullable=False)
    # relationships
    parent = relationship('MenuItem', back_populates='children', foreign_keys='MenuItem.parent_id')
    children = relationship('MenuItem', back_populates='parent', remote_side='MenuItem.id')
    menu = relationship('Menu', back_populates='items', foreign_keys='MenuItem.menu_id')


class Capability(Base):
    __tablename__ = 'Capability'
    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=True)
    type = Column(String(50), nullable=False) # what will access specifically (single-post, post-type, menu, user, etc...)
    target_id = Column(Integer, nullable=True) # specifc post and post_type id if type is single-post or post-type
    can_write = Column(Boolean, nullable=False)
    can_read = Column(Boolean, nullable=False)
    can_delete = Column(Boolean, nullable=False)
    # relationships
    roles = relationship('Role', secondary=Capability_Role, back_populates='capabilities')


class Role(Base):
    __tablename__ = 'Role'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    can_access_admin = Column(Boolean, nullable=False)
    # relationships
    capabilities = relationship('Capability', secondary=Capability_Role, back_populates='roles')
    users = relationship('User', back_populates='role')


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    login = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    nickname = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=False)
    registered = Column(DateTime, default=now, nullable=False)
    status = Column(String(15), nullable=False)
    # foreignKeys
    role_id = Column(Integer, ForeignKey('Role.id'), nullable=False)
    avatar_id = Column(Integer, ForeignKey('Media.id'), nullable=True)
    page_id = Column(Integer, ForeignKey('Post.id'), nullable=True)
    # relationships
    role = relationship('Role', back_populates='users', foreign_keys='User.role_id')
    socials = relationship('Social', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    medias = relationship('Media', back_populates='user', foreign_keys='Media.user_id')
    avatar = relationship('Media', back_populates='avatar_owner', foreign_keys='User.avatar_id')
    page = relationship('Post', back_populates='page_owner', foreign_keys='User.page_id')
    posts = relationship('Post', back_populates='user', foreign_keys='Post.user_id')


class Language(Base):
    __tablename__ = 'Language'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(10), nullable=False, unique=True)
    status = Column(String(15), nullable=False)
    datetime_format = Column(String(100), nullable=True) # must be an regular expression
    # relationships
    posts = relationship('Post', back_populates='language')
    terms = relationship('Term', back_populates='language')
    configurations = relationship('Configuration', back_populates='language')
    comments = relationship('Comment', back_populates='language')
    menus = relationship('Menu', back_populates='language')


class Configuration(Base):
    __tablename__ = 'Configuration'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    has_comments = Column(Boolean, nullable=False)
    email = Column(String(100), nullable=True)
    # foreignKeys
    language_id = Column(Integer, ForeignKey('Language.id'), nullable=False)
    # relationships
    language = relationship('Language', back_populates='configurations', foreign_keys='Configuration.language_id')
    socials = relationship('Social', back_populates='configuration')


class Social(Base):
    __tablename__ = 'Social'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    url = Column(String(255), nullable=False)
    target = Column(String(15), nullable=True)
    description = Column(String(255), nullable=True)
    origin = Column(String(50), nullable=False)
    # foreignKeys
    configuration_id = Column(Integer, ForeignKey('Configuration.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    # relationships
    configuration = relationship('Configuration', back_populates='socials', foreign_keys='Social.configuration_id')
    user = relationship('User', back_populates='socials', foreign_keys='Social.user_id')


class Comment(Base):
    __tablename__ = 'Comment'
    id = Column(Integer, primary_key=True)
    comment = Column(Text, nullable=False)
    status = Column(String(15), nullable=False)
    origin_ip = Column(String(100), nullable=False)
    origin_agent = Column(String(255), nullable=False)
    created = Column(DateTime, default=now, nullable=False)
    # foreignKeys
    parent_id = Column(Integer, ForeignKey('Comment.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id'), nullable=False)
    language_id = Column(Integer, ForeignKey('Language.id'), nullable=False)
    # relationships
    parent = relationship('Comment', back_populates='children', foreign_keys='Comment.parent_id')
    children = relationship('Comment', back_populates='parent', remote_side='Comment.id')
    user = relationship('User', back_populates='comments', foreign_keys='Comment.user_id')
    post = relationship('Post', back_populates='comments', foreign_keys='Comment.post_id')
    language = relationship('Language', back_populates='comments', foreign_keys='Comment.language_id')


class Blacklist(Base):
    __tablename__ = 'Blacklist'
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False) # must be what kind of item is (email, ip,  user, etc...)
    value = Column(Text, nullable=False)
    target = Column(String(100), nullable=False) # must be what kind of element will be protected (login, comments, etc...)


class Variable(Base):
    __tablename__ = 'Variable'
    id = Column(Integer, primary_key=True)
    key = Column(String(255), nullable=False, unique=True)
    value = Column(Text(4294000000), nullable=False)