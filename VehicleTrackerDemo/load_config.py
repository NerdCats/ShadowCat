import json


def get_configurations(config_file):
    json_data = open(config_file).read()
    data = json.loads(json_data)

    if "host" in data:
        host = data["host"]
    else:
        host = "127.0.0.1"

    if "port" in data:
        port = data["port"]
    else:
        port = 32767

    if "buffer_size" in data:
        buffer_size = data["buffer_size"]
    else:
        buffer_size = 1024

    if "server_queue" in data:
        queue_size = data["server_queue"]
    else:
        queue_size = 5

    server_config = {
        "host": host,
        "port": port,
        "buffer_size": buffer_size,
        "queue_size": queue_size
    }

    return server_config
