# Import necessary Python libraries for handling file paths + environment variables
import os
from pathlib import Path

# --- Core Paths and Settings ---
# Build paths inside the project like this: BASE_DIR / 'subdir'
# BASE_DIR points to the root folder of the project (bf_backend_v2)
BASE_DIR = Path(__file__).resolve().parent.parent

# A secret key used for cryptographic signing
# Kept private in production!
SECRET_KEY = 'django-insecure-&97*1w%=16+j274*jws2yseggontf4eh36os@cw+jjikn^&vwq' 

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True shows detailed error pages
# Set to False for a live website
DEBUG = True

# A list of allowed hostnames/domains for this site
ALLOWED_HOSTS = []

# Points to the main urls.py file for the project
ROOT_URLCONF = 'butterfly_api.urls'

# Points to the WSGI application used by production servers
WSGI_APPLICATION = 'butterfly_api.wsgi.application'

# The default primary key type for new models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Application Definitions ---
# A list of all Django apps that are active in this project
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',

    # My custom apps
    'shop', 
    'users',
]

# A list of middleware components that process requests + responses globally
# Order is important!!!
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Manages user sessions
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', # Adds CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Manages user authentication
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- Database ---
# Database configuration
# Default is a simple SQLite3 file
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- Templates ---
# Configuration for Django's template engine
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], # List of directories to search for templates outside of apps
        'APP_DIRS': True, # This tells Django to look for a 'templates' folder inside each app
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

# --- Static Files (CSS, JavaScript, Images) ---
# The URL prefix for static files (e.g., /static/shop/css/style.css)
STATIC_URL = 'static/'

# A list of additional directories where Django will look for static files
STATICFILES_DIRS = [
    # Left empty as all static files are inside app directories
]

# This tells Django where to collect all static files into
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# --- Internationalisation & Password Validation (Standard) ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Custom Project Settings ---
# The URL name to redirect to for pages that require a login
LOGIN_URL = 'login-page'