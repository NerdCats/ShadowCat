from json import dumps

expected_keys = ('asset_id', 'point')
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
