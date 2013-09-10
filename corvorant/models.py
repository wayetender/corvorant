from sqlalchemy import *
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session, deferred, reconstructor
from flask import g
import config
import datetime
import json

Base = declarative_base()

engine = create_engine(config.get_db_url(), echo=False)
def on_connect(conn, record):
    if 'sqlite' in config.get_db_url():
        conn.execute('pragma foreign_keys=ON')
        conn.execute('PRAGMA read_uncommitted = 0')
from sqlalchemy import event
event.listen(engine, 'connect', on_connect)

session_factory = sessionmaker(bind=engine)
DBSession = scoped_session(session_factory)

class User(Base):
    __tablename__ = 'users'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.created = datetime.datetime.now()

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(129))
    created = Column(DateTime)
