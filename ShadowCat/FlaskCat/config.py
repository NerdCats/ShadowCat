from pymongo import MongoClient

# Server configurations
DEBUG = True
# SERVER_NAME doesn't work on localhost
# SERVER_NAME = '0.0.0.0'
SERVER_PORT = 1337
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

# Broadcaster configurations
BC_URL = 'http://gofetch.cloudapp.net:1001/signalr'
BC_HUB = 'ShadowHub'
