from datetime import datetime, timedelta


class User(object):
    def __init__(self,
                 user_id,
                 name,
                 location=None,
                 device=None,
                 timestamp=datetime.now() + timedelta(hours=6)):
        self.user_id = user_id
        self.name = name
        self.location = Location(
            location.lat,
            location.lon
        )
        self.device = Device(
            device.imei,
            device.phone_number
        )
        self.timestamp = timestamp


class Device(object):
    def __init__(self, imei, phone_number):
        self.imei = imei
        self.phone_number = phone_number


class Location(object):
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
