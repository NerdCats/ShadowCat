from flask import request, Flask
from flask.ext.cors import CORS
from models import User
from bson.json_util import dumps
from datetime import datetime
import pymongo
import utilities
import logging

app = Flask(__name__)
CORS(app)
app.config.from_object('config')


@app.route('/api/ping', methods=['POST'])
def ping_location():
    json_data = request.get_json()
    error = utilities.validate_input(json_data)
    if error:
        logger.debug("Inconsistent input: %s", error)
        return error, 422

    data = get_payload(json_data)
    add_ping(data)
    add_history(data)

    return dumps(''), 201, {'Content-Type': 'application/json'}


def get_payload(raw_data):
    if 'name' in raw_data:
        name = raw_data["name"]
    else:
        name = "Name not provided"

    return User(
        raw_data["asset_id"],
        name,
        raw_data["point"]
    )


def add_ping(data):
    try:
        app.config['DB_COLL_PINGS'].update_one(
            {"asset_id": data.asset_id},
            {
                '$set': {
                    "point": data.point,
                    "name": data.name,
                    "timestamp": datetime.now()
                }
            },
            upsert=True
        )
    except pymongo.errors.AutoReconnect as e:
        logger.error(e.message)
    except Exception as e:
        logger.error(e.message)


def add_history(data):
    try:
        app.config['DB_COLL_HISTORY'].insert_one(data.__dict__)
        logger.debug("User data: %s", data.__dict__)
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
    server.listen(app.config['PING_SERVICE_PORT'])
    logger.info('Server listening at port: %s', app.config['PING_SERVICE_PORT'])

    logger.info('Starting ping service...')
    IOLoop.instance().start()
