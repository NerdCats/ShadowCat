from FlaskCat import app

if __name__ == '__main__':
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    server = HTTPServer(WSGIContainer(app))
    server.listen(app.config['SERVER_PORT'])
    IOLoop.instance().start()
