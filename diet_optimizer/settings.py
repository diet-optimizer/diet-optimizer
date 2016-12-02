# settings.py
from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# settings.py

SPOONACULAR_KEY = os.environ.get("SPOONACULAR_KEY")
APP_KEY = os.environ.get("APP_KEY")

import sys
import urlparse
try:

    # Check to make sure DATABASES is set in settings.py file.
    # If not default to {}

    if 'DATABASES' not in locals():
        DATABASES = {}

    if 'DATABASE_URL' in os.environ:
        url = urlparse.urlparse(os.environ['DATABASE_URL'])

        # Ensure default database exists.
        DATABASES['default'] = DATABASES.get('default', {})

        # Update with environment configuration.
        DATABASES['default'].update({
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
        })


        if url.scheme == 'mysql':
            DATABASES['default']['ENGINE'] = 'flask.db.backends.mysql'
except Exception:
    print 'Unexpected error:', sys.exc_info()
