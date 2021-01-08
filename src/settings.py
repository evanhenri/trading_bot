import os


# Configuration values common to all containers
APP_NAME = 'trader'

DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_PASS = os.environ['DB_PASS']
DB_PORT = os.environ['DB_PORT']
DB_USER = os.environ['DB_USER']

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']

# CELERY_RESULT_BACKEND = REDIS_URI
# CELERY_BROKER_TRANSPORT = REDIS_URI
