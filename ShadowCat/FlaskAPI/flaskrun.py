import optparse


def flaskrun(app, host=None, port=None):
    parser = optparse.OptionParser()
    parser.add_option('-H', '--host',
                      help='Hostname for the app' +
                           '[default %s]' % host,
                      default=host)
    parser.add_option('-P', '--port',
                      help='Port for the app' +
                           '[default %s]' % port,
                      default=port)
    parser.add_option('-D', '--debug',
                      action='store_true', dest='debug',
                      help=optparse.SUPPRESS_HELP)

    (options, args) = parser.parse_args()

    if options.host is None or options.port is None:
        app.run(
            debug=options.debug
        )
    else:
        app.run(
            debug=options.debug,
            host=options.host,
            port=int(options.port)
        )
