from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customers(Base):
    __tablename__ = 'tst_customers'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    address = Column(String(255))
    email = Column(String(100))

class Parent(Base):
    __tablename__ = 'tst_left'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    children = relationship("Association", back_populates="parent")

class Child(Base):
    __tablename__ = 'tst_right'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    children = relationship("Association")

class Association(Base):
    __tablename__ = 'tst_association'
    id = Column(Integer, primary_key=True)
    left_id = Column(Integer, ForeignKey('tst_left.id'))
    right_id = Column(Integer, ForeignKey('tst_right.id'))
    value = Column(String(50))
    child = relationship("Child")
    parent = relationship("Parent", back_populates="children")