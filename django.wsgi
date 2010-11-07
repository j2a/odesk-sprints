import os
import sys

current_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

activate_this = os.path.join(current_dir, 've', 'bin', 'activate_this.py')

# activate virtualenv
execfile(activate_this, {'__file__': activate_this})

# add project itself to system path
if current_dir not in sys.path:
    sys.path.append(current_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'local_settings'
os.environ['PYTHON_EGG_CACHE'] = '/var/www/python_eggs/'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
