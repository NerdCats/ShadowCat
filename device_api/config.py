from pymongo import MongoClient

# Server configurations
DEBUG = True
# SERVER_NAME doesn't work on localhost
# SERVER_NAME = '0.0.0.0:7000'
JSON_AS_ASCII = False

# Database configurations
DB_HOST = 'taskcatmongo.cloudapp.net'
DB_PORT = 27017
DB_CLIENT = MongoClient(DB_HOST, DB_PORT)
DB_NAME = 'shadowcat'
DB_DATABASE = DB_CLIENT[DB_NAME]

COLL_HTTP_DEVICES = 'httpDevices'
COLL_PINGS = 'pings'
COLL_HISTORY = 'history'

# the following shows the collection name as
# COLL_HTTP_DEVICES, ... etc, if that's the
# collection's name it needs to be fixed
DB_COLL_DEVICES = DB_DATABASE.COLL_HTTP_DEVICES
DB_COLL_PINGS = DB_DATABASE.COLL_PINGS
DB_COLL_HISTORY = DB_DATABASE.COLL_HISTORY
