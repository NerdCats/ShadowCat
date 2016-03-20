# from server import TCPServer
from tracker import Tracker
from load_config import get_configurations

# Load configurations
config = get_configurations("config.json")

imei = "442283480893012"
tracker = Tracker(config["host"],
                  config["port"],
                  config["buffer_size"],
                  imei)
tracker.ping_server()
