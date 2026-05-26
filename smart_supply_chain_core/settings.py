import json
import os
from pathlib import Path

# 1. FIX: Keep BASE_DIR as a Path object so Django's forward-slash / operator works perfectly
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Load your custom PostgreSQL parameters from db_config.json safely using Path
with open(BASE_DIR / 'db_config.json', 'r') as f:
    db_cfg = json.load(f)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3l#zhi8^tc%=xr)1$p)p*@lo2b(k%g%-lbrovhs09m7@vk1)z%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'forecasting',
    # 'models',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'smart_supply_chain_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # FIX: Using proper Path slash notation here too
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'smart_supply_chain_core.wsgi.application'


# Database Configuration
# 3. FIX: Hook up your live PostgreSQL engine here instead of SQLite!
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db_cfg["POSTGRES_DB"],
        'USER': db_cfg["POSTGRES_USER"],
        'PASSWORD': db_cfg["POSTGRES_PASSWORD"],
        'HOST': db_cfg["POSTGRES_HOST"],
        'PORT': db_cfg["POSTGRES_PORT"],
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
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'