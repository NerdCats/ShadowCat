from location import Location
from client import TCPClient
import time


class Tracker:
    def __init__(self, host, port, buffer_size, imei=""):
        self.loc = Location()
        self.client = TCPClient(host, port, buffer_size)
        self.imei = imei

    def ping_server(self):
        while True:
            self.loc.random_movement()
            message = "{}, {}, {}".format(
                    self.loc.lat, self.loc.lon, self.imei)
            self.client.send_message(message)
            time.sleep(10)
