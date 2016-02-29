import os
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'gettingstarted.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gettingstarted.settings")

import django
application = get_wsgi_application()
import p

