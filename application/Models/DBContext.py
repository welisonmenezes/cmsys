from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

now = datetime.datetime.now()

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
    parent_id = Column(Integer, ForeignKey('Post.id'))
    post_type_id = Column(Integer, ForeignKey('Post_Type.id'), nullable=False)
    # relationships
    parent = relationship('Post', back_populates='children')
    children = relationship('Post', back_populates='parent')
    post_type = relationship('PostType', back_populates='posts')
    nests = relationship('Nest', back_populates='post')


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