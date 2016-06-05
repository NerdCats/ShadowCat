from signalr import Connection


class Broadcaster(object):
    def __init__(self, url, hubname, session):
        self.connection = Connection(url, session)
        self.hub = self.connection.register_hub(hubname)
