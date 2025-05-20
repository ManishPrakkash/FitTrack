"""
WSGI handler for Vercel deployment.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fittrack_backend.settings')

app = get_wsgi_application()
