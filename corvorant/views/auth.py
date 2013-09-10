from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
from flask import request
from flask import g
from flask import flash
from corvorant import db
import logging

mod = Blueprint('auth', __name__)

@mod.route('/login', methods=['post','get'])
def login():
    if g.session:
        return redirect('/')
    if request.method != 'POST':
        logging.debug('got raw login')
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    user = db.find_user_by_password(username, password)
    if not user:
        logging.debug('bad username/password')
        return render_template('login.html', error='Invalid username/password')
    s = db.make_session(user)
    session['sessionid'] = s.sessionid
    flash(('success', 'You were successfully logged in.'))
    return redirect(request.args.get('back') or request.referrer or '/')


@mod.route('/logout')
def about():
    if 'sessionid' not in session:
        return redirect('/')
    db.delete_session(session['sessionid'])
    del session['sessionid']
    flash(('success', 'You were successfully logged out.'))
    return redirect('/')


@mod.route('/register')
def register():
    return render_template('register.html')
