import json
import random
from geojson import Point


def load_config(config_file):
    with open(config_file) as json_data:
        data = json.load(json_data)

    return {
        'host': data['host'],
        'port': data['port'],
        'buffer_size': data['buffer_size'],
        'url': data['url']
    }


def load_dummy_data(data_file):
    with open(data_file) as json_data:
        data = json.load(json_data)

    return data


# data = load_dummy_data("dummy_data.json")
# print len(data)
# i = random.randint(0, len(data))
# for location in data[i]['coordinates']:
#     point = Point((
#         location[0],
#         location[1]
#     ))
#     print point


