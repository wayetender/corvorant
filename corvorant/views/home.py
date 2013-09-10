from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
from flask import request
from flask import g

mod = Blueprint('general', __name__)

@mod.route('/')
def index():
    return render_template('index.html')

@mod.route('/about')
def about():
    return render_template('about.html')

