from FlaskCat import app
from models import User
import utilities

from flask import request
from bson.json_util import dumps
from datetime import datetime
import pymongo

coll_history = app.config['DB_COLL_HISTORY']
coll_pings = app.config['DB_COLL_PINGS']


@app.route('/')
@app.route('/api')
def api_home():
    return dumps('.:: Welcome to ShadowCat API ::.')


@app.route('/api/ping', methods=['POST'])
def ping_location():
    json_data = request.get_json()
    error = utilities.validate_input(json_data)
    if error:
        return error

    data = User(
        json_data["asset_id"],
        json_data["point"]
    )
    coll_history.insert_one(data.__dict__)
    coll_pings.update_one(
        {"asset_id": json_data["asset_id"]},
        {
            '$set': {
                "point": json_data["point"],
                "timestamp": datetime.utcnow()
            }
        },
        upsert=True
    )
    return dumps(''), 201, {'Content-Type': 'application/json'}


@app.route('/api/location/<asset_id>', methods=['GET'])
def get_location(asset_id):
    user_data = coll_pings.find_one({'asset_id': asset_id})
    if not user_data:
        message = 'Asset not found!'
        return dumps(message), 404
    else:
        iso_data = utilities.to_isoformat_datetime(user_data)
        return dumps(iso_data)


@app.route('/api/history/<asset_id>', methods=['GET'])
@app.route('/api/history/<asset_id>/<document_limit>', methods=['GET'])
def get_history(asset_id, document_limit=10):
    cursor = coll_history.find(
        {'asset_id': asset_id}
    ).sort(
        "timestamp", pymongo.DESCENDING
    ).limit(int(document_limit))
    history = []
    for document in cursor:
        doc = utilities.to_isoformat_datetime(document)
        history.append(doc)
    return dumps(history)
