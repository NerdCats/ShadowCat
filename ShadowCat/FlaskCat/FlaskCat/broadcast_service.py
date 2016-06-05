from flask import Flask, request
from flask.ext.cors import CORS
from broadcaster import Broadcaster
from bson.json_util import dumps
import utilities
import logging

app = Flask(__name__)
CORS(app)
app.config.from_object('config')

bcaster = Broadcaster(
    app.config['BC_URL'],
    app.config['BC_HUB']
)

subscriptions = {}


# payload = sub(asset, subscriber)
@app.route('/subscribe', methods=['POST'])
def subscribe():
    json_data = request.get_json()
    subscribers = []
    if json_data['asset'] not in subscriptions:
        subscribers.append(json_data['subscriber'])
        subscriptions[json_data['asset']] = subscribers
    else:
        subscriptions[json_data['asset']].append(json_data['subscriber'])

    return 200, {'Content-Type': 'application/json'}


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    json_data = request.get_json()
    if json_data['asset'] not in subscriptions:
        return dumps('Asset not found'), 404, {'Content-Type': 'application/json'}
    else:
        try:
            subscriptions[json_data['asset']].remove(json_data['asset'])
            # return something
        except ValueError as e:
            logger.error(e.message)
            return dumps('Subscriber not found'), 404, {'Content-Type': 'application/json'}


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
