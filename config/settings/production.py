"""
Production settings for config project.

This file imports all settings from base.py and overrides them for production.
"""

import os
import dj_database_url
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set in production")

# Allow all hosts for Cloud Run flexibility
ALLOWED_HOSTS = ['*']

# CSRF trusted origins for Cloud Run
CSRF_TRUSTED_ORIGINS = ['https://*.run.app']

# Database configuration using dj-database-url
# Reads from DATABASE_URL environment variable, falls back to default if not found
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Fallback to default database configuration (should not happen in production)
    # This is a safety measure, but DATABASE_URL should be set in production
    pass

# WhiteNoise configuration for static files
# Add WhiteNoise middleware at the top of MIDDLEWARE (after SecurityMiddleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add WhiteNoise middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# WhiteNoise storage configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Static files root for production (where collectstatic will gather files)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

