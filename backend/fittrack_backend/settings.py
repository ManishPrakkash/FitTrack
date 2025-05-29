"""
Django settings for fittrack_backend project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-key-for-development-only')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'fitrack-backend.vercel.app']

# Application definition
INSTALLED_APPS = [
    # Local apps first to ensure they're loaded before admin
    'authentication',
    'challenges',
    'activities',

    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'cors_middleware.CorsMiddleware',  # Custom CORS middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fittrack_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fittrack_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# MongoDB connection with better timeout and retry settings
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb+srv://manishprakkash:HYeLg73wjj0593Gy@fitrack-db.9hmlhdb.mongodb.net/?retryWrites=true&w=majority&appName=fitrack-db&serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&socketTimeoutMS=10000&maxPoolSize=10&retryReads=true')

# Database configuration with fallback
USE_MONGODB = os.environ.get('USE_MONGODB', 'True').lower() == 'true'

if USE_MONGODB:
    # Use MongoDB for production
    DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'NAME': 'fittrack_db',
            'CLIENT': {
                'host': MONGODB_URI,
                'username': os.environ.get('MONGODB_USERNAME', 'manishprakkash'),
                'password': os.environ.get('MONGODB_PASSWORD', 'HYeLg73wjj0593Gy'),
                'authSource': 'admin',
                'authMechanism': 'SCRAM-SHA-1',
                'serverSelectionTimeoutMS': 5000,
                'connectTimeoutMS': 10000,
                'socketTimeoutMS': 10000,
                'maxPoolSize': 10,
                'retryWrites': True,
                'retryReads': True,
            },
        }
    }
else:
    # Fallback to SQLite for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(BASE_DIR / 'db.sqlite3'),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Using Django's built-in User model for now
# AUTH_USER_MODEL = 'authentication.User'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'authentication.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# CORS settings
CORS_ORIGIN_ALLOW_ALL = True  # Allow all origins during development
CORS_ALLOW_ALL_ORIGINS = True  # For newer versions of django-cors-headers
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Add specific origins if needed
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5173',
    'https://fitrack-lime.vercel.app',
]
