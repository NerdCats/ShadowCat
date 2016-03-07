from flask import Flask, request
# from pymongo import MongoClient
from bson.json_util import dumps
from datetime import datetime, timedelta
from models import User

# host = 'taskcatmongo.cloudapp.net'
# port = 27017
# client = MongoClient(host, port)
# db = client.shadowcat                           # Database: shadowcat
# coll_devices = db.httpDevices                   # Collection: httpDevice
# coll_current_ping = db.currentLocation          # Collection: currentLocation
# coll_location_history = db.locationHistory      # Collection: locationHistory

# print client, '\n'
# print db, '\n'
# print coll_location_history, '\n'
# print coll_current_ping, '\n'
# print coll_devices, '\n'

app = Flask(__name__)


@app.route('/')
def home():
    return 'Welcome to ShadowCat'


@app.route('/api/register', methods=['POST'])
def register_device():
    json_data = request.get_json()
    data = User(
        json_data["user_id"],
        json_data["name"],
        json_data["point"],
        json_data["device"]
    )
    app.config['DB_COLL_DEVICES'].insert_one(data.__dict__)
    return dumps(data.__dict__), 201


# Save location history of the Asset
@app.route('/api/ping', methods=['POST'])
def ping_location():
    json_data = request.get_json()
    data = User(
        json_data["user_id"],
        json_data["name"],
        json_data["point"]
    )
    app.config['DB_COLL_HISTORY'].insert_one(data.__dict__)

    user_data = app.config['DB_COLL_PINGS'].find_one({"user_id": json_data["user_id"]})
    if not user_data:
        app.config['DB_COLL_PINGS'].insert_one(data.__dict__)
    else:
        app.config['DB_COLL_PINGS'].update_one({"user_id": json_data["user_id"]},
                                               {'$set': {"point": json_data["point"],
                                                         "timestamp": datetime.utcnow() + timedelta(hours=6)}
                                                })
    # return jsonify({'data': data}), 201
    return dumps(data.__dict__), 201


# Save current location of Asset
@app.route('/api/current', methods=['POST', 'GET'])
def ping_current():
    if request.method == 'GET':
        cursor = app.config['DB_COLL_PINGS'].find()
        current_locations = []
        for document in cursor:
            current_locations.append(document)

        return dumps(current_locations)

    # FIX: maybe unnecessary
    else:
        json_data = request.get_json()
        data = User(
            json_data["user_id"],
            json_data["name"],
            json_data["point"]
        )

        user_data = app.config['DB_COLL_PINGS'].find_one({"user_id": json_data["user_id"]})
        if not user_data:
            app.config['DB_COLL_PINGS'].insert_one(data)
        else:
            app.config['DB_COLL_PINGS'].update_one({"user_id": json_data["user_id"]},
                                                   {'$set': {"point": json_data["point"]}})

        return dumps(data), 201


@app.route('/api/devices', methods=['GET'])
def get_devices():
    cursor = app.config['DB_COLL_DEVICES'].find()
    device_list = []
    for document in cursor:
        device_list.append(document)

    return dumps(device_list)


if __name__ == "__main__":
    app.config.from_object('config')
    app.run()
