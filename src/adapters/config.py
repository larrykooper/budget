import os
import logging
import sys 

APP_NAME = 'budget'

# Set to False to force reporting queries to share pool with non-reporting queries
REPORTING_POOL = True

POOL_MIN_SIZE = 1
POOL_MAX_SIZE = 10
POOL_MAX_IDLE = 60
POOL_STAT_SLEEP = 300


if not REPORTING_POOL:
    pool_max_size += 5


CURR_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_BASE_PATH = os.path.abspath(os.path.join(CURR_PATH, os.pardir))

try:
    LOG_PATH = os.environ['LOG_PATH']
except KeyError:
    LOG_PATH = PROJECT_BASE_PATH + '/budget.log'


try:
    DATABASE_STRING = os.environ['PG_CONN']
except KeyError:
    key_msg = 'Database environment variable not set.  Need PG_CONN string'
    sys.exit(key_msg)


try:
    APP_DEBUG_RAW = os.environ['APP_DEBUG']
    if APP_DEBUG_RAW == 'False':
        APP_DEBUG = False
    else:
        APP_DEBUG = True
except KeyError:
    APP_DEBUG = False

