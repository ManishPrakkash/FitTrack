"""
WSGI config for fittrack_backend project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fittrack_backend.settings')

application = get_wsgi_application()

# Vercel needs the variable to be named 'app'
app = application
