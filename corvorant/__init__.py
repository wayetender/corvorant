from flask import Flask
from flask import session
from flask import g
from flask import request
import logging
import os
from models import DBSession


app = Flask(__name__)
app.config.from_object('corvorant.config')
app.config.from_envvar('OVERRIDE_SETTINGS', silent=True)

logging.basicConfig(level=app.config['LOG_LEVEL'], format=app.config['LOG_FORMAT'])
app.logger.setLevel(app.config['LOG_LEVEL'])

@app.before_request
def before_request():
    g.logger = logging.getLogger('corvorant')
    logging.getLogger().setLevel(app.config['LOG_LEVEL'])
    g.config = app.config
    # if 'sessionid' in request.headers:
    #     g.session = db.load_session(request.headers.get('sessionid'))
    # else:
    #     g.session = None

@app.after_request
def teardown_request(response):
    DBSession.commit()
    return response

@app.teardown_appcontext
def shutdown_session(exception=None):
    DBSession.remove()

@app.errorhandler(Exception)
def error_handler(ex):
    g.logger.exception(ex)
    g.db_session.rollback()
    return "{'result': 'error', 'message': '%s'}" % str(ex), 500


############################################ VIEWS ###########################################
from views import home
app.register_blueprint(home.mod)
