from FlaskCat import app
from models import User

from flask import request
from bson.json_util import dumps
from datetime import datetime, timedelta

coll_history = app.config['DB_COLL_HISTORY']
coll_pings = app.config['DB_COLL_PINGS']


@app.route('/')
@app.route('/api')
def api_home():
    return '.:: Welcome to ShadowCat API ::.'


@app.route('/api/ping', methods=['POST'])
def ping_location():
    json_data = request.get_json()
    data = User(
        json_data["asset_id"],
        json_data["point"]
    )
    coll_history.insert_one(data.__dict__)

    user_data = coll_pings.find_one({"asset_id": json_data["asset_id"]})
    if not user_data:
        coll_pings.insert_one(data.__dict__)
    else:
        coll_pings.update_one({"asset_id": json_data["asset_id"]},
                              {'$set': {"point": json_data["point"],
                                        "timestamp": datetime.utcnow() + timedelta(hours=6)}
                               })
    return dumps(data.__dict__), 201


@app.route('/api/location/<asset_id>', methods=['GET'])
def get_location(asset_id):
    user_data = coll_pings.find_one({'asset_id': asset_id})
    if not user_data:
        return 'Not found!', 404
    else:
        return dumps(user_data)


@app.route('/api/history/<asset_id>', methods=['GET'])
def get_history(asset_id):
    cursor = coll_history.find({'asset_id': asset_id})
    history = []
    for document in cursor:
        history.append(document)
    return dumps(history)
