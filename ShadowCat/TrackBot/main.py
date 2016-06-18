import sys
import getopt


def usage():
    print "usage: %s -d" % sys.argv[0]
    print "usage: %s --demo" % sys.argv[0]


def deploy_trackbot(asset_id, name):
    from trackbot import TrackBot
    from geojson import Point
    import utilities
    import random

    config = utilities.load_config("config.json")
    data = utilities.load_dummy_data("dummy_data.json")
    bot = TrackBot(
        config['host'],
        config['port'],
        config['buffer_size'],
        config['url']
    )
    i = random.randint(0, len(data))
    for location in data[i]['coordinates']:
        point = Point((
            location[0],
            location[1]
        ))
        print bot.ping_api(asset_id, name, point)


def main():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "dh",
            ["dummy", "help"]
        )
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    for option, argument in opts:
        if option in ('-d', '--dummy'):
            print "starting dummy tracker..."
            deploy_trackbot('123456', 'Demo')
        elif option in ('-h', '--help'):
            usage()
        else:
            usage()


if __name__ == "__main__":
    main()




# from trackbot import TrackBot
# from utilities import load_config
#
# config = load_config('config.json')
#
# imei = "442283480893012"
# tracker = TrackBot(
#     config['host'],
#     config['port'],
#     config['buffer_size'],
#     config['url'],
#     imei
# )
#
# # while True:
# #     tracker.ping_tcp_random()
#
# while True:
#     print tracker.ping_api_random('123', 'Shaphil')
