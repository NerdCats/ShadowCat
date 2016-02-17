# from server import TCPServer
from tracker import Tracker
import json

# Load configurations
json_data = open("config.json").read()
data = json.loads(json_data)

if "host" in data:
    host = data["host"]
else:
    host = "127.0.0.1"

if "port" in data:
    port = data["port"]
else:
    port = 32767

if "buffer_size" in data:
    buffer_size = data["buffer_size"]
else:
    buffer_size = 1024

if "server_queue" in data:
    queue_size = data["server_queue"]
else:
    queue_size = 5

# FIXME: server and client's not working from same location
# Create and start the server
# server = TCPServer(host, port, buffer_size, queue_size)
# server.start_server()

imei = "442283480893012"
tracker = Tracker(host, port, buffer_size, imei)
tracker.ping_server()
