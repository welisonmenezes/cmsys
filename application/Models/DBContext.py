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


class Template(Base):
    __tablename__ = 'Template'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    value = Column(Text(4294000000), nullable=False)
    # relationships
    post_types = relationship('PostType', back_populates='template')


class PostType(Base):
    __tablename__ = 'Post_Type'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    type = Column(String(50), nullable=False)
    # foreignKeys
    template_id = Column(Integer, ForeignKey('Template.id'))
    # relationships
    template = relationship('Template', back_populates='post_types')
    posts = relationship('Post', back_populates='post_type')
    nests = relationship('Nest', back_populates='post')
    post_types = relationship('PostType', secondary=Post_Type_Taxonomy, back_populates='taxonomies')
    

class Post(Base):
    __tablename__ = 'Post'
    id = Column(Integer, primary_key=True)
    slug = Column(String(255), nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(15), nullable=False)
    is_protected = Column(Boolean, nullable=False)
    has_comments = Column(Boolean, nullable=False)
    created = Column(DateTime, default=now, nullable=False)
    edited = Column(DateTime, default=now, onupdate=now, nullable=False)
    # foreignKeys
    parent_id = Column(Integer, ForeignKey('Post.id'), nullable=True)
    post_type_id = Column(Integer, ForeignKey('Post_Type.id'), nullable=False)
    # relationships
    parent = relationship('Post', back_populates='children')
    children = relationship('Post', back_populates='parent')
    post_type = relationship('PostType', back_populates='posts')
    nests = relationship('Nest', back_populates='post')
    term = relationship('Term', back_populates='page')
    terms = relationship('Term', secondary=Post_Term, back_populates='posts')
    groupers = relationship('Grouper', back_populates='post')


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
    post = relationship('Post', back_populates='nests')
    post_type = relationship('PostType', back_populates='nests')


class Term(Base):
    __tablename__ = 'Term'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(100), nullable=True)
    description = Column(String(255), nullable=True)
    # foreignKeys
    parent_id = Column(Integer, ForeignKey('Term.id'), nullable=True)
    page_id = Column(Integer, ForeignKey('Post.id'), nullable=True)
    taxonomy_id = Column(Integer, ForeignKey('Taxonomy.id'), nullable=True)
    # relationships
    parent = relationship('Term', back_populates='children')
    children = relationship('Term', back_populates='parent')
    page = relationship('Post', back_populates='term')
    posts = relationship('Post', secondary=Post_Term, back_populates='terms')
    taxonomy = relationship('Taxonomy', back_populates='terms')


class Taxonomy(Base):
    __tablename__ = 'Taxonomy'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    has_child = Column(Boolean, nullable=False)
    # relationships
    terms = relationship('Term', back_populates='taxonomy')
    post_types = relationship('PostType', secondary=Post_Type_Taxonomy, back_populates='taxonomies')


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
    parent = relationship('Grouper', back_populates='children')
    children = relationship('Grouper', back_populates='parent')
    post = relationship('Post', back_populates='groupers')
    fields = relationship('Field', back_populates='grouper')


class Field(Base):
    __tablename__ = 'Field'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    type = Column(String(15), nullable=False)
    order = Column(Integer, nullable=False)
    # foreignKeys
    grouer_id = Column(Integer, ForeignKey('Grouper.id'), nullable=False)
    # relationships
    grouper = relationship('Grouper', back_populates='fields')
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
    field = relationship('Field', back_populates='contents')


class FieldText(Base):
    __tablename__ = 'Field_Text'
    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    # foreignKeys
    field_id = Column(Integer, ForeignKey('Field.id'), nullable=False)
    # relationships
    field = relationship('Field', back_populates='texts')


class FieldFile(Base):
    __tablename__ = 'Field_File'
    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    # foreignKeys
    field_id = Column(Integer, ForeignKey('Field.id'), nullable=False)
    media_id = Column(Integer, ForeignKey('Media.id'), nullable=False)
    # relationships
    field = relationship('Field', back_populates='files')
    media = relationship('Media', back_populates='media')


class Media(Base):
    __tablename__ = 'Media'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    type = Column(String(100), nullable=False)
    file = Column(LargeBinary, nullable=False)
    origin = Column(String(50), nullable=False)
    # relationships
    field_files = relationship('FieldFile', back_populates='media')