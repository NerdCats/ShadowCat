from flask import Flask
from flask.ext.cors import CORS
from bson.json_util import dumps
import utilities
import pymongo
import logging

app = Flask(__name__)
CORS(app)
app.config.from_object('config')


@app.route('/api/location/<asset_id>', methods=['GET'])
def get_location(asset_id):
    try:
        user_data = app.config['DB_COLL_PINGS'].find_one({'asset_id': asset_id})
    except pymongo.errors.AutoReconnect as e:
        logger.error(e.message)
    except Exception as e:
        logger.error(e.message)

    if not user_data:
        message = 'Asset not found!'
        return dumps(message), 404
    else:
        iso_data = utilities.to_isoformat_datetime(user_data)
        return dumps(iso_data)


@app.route('/api/history/<asset_id>', methods=['GET'])
@app.route('/api/history/<asset_id>/<document_limit>', methods=['GET'])
def get_history(asset_id, document_limit=10):
    try:
        cursor = app.config['DB_COLL_HISTORY'].find(
            {'asset_id': asset_id}
        ).sort(
            "timestamp", pymongo.DESCENDING
        ).limit(int(document_limit))
    except pymongo.errors.AutoReconnect as e:
        logger.error(e.message)
    except Exception as e:
        logger.error(e.message)

    history = []
    for document in cursor:
        doc = utilities.to_isoformat_datetime(document)
        history.append(doc)
    return dumps(history)


if __name__ == '__main__':
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    logger = logging.getLogger(__name__)
    utilities.configure_logger()

    server = HTTPServer(WSGIContainer(app))
    server.listen(app.config['DATA_SERVICE_PORT'])
    logger.info('Server listening at port: %s', app.config['DATA_SERVICE_PORT'])

    logger.info('Starting data service...')
    IOLoop.instance().start()
