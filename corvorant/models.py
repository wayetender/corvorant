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
    is_admin = Column(Boolean, default=False)
    sessions = relationship("Session", cascade="all,delete", backref="user", order_by="Session.expires")


class Session(Base):
    __tablename__ = 'sessions'

    def __init__(self, sessionid, user_id, expires):
        self.sessionid = sessionid
        self.user_id = user_id
        self.expires = expires

    sessionid = Column(String(255), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    expires = Column(DateTime)


class Term(Base):
    __tablename__ = 'terms'

    def __init__(self, name):
        self.name = name

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    current = Column(Boolean, default=True)
    terms = relationship("Course", backref="term")


class Course(Base):
    __tablename__ = 'courses'

    def __init__(self, code, name, term_id):
        self.code = code
        self.name = name
        self.term_id = term
        self.created = datetime.datetime.now()

    id = Column(Integer, primary_key=True)
    code = Column(String(16))
    name = Column(String(255))
    created = Column(DateTime)
    term_id = Column(Integer, ForeignKey('terms.id'))
    description = Column(String)
    archived = Column(Boolean, default=False)

