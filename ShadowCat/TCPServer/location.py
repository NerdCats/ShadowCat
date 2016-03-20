import random


class Location:
    """
        Location class
    """

    def __init__(self, lat=0, lon=0):
        self.lat = lat
        self.lon = lon

    def random_location(self):
        self.lat = random.uniform(20, 26)
        self.lon = random.uniform(88, 92)

    def random_movement(self):
        if self.lat == 0 or self.lon == 0:
            self.random_location()

        self.lat += random.random() / 100
        self.lon += random.random() / 100
