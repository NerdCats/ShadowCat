from pymongo import MongoClient

# Server configurations
DEBUG = True
PING_SERVICE_PORT = 1337
DATA_SERVICE_PORT = 1338
JSON_AS_ASCII = False

# Database configurations
DB_HOST = 'gofetch.cloudapp.net'
DB_PORT = '27017'
DB_USER = ''
DB_PASS = ''

if DB_USER == '' or DB_PASS == '':
    DB_CONN_STR = 'mongodb://' + DB_HOST + ':' + DB_PORT
else:
    DB_CONN_STR = 'mongodb://' + DB_USER + ':' + DB_PASS + '@' + DB_HOST + ':' + DB_PORT

DB_CLIENT = MongoClient(DB_CONN_STR)
DB_NAME = 'shadowcat'
DB_DATABASE = DB_CLIENT[DB_NAME]
DB_COLL_DEVICES = DB_DATABASE.httpDevices
DB_COLL_PINGS = DB_DATABASE.pings
DB_COLL_HISTORY = DB_DATABASE.history

# Azure Service Bus configurations
SVC_BUS_NAMESPACE = 'pyzure'
SVC_BUS_ACCESS_KEY_NAME = 'RootManageSharedAccessKey'
SVC_BUS_ACCESS_KEY_VALUE = 'BhSjDnj6xsHC5tmd73qRlZKdHYWdM6RM3YyF028hPH4='
QUEUE_NAME = 'taskqueue'
QUEUE_MAX_SIZE = '5120'
QUEUE_MSG_TTL = 'PT1M'
