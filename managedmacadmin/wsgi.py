"""
WSGI config for abcxx project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
import site

site.addsitedir('/var/mdm/env/lib/python2.7/site-packages')
sys.path.append('/var/mdm/env/managedmacadmin')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "managedmacadmin.settings")

activate_env='/var/mdm/env/bin/activate_this.py'
execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
