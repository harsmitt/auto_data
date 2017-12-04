"""
WSGI config for DataAutomation project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DataAutomation.settings")
#
# application = get_wsgi_application()

import os, sys
print ("mahima")
# import pdb;pdb.set_trace()
# Calculate the path based on the location of the WSGI script.
apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)
sys.path.append(project)

# Add the path to 3rd party django application and to django itself.
sys.path.append('/home/administartor')
os.environ['DJANGO_SETTINGS_MODULE'] = 'DataAutomation.settings'
# import django.core.handlers.wsgi
# application = django.core.handlers.wsgi.WSGIHandler()

# import os
#
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
