import socket
import json


class TCPServer:
    def __init__(self, host, port, buff_size, queue_size):
        self.ADDRESS = host, port
        self.BUFSIZE = buff_size
        self.queue_size = queue_size

    def start_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(self.ADDRESS)
        s.listen(self.queue_size)  # Queue up to 5 connections

        while True:
            conn, address = s.accept()
            print "Incoming connection from: ", address
            while True:
                data = conn.recv(self.BUFSIZE)
                if not data:
                    break
                print address, ":", data
                conn.sendall(data)
            conn.close()


# FIXME: should be somewhere else, looks ugly
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

# Create and start the server
server = TCPServer(host, port, buffer_size, queue_size)
server.start_server()
