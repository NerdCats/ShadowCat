from datetime import datetime, timedelta


class Users(object):
    def __init__(self,
                 user_id,
                 name,
                 location,
                 timestamp=datetime.now() + timedelta(hours=6)):
        self.user_id = user_id
        self.name = name
        self.location = location
        self.timestamp = timestamp


class Device(object):
    def __init__(self, imei, phone_number):
        self.imei = imei
        self.phone_number = phone_number
