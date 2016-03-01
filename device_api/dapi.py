from flask import Flask, request
from pymongo import MongoClient
from bson.json_util import dumps
from datetime import datetime, timedelta
from models import User, Device

app = Flask(__name__)

host = 'taskcatmongo.cloudapp.net'
port = 27017
client = MongoClient(host, port)
db = client.shadowcat                       # Database: shadowcat
devices = db.httpDevices                    # Collection: httpDevice
current_ping = db.currentLocation           # Collection: currentLocation
location_history = db.locationHistory       # Collection: locationHistory


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
    devices.insert_one(data.__dict__)
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
    location_history.insert_one(data.__dict__)

    user_data = current_ping.find_one({"user_id": json_data["user_id"]})
    if not user_data:
        current_ping.insert_one(data.__dict__)
    else:
        current_ping.update_one({"user_id": json_data["user_id"]},
                                {'$set': {"point": json_data["point"],
                                          "timestamp": datetime.utcnow() + timedelta(hours=6)}
                                 })
    # return jsonify({'data': data}), 201
    return dumps(data.__dict__), 201


# Save current location of Asset
@app.route('/api/current', methods=['POST', 'GET'])
def ping_current():
    if request.method == 'GET':
        cursor = current_ping.find()
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

        user_data = current_ping.find_one({"user_id": json_data["user_id"]})
        if not user_data:
            current_ping.insert_one(data)
        else:
            current_ping.update_one({"user_id": json_data["user_id"]},
                                    {'$set': {"point": json_data["point"]}})

        return dumps(data), 201


@app.route('/api/devices', methods=['GET'])
def get_devices():
    cursor = devices.find()
    device_list = []
    for document in cursor:
        device_list.append(document)

    return dumps(device_list)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True
    )
