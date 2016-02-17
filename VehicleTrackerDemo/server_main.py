from server import TCPServer
from load_config import get_configurations

# Load configurations
config = get_configurations("config.json")

# Create and start the server
server = TCPServer(config["host"],
                   config["port"],
                   config["buffer_size"],
                   config["queue_size"])
server.start_server()
