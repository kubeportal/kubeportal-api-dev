from flask import Flask, jsonify, request, make_response, redirect
from flask_cors import CORS
from functools import wraps
import jwt
import datetime
from . import mock
from . import security

import json

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'kubeportal'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['Authorization'].split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            verified = security.token_verify(data)
            if verified is None:
                return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic Realm="Login Failed"'})
        except:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def hello_world():
    return jsonify({'Json sagt': 'Hallo, I bims, der Json'})


@app.route('/users/<uid>', methods=['GET'])
@token_required
def get_current_user(uid):
    users = mock.users
    user = next((user for user in users if user['username'] == uid), {'user': None})
    return jsonify(user)


@app.route('/webapps', methods=['GET'])
@token_required
def get_all_webapps():
    return jsonify(mock.webapps)


@app.route('/statistics/<metricname>', methods=['GET'])
@token_required
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
        token = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                           app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token.decode('UTF-8')})
