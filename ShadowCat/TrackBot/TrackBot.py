from audioop import mul

from geojson import Point
import random
import time

from TCPServer.client import TCPClient


class TrackBot(object):
    def __init__(self, host, port, buffer_size, imei=""):
        self.client = TCPClient(host, port, buffer_size)
        self.imei = imei
        self.location = Point((0, 0))

    def ping_server(self):
        self.ping_random()
        message = "{}, {}, {}".format(
            self.location['coordinates'][0],
            self.location['coordinates'][1],
            self.imei
        )
        self.client.send_message(message)
        time.sleep(5)

    @staticmethod
    def get_random_location():
        return Point((
            random.uniform(20, 26),
            random.uniform(88, 92)
        ))

    def ping_random(self):
        if self.location['coordinates'][0] == 0\
                and self.location['coordinates'][1] == 0:
            self.location = self.get_random_location()

        multiplier = random.choice([1, -1])
        lat = self.location['coordinates'][0] + (random.random() / 100 * multiplier)
        lon = self.location['coordinates'][1] + (random.random() / 100 * multiplier)
        self.location = Point((lat, lon))
