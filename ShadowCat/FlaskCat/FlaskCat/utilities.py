from json import dumps
import os
import json
import logging.config

expected_keys = ('asset_id', 'point', 'name')
point_keys = ('coordinates', 'type')


def validate_input(jason):
    for key in expected_keys:
        if key not in jason:
            message = '"{}" not provided'.format(key)
            return dumps(message)

    if 'point' in jason:
        for key in point_keys:
            if key not in jason['point']:
                message = '"{}" not present in "point"'.format(key)
                return dumps(message)

        if len(jason['point']['coordinates']) != 2:
            message = '"coordinates" not conformant to geojson'
            return dumps(message)


def to_isoformat_datetime(document):
    if 'timestamp' in document:
        d = document['timestamp']
        document['timestamp'] = d.isoformat()
        return document


def configure_logger(
        filename='\..\log_config.json',
        default_level=logging.DEBUG
):
    path = os.path.dirname(__file__) + filename
    if os.path.exists(path):
        with open(path, 'r+') as f:
            config = json.load(f)
        logs_folder = config['log_folder']
        if not os.path.exists(logs_folder):
            os.mkdir(logs_folder)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
