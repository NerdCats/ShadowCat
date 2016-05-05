from FlaskCat import app
from models import User, AssetPayload
from broadcaster import Broadcaster
import utilities

from flask import request
from bson.json_util import dumps
from datetime import datetime
from requests import Session
import pymongo
import logging

coll_history = app.config['DB_COLL_HISTORY']
coll_pings = app.config['DB_COLL_PINGS']

bc_url = app.config['BC_URL']
bc_hub = app.config['BC_HUB']

logger = logging.getLogger(__name__)


@app.route('/')
@app.route('/api')
def api_home():
    return dumps('.:: Welcome to ShadowCat API ::.')


# Getting bulkier and bulkier...
# need to do something
@app.route('/api/ping', methods=['GET', 'POST'])
def ping_location():
    if request.method == 'POST':
        json_data = request.get_json()
        error = utilities.validate_input(json_data)
        if error:
            logger.debug("Inconsistent input: %s", error)
            return error, 422

        if 'name' in json_data:
            data = User(
                json_data["asset_id"],
                json_data["name"],
                json_data["point"]
            )
        else:
            data = User(
                json_data["asset_id"],
                "Name not provided",
                json_data["point"]
            )
        try:
            coll_history.insert_one(data.__dict__)
            logger.debug("User data: %s", data.__dict__)
            send_location(data)
        except pymongo.errors.AutoReconnect as e:
            logger.error(e.message)
        except Exception as e:
            logger.error(e.message)

        try:
            coll_pings.update_one(
                {"asset_id": json_data["asset_id"]},
                {
                    '$set': {
                        "point": json_data["point"],
                        "name": json_data["name"],
                        "timestamp": datetime.now()
                    }
                },
                upsert=True
            )
        except pymongo.errors.AutoReconnect as e:
            logger.error(e.message)
        except Exception as e:
            logger.error(e.message)

        return dumps(''), 201, {'Content-Type': 'application/json'}
    else:
        cursor = coll_pings.find()
        pings = []
        for dox in cursor:
            iso_doc = utilities.to_isoformat_datetime(dox)
            pings.append(iso_doc)
        return dumps(pings)


def send_location(data):
    payload = AssetPayload(
        data.asset_id,
        data.point,
        data.name
    )
    with Session() as session:
        broadcaster = Broadcaster(bc_url, bc_hub, session)
        with broadcaster.connection:
            broadcaster.broadcast(payload.__dict__)


@app.route('/api/location/<asset_id>', methods=['GET'])
def get_location(asset_id):
    try:
        user_data = coll_pings.find_one({'asset_id': asset_id})
    except pymongo.errors.AutoReconnect as e:
        logger.error(e.message)
    except Exception as e:
        logger.error(e.message)

    if not user_data:
        message = 'Asset not found!'
        return dumps(message), 404
    else:
        iso_data = utilities.to_isoformat_datetime(user_data)
        return dumps(iso_data)


@app.route('/api/history/<asset_id>', methods=['GET'])
@app.route('/api/history/<asset_id>/<document_limit>', methods=['GET'])
def get_history(asset_id, document_limit=10):
    try:
        cursor = coll_history.find(
            {'asset_id': asset_id}
        ).sort(
            "timestamp", pymongo.DESCENDING
        ).limit(int(document_limit))
    except pymongo.errors.AutoReconnect as e:
        logger.error(e.message)
    except Exception as e:
        logger.error(e.message)

    history = []
    for document in cursor:
        doc = utilities.to_isoformat_datetime(document)
        history.append(doc)
    return dumps(history)
