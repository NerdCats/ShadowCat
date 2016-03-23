import random
import time
from geojson import Point

from client import TCPClient
import requests


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
        time.sleep(5)

    def ping_tcp_random(self):
        if self.location['coordinates'][0] == 0 \
                and self.location['coordinates'][1] == 0:
            self.location = TrackBot.get_random_location()

        self.move_randomly()
        self.ping_tcp(self.location)

    @staticmethod
    def ping_api(user_id, name, point):
        data = {
            'user_id': user_id,
            'name': name,
            'point': point
        }
        url = 'http://localhost:5000/api/ping'
        response = requests.post(url, json=data)
        return response.json()

    def ping_api_random(self, user_id, name):
        if self.location['coordinates'][0] == 0 \
                and self.location['coordinates'][1] == 0:
            self.location = TrackBot.get_random_location()

        self.move_randomly()
        return self.ping_api(user_id, name, self.location)
