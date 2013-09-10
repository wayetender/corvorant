from sqlalchemy import func, not_
import logging
import hashlib
import uuid
import datetime

from corvorant import config
from models import DBSession
from models import User
from models import Session


###################################### USERS ##########################################
def find_user(username):
    return DBSession.query(User).filter(func.lower(User.username) == func.lower(username)).first()


def get_user(username):
    u = find_user(username)
    if not u:
        raise RuntimeError("user %s not found" % username)
    return u


def hash_password(password):
    return hashlib.sha512(password + config.PASSWORD_SALT).hexdigest()


def create_user(username, password):
    logging.debug("creating user %s" % (username))
    if find_user(username):
    	raise RuntimeError("User %s already exists" % (username))
    hashed_password = hash_password(password)
    u = User(username=username, password=hashed_password)
    DBSession.add(u)
    DBSession.flush()
    DBSession.expunge(u)
    return u


def find_user_by_password(username, password):
    hashed_password = hash_password(password)
    return DBSession.query(User).filter(func.lower(User.username) == func.lower(username), User.password == hashed_password).first()


###################################### SESSIONS #######################################
def make_session(user, sessionid=None, expires_in=3600):
    if not sessionid:
        sessionid = str(uuid.uuid4())
    DBSession.query(Session).filter(Session.sessionid == sessionid).delete()
    logging.debug("making session for %s with sessionid %s" % (user.username, sessionid))
    s = Session(user_id=user.id, sessionid=sessionid, expires=datetime.datetime.now() + datetime.timedelta(0, expires_in))
    DBSession.add(s)
    DBSession.flush()
    DBSession.expunge(s)
    return s


def active_sessions_count():
    return DBSession.query(Session).filter(Session.expires > datetime.datetime.now()).count()


def load_session(sessionid):
    session = DBSession.query(Session).filter(Session.sessionid == sessionid).first()
    if session and session.expires < datetime.datetime.now():
        logging.debug("session %s expired" % (sessionid))
        DBSession.delete(session)
        return None
    else:
        return session


def delete_session(sessionid):
    DBSession.query(Session).filter(Session.sessionid == sessionid).delete()

