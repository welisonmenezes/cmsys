from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app import app_config

Engine = create_engine(app_config['SQLALCHEMY_DATABASE_URI'],  pool_recycle=3600, echo=False)
Session = scoped_session(sessionmaker(bind=Engine))