from servicebus_queue import ServiceBusQueue
from broadcaster import Broadcaster
import pymongo
import logging

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

while True:
    # implement with database first
    # if that seems problematic, move to service bus
    pass
