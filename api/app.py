from flask import Flask, jsonify, request, make_response, redirect
from flask_cors import CORS
from functools import wraps
import jwt
import datetime
import os
from . import mock
from . import security
import json

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
PRIVATE_KEY = os.environ.get('GOOGLE_PRIVATE_KEY')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['Authorization'].split(' ')[1]
        if not token:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic Realm="Login Failed"'})
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'])
            verified = security.token_verify(decoded_token)
            if verified is None:
                return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic Realm="Login Failed"'})
        except Exception as e:
            print(e.__cause__)
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic Realm="Login Failed"'})
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
    authenticated = security.authenticate(auth_key='username', auth_value=auth['username'], identifier=auth['password'])
    if authenticated is None:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic Realm="Login Required"'})
    else:
        token = generate_token(auth)
        return jsonify({'user_authorized': auth['username'], 'token': token.decode('UTF-8')})


@app.route('/login/authorize_google_user', methods=['POST'])
def authorize_google_user():
    authCode = json.loads(request.data.decode('utf-8')) # access_token, id_token etc.
    requested_user = jwt.decode(authCode['id_token'], PRIVATE_KEY, algorithms=['HS256'], verify=False)
    authenticated = security.authenticate(auth_key='email', auth_value=requested_user['email'],
                                          identifier=requested_user['email_verified'])
    # returns True or False and the authenticated user object
    if authenticated['authenticated_and_authorized']:
        current_user = authenticated['user']
        auth = {'email': current_user['email'], 'username': current_user['username']}
        token = generate_token(auth)
        return jsonify({'user_authorized': current_user['username'], 'token': token.decode('UTF-8')})
    else:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic Realm="Login Failed"'})


def generate_token(auth):
    return jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                           key=app.config['SECRET_KEY'], algorithm='HS256')

