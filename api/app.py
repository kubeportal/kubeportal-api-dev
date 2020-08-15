from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from . import mock
from . import security

import json

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return jsonify({'Json sagt' : 'Hallo, I bims, der Json'})


@app.route('/users/<uid>', methods=['GET'])
def get_current_user(uid):
    users = mock.users
    user = next((user for user in users if user['username'] == uid), {'user' : None})
    return jsonify(user)


@app.route('/webapps', methods=['GET'])
def get_all_webapps():
    return jsonify(mock.webapps)


@app.route('/statistics/<metricname>', methods=['GET'])
def get_cluster_statistics(metricname):
    metrics = mock.metrics
    '''
    iterate through the list of metrics, remove whitespaces in key and convert key to lowerspace to match with url param
    '''
    for metric in metrics:
        if next(iter(metric)).lower().replace(' ', '') == metricname:
            return jsonify(metric)
    return jsonify({'metric': None})


@app.route('/login', methods=['POST'])
def login():
    auth = json.loads(request.data.decode('utf-8'))
    print(auth)
    authenticated = security.authenticate(auth['username'], auth['password'])
    if authenticated is None:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic Realm="Login Required"'})
    else:
        return ''
