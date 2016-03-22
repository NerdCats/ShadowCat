import random
import time
from geojson import Point

from client import TCPClient


class TrackBot(object):
    def __init__(self, host, port, buffer_size, imei=""):
        self.client = TCPClient(host, port, buffer_size)
        self.imei = imei
        self.location = Point((0, 0))

    @staticmethod
    def get_random_location():
        return Point((
            random.uniform(20, 26),
            random.uniform(88, 92)
        ))

    def ping_tcp(self, point):
        message = 'lat={},lon={},imei={}'.format(
            point['coordinates'][0],
            point['coordinates'][1],
            self.imei
        )
        self.client.send_message(message)
        time.sleep(5)

    def ping_tcp_random(self):
        if self.location['coordinates'][0] == 0 \
                and self.location['coordinates'][1] == 0:
            self.location = TrackBot.get_random_location()

        multiplier = random.choice([1, -1])
        lat = self.location['coordinates'][0] + (random.random() / 100 * multiplier)
        lon = self.location['coordinates'][1] + (random.random() / 100 * multiplier)
        self.location = Point((lat, lon))
        self.ping_tcp(self.location)
