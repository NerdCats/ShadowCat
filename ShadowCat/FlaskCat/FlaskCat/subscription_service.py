from flask import Flask, request
from flask.ext.cors import CORS
from bson.json_util import dumps
import pymongo
import utilities
import logging

app = Flask(__name__)
CORS(app)
app.config.from_object('config')


# payload = {asset, subscriber}
@app.route('/subscribe', methods=['POST'])
def subscribe():
    json_data = request.get_json()
    add_subscription(json_data)
    logger.debug(json_data)

    return dumps(""), 200, {'Content-Type': 'application/json'}


def add_subscription(data):
    try:
        app.config['DB_COLL_SUBSCRIPTIONS'].update_one(
            {
                "asset": data['asset'],
                "subscriber": data['subscriber']
            },
            {
                '$set': {
                    "asset": data['asset'],
                    "subscriber": data['subscriber']
                }
            },
            upsert=True
        )
    except pymongo.errors.AutoReconnect as e:
        logger.error(e.message)
    except Exception as e:
        logger.error(e.message)


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    json_data = request.get_json()
    remove_subscription(json_data)
    logger.debug(json_data)

    return dumps(""), 200, {'Content-Type': 'application/json'}


def remove_subscription(data):
    try:
        app.config['DB_COLL_SUBSCRIPTIONS'].delete_one(
            {
                "asset": data['asset'],
                "subscriber": data['subscriber']
            }
        )
    except pymongo.errors.AutoReconnect as e:
        logger.error(e.message)
    except Exception as e:
        logger.error(e.message)


if __name__ == '__main__':
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    logger = logging.getLogger(__name__)
    utilities.configure_logger()

    server = HTTPServer(WSGIContainer(app))
    server.listen(app.config['SUBSCRIPTION_SVC_PORT'])
    logger.info('Server listening at port: %s', app.config['SUBSCRIPTION_SVC_PORT'])

    logger.info('Starting ping service...')
    IOLoop.instance().start()
