from servicebus_queue import ServiceBusQueue
from broadcaster import Broadcaster
from pymongo import MongoClient

# need to remove hard coded values
bc_svc = ServiceBusQueue(
    'pyzure',
    'RootManageSharedAccessKey',
    'BhSjDnj6xsHC5tmd73qRlZKdHYWdM6RM3YyF028hPH4=',
    'taskqueue'
)

broadcaster = Broadcaster(
    'http://gofetch.cloudapp.net:1001/signalr',
    'ShadowHub'
)

# Database configurations
host = 'gofetch.cloudapp.net'
port = 27017
client = MongoClient(host, port)
db = client.shadowcat
coll_subs = db.subscriptions

while True:
    ping = bc_svc.receive()
    cursor = coll_subs.find()
    for document in cursor:
        if document['asset_id'] == ping['asset_id']:
            # broadcast to buzzCat
            pass
