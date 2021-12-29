import os
from dj_static import Cling
from django.core.wsgi import get_wsgi_application
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapp.settings")

application = Cling(get_wsgi_application())