from datetime import datetime
from geojson import Point


class User(object):
    def __init__(self,
                 asset_id,
                 point=None,
                 device=None,
                 timestamp=datetime.now()):
        self.asset_id = asset_id
        self.point = Point((
            point["coordinates"][0],
            point["coordinates"][1]
        ))
        self.device = device
        self.timestamp = timestamp


class Device(object):
    def __init__(self, imei, phone_number):
        self.imei = imei
        self.phone_number = phone_number
