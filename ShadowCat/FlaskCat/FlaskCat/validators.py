expected_keys = ('asset_id', 'point')
point_keys = ('coordinates', 'type')


def validate_input(jason):
    for key in expected_keys:
        if key not in jason:
            return '"{}" not provided'.format(key)

    if 'point' in jason:
        for key in point_keys:
            if key not in jason['point']:
                return '"{}" not present in "point"'.format(key)

        if len(jason['point']['coordinates']) != 2:
            return '"coordinates" not conformant to geojson'
