from FlaskCat import app, utilities
import logging

if __name__ == '__main__':
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    logger = logging.getLogger(__name__)
    utilities.configure_logger()

    server = HTTPServer(WSGIContainer(app))
    server.listen(app.config['SERVER_PORT'])
    logger.info('Server listening at port: %s', app.config['SERVER_PORT'])

    logger.info('Starting server...')
    IOLoop.instance().start()
