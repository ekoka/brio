# coding=utf8
import os
import uuid
import locale

PROJECT_NAME = 'brio'
SECRET_KEY = uuid.uuid4().hex

# LOCALE
#LOCALE = 'fr_CA.UTF-8'
#locale.setlocale(locale.LC_ALL, LOCALE)
#AVAILABLE_LANGS = dict(fr=u'Français', en=u'English')
#DEFAULT_LANG = 'en'

# PATHS
filepath = os.path.realpath(__file__)
PROJECT_PATH = os.path.dirname(os.path.dirname(filepath))
APP_PATH = '/'.join([PROJECT_PATH, PROJECT_NAME])
LOGGING_PATH = '/'.join([PROJECT_PATH, 'logs/code.log'])
# static files
#STATIC_PATH = '/'.join([PROJECT_PATH, 'static'])

DB_DIALECT = "postgresql+psycopg2"
DB_NAME = PROJECT_NAME
DB_HOST = 'localhost'
DB_USER = PROJECT_NAME
DB_PASSWORD = '1234abcd'
connect_string = "{dialect}://{user}:{password}@{host}/{dbname}".format(
    dialect=DB_DIALECT, 
    user=DB_USER, 
    password=DB_PASSWORD, 
    host=DB_HOST,
    dbname=DB_NAME)

SQLALCHEMY_BINDS                = {None: connect_string}
SQLALCHEMY_NATIVE_UNICODE       = True
SQLALCHEMY_ECHO                 = False
SQLALCHEMY_POOL_SIZE            = None
SQLALCHEMY_POOL_TIMEOUT         = None
SQLALCHEMY_POOL_RECYCLE         = None
SQLALCHEMY_MAX_OVERFLOW         = None
SQLALCHEMY_COMMIT_ON_RESPONSE   = True
