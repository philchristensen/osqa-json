# encoding:utf-8
import os.path

SITE_SRC_ROOT = os.path.dirname(__file__)
LOG_FILENAME = 'django.osqa.log'

#for logging
import logging
logging.basicConfig(
    filename=os.path.join(SITE_SRC_ROOT, 'log', LOG_FILENAME),
    level=logging.ERROR,
    format='%(pathname)s TIME: %(asctime)s MSG: %(filename)s:%(funcName)s:%(lineno)d %(message)s',
)

#ADMINS and MANAGERS
ADMINS = ()
MANAGERS = ADMINS

DEBUG = True
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': True
}
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)


DATABASE_NAME = 'osqa'             # Or path to database file if using sqlite3.
DATABASE_USER = 'osqa'               # Not used with sqlite3.
DATABASE_PASSWORD = 'liejujryn'               # Not used with sqlite3.
DATABASE_ENGINE = 'mysql'  #mysql, etc
DATABASE_HOST = 'localhost'
DATABASE_PORT = '3306'

CACHE_BACKEND = 'file://%s' % os.path.join(os.path.dirname(__file__),'cache').replace('\\','/')
#CACHE_BACKEND = 'dummy://'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

APP_URL = 'http://megatron.bubblehouse.org/osqa' #used by email notif system and RSS

#LOCALIZATIONS
TIME_ZONE = 'America/New_York'

###########################
#
#   this will allow running your forum with url like http://site.com/forum
#
#   FORUM_SCRIPT_ALIAS = 'forum/'
#
FORUM_SCRIPT_ALIAS = '' #no leading slash, default = '' empty string


#OTHER SETTINGS

USE_I18N = True
LANGUAGE_CODE = 'en'

DJANGO_VERSION = 1.1
OSQA_DEFAULT_SKIN = 'default'

DISABLED_MODULES = ['books', 'recaptcha', 'project_badges', 'facebookauth', 'oauthauth', 'openidauth']
