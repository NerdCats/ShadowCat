import optparse


def flaskrun(app, default_host='127.0.0.1',
             default_port=5000):
    parser = optparse.OptionParser()
    parser.add_option('-H', '--host',
                      help='Hostname for the app' +
                           '[default %s]' % default_host,
                      default=default_host)
    parser.add_option('-P', '--port',
                      help='Port for the app' +
                           '[default %s]' % default_port,
                      default=default_port)
    parser.add_option('-D', '--debug',
                      action='store_true', dest='debug',
                      help=optparse.SUPPRESS_HELP)

    (options, args) = parser.parse_args()

    app.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )
