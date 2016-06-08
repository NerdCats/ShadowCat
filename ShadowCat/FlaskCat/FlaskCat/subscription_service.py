from flask import Flask, request
from flask.ext.cors import CORS
from bson.json_util import dumps
from servicebus_queue import ServiceBusQueue
import utilities
import logging

app = Flask(__name__)
CORS(app)
app.config.from_object('config')

# azure servicebus queue
svc = ServiceBusQueue(
    app.config['SVC_BUS_NAMESPACE_SUB'],
    app.config['SVC_BUS_ACCESS_KEY_NAME_SUB'],
    app.config['SVC_BUS_ACCESS_KEY_VALUE_SUB'],
    app.config['QUEUE_NAME_SUB']
)


# payload = sub(asset, subscriber)
@app.route('/subscribe', methods=['POST'])
def subscribe():
    json_data = request.get_json()
    json_data['subscription'] = "on"
    logger.debug(json_data)
    svc.send(json_data)

    return dumps(""), 200, {'Content-Type': 'application/json'}


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    json_data = request.get_json()
    json_data['subscription'] = "off"
    logger.debug(json_data)
    svc.send(json_data)

    return dumps(""), 200, {'Content-Type': 'application/json'}


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
