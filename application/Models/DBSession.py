from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

Engine = create_engine('mysql+pymysql://root:@localhost/testes',  pool_recycle=3600)
Session = scoped_session(sessionmaker(bind=Engine))