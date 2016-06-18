from pymongo import MongoClient

# Server configurations
DEBUG = True
PING_SERVICE_PORT = 1337
DATA_SERVICE_PORT = 1338
SUBSCRIPTION_SVC_PORT = 1339
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
DB_COLL_SUBSCRIPTIONS = DB_DATABASE.subscriptions

# Azure Service Bus configurations
SVC_BUS_NAMESPACE = 'gobdmjolinir'
SVC_BUS_ACCESS_KEY_NAME = 'RootManageSharedAccessKey'
SVC_BUS_ACCESS_KEY_VALUE = 'W7RPzuTkjuRtajrTpc1rmh0e0fWg3KHNbXxxCHa/lKU='
QUEUE_NAME = 'shadowcat'


QUEUE_MAX_SIZE = '5120'
QUEUE_MSG_TTL = 'PT1M'

# SignalR broadcaster configurations
BC_URL = 'http://gofetch.cloudapp.net:1001/signalr'
BC_HUB = 'ShadowHub'
