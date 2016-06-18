import random
import time
from geojson import Point

from client import TCPClient
import requests


class TrackBot(object):
    def __init__(self, host, port, buffer_size, url, sleep_time=30, imei=""):
        self.client = TCPClient(host, port, buffer_size)
        self.url = url
        self.sleep_time = float(sleep_time)
        self.imei = imei
        self.location = Point((0, 0))

    @staticmethod
    def get_random_location():
        return Point((
            random.uniform(20, 26),
            random.uniform(88, 92)
        ))

    def move_randomly(self):
        multiplier = random.choice([1, -1])
        lat = self.location['coordinates'][0] + (random.random() / 100 * multiplier)
        lon = self.location['coordinates'][1] + (random.random() / 100 * multiplier)
        self.location = Point((lat, lon))

    def ping_tcp(self, point):
        message = 'lat={},lon={},imei={}'.format(
            point['coordinates'][0],
            point['coordinates'][1],
            self.imei
        )
        self.client.send_message(message)
        time.sleep(self.sleep_time)

    def ping_tcp_random(self):
        if self.location['coordinates'][0] == 0 \
                and self.location['coordinates'][1] == 0:
            self.location = TrackBot.get_random_location()

        self.move_randomly()
        self.ping_tcp(self.location)

    def ping_api(self, asset_id, name, point):
        data = {
            'asset_id': asset_id,
            'name': name,
            'point': point
        }
        response = requests.post(self.url, json=data)

        # ping every 30 seconds
        time.sleep(self.sleep_time)
        return response.json()

    def ping_api_random(self, asset_id, name):
        if self.location['coordinates'][0] == 0 \
                and self.location['coordinates'][1] == 0:
            self.location = TrackBot.get_random_location()

        self.move_randomly()
        return self.ping_api(asset_id, name, self.location)
