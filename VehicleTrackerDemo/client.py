import socket


class TCPClient:
    def __init__(self, host, port, buff_size):
        self.HOST = host
        self.PORT = port
        self.BUFSIZE = buff_size

    def send_message(self, message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        s.sendall(message)
        data = s.recv(self.BUFSIZE)
        s.close()
        return data
