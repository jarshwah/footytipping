import os 
import sys
import site

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
SITE_PACKAGES = os.path.join(SITE_ROOT, '../lib/python2.7/site-packages')

site.addsitedir(SITE_PACKAGES)
sys.path.insert(0, os.path.join(SITE_ROOT,'../' ))
sys.path.insert(0, SITE_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'footytipping.settings'

from django.core.handlers import wsgi
application = wsgi.WSGIHandler()
