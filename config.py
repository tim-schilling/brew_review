import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
APP_DIR = os.path.join(BASE_DIR, 'app')

DEBUG = os.environ.get('DEBUG', True)

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URI', "postgresql://brew_review:brew_review@localhost/f_brew_review")

DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

CSRF_SESSION_KEY = os.environ.get('CSRF_SESSION_KEY', 'TBqo6whMrrqrLE74DO6okH09BV5F9UBw')
SECRET_KEY = os.environ.get('SECRET_KEY', 'Ij5ytnTm983T4zt8zuI8usKkygrdhiad')
