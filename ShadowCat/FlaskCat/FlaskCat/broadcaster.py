from signalr import Connection


class Broadcaster(object):
    def __init__(self,
                 url=None,
                 hubname=None,
                 session=None):
        self.connection = Connection(url, session)
        self.hub = self.connection.register_hub(hubname)
        self.hub.client.on('getLocation', self.get_location)

    @staticmethod
    def get_location(location):
        print location

    def broadcast(self, location):
        self.hub.server.invoke('sendLocation', location)
        self.connection.wait(1)
