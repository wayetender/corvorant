import logging
import os

DEBUG = True
SECRET_KEY = 'key'
PASSWORD_SALT = 'aasdpok#$3321()_IAlkjaSF_(23@IU$)(UJIFA)(U@#)_(U'

LOG_LEVEL = logging.DEBUG  # 10
LOG_FORMAT = '%(asctime)s [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)s] %(message)s'

def get_db_url():
    return os.getenv('DATABASE_URL') or 'sqlite:///corvorant.db'
