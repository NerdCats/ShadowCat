import socket


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
