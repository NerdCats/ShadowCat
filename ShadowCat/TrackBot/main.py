from TrackBot import TrackBot
# from TCPServer.load_config import get_configurations

# Load configurations
# config = get_configurations("TCPServer.config.json")

imei = "442283480893012"
tracker = TrackBot('127.0.0.1',
                   32767,
                   1024,
                   imei)
while True:
    tracker.ping_server()
