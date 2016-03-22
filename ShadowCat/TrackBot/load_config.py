import json


def load_config(config_file):
    with open(config_file) as json_data:
        data = json.load(json_data)

    return {
        'host': data['host'],
        'port': data['port'],
        'buffer_size': data['buffer_size']
    }
