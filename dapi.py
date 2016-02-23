from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

host = 'taskcatmongo.cloudapp.net'
port = 27017
client = MongoClient(host, port)
db = client.shadowcat
devices = db.httpDevices
current_ping = db.currentLocation
location_history = db.locationHistory


@app.route('/')
def home():
    return 'Welcome'


@app.route('/api/register', methods=['POST'])
def register_device():
    data = {
        'imei': request.json['imei'],
        'PhoneNumber': request.json['phone']
    }
    devices.insert_one(data)

    return str(data), 201


# Save a location history of Asset
@app.route('/api/ping', methods=['POST'])
def ping_location():
    json_data = request.get_json()
    data = {
        "user_id": json_data["user_id"],
        "name": json_data["name"],
        "location": json_data["location"]
    }

    location_history.insert_one(data)
    user_data = current_ping.find_one({"user_id": json_data["user_id"]})
    if not user_data:
        current_ping.insert_one(data)
    else:
        current_ping.update_one({"user_id": json_data["user_id"]},
                                {'$set': {"location": json_data["location"]}})
    # return jsonify({'data': data}), 201
    return str(data), 201


# FIX: maybe unnecessary
# Save current location of Asset
@app.route('/api/current', methods=['POST'])
def ping_current():
    json_data = request.get_json()
    data = {
        "user_id": json_data["user_id"],
        "name": json_data["name"],
        "location": json_data["location"]
    }

    user_data = current_ping.find_one({"user_id": json_data["user_id"]})
    if not user_data:
        current_ping.insert_one(data)
    else:
        current_ping.update_one({"user_id": json_data["user_id"]},
                                {'$set': {"location": json_data["location"]}})

    return str(data), 201


@app.route('/api/devices', methods=['GET'])
def get_devices():
    device_list = devices.find()

    return str(device_list)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
