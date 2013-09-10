import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

from corvorant import db
from corvorant.models import DBSession

username = 'admin'
password = 'admin'

user = db.find_user(username)
if not user:
	u = db.create_user(username, password)
	u.is_admin = True
	DBSession.add(u)
	DBSession.commit()
	print "User with username %s and password %s created." % (username, password)
else:
	print "User %s already created" % username
