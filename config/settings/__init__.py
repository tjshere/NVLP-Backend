"""
Django settings module that loads the appropriate settings based on environment.

Set DJANGO_SETTINGS_ENV environment variable to 'production' to use production settings.
Otherwise, development settings (base.py) will be used.
"""

import os

# Check environment variable to determine which settings to load
ENVIRONMENT = os.environ.get('DJANGO_SETTINGS_ENV', 'development').lower()

if ENVIRONMENT == 'production':
    from .production import *
else:
    from .base import *

