from flask import Blueprint, request, jsonify, session
from flask_api import status
from flask_cors import cross_origin

from api.consts import API_VERSION
from api import mock
from functools import wraps

import json

login_bp = Blueprint('login_bp', __name__)


def log_info(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print(f'request data: {json.loads(request.data.decode("utf-8"))}')
        return f(*args, **kwargs)

    return decorated


@login_bp.route(f'/api/{API_VERSION}/login', methods=['POST'])
@cross_origin(allow_headers=['Content-Type', 'Authorization'],
              methods=['POST', 'OPTIONS'],
              expose_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Headers', 'Origin', 'Accept',
                              'Access-Control-Allow-Origin', 'X-Requested-With', 'Access-Control-Request-Headers'],
              supports_credentials=True,
              origins=['http://localhost:8086'])
def login():
    request_data = json.loads(request.data.decode('utf-8'))
    user = mock.users[0]
    try:
        request_data.get('password')  # only testing
        request_data.get('username')  # only testing
        session['username'] = user['username']
        data = {"id": user['id'], "firstname": user['firstname'], "token": "123456789"}
        return jsonify(data), status.HTTP_200_OK
    except KeyError as e:
        print(e.__cause__)
    return jsonify({'error': 'bad request'}), status.HTTP_400_BAD_REQUEST


@login_bp.route(f'/api/{API_VERSION}/login_google', methods=['POST'])
@cross_origin(allow_headers=['Content-Type', 'Authorization'],
              methods=['POST', 'OPTIONS'],
              expose_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Headers', 'Origin', 'Accept',
                              'Access-Control-Allow-Origin', 'X-Requested-With', 'Access-Control-Request-Headers'],
              supports_credentials=True,
              origins=['http://localhost:8086'])
def google_login():
    request_data = json.loads(request.data.decode('utf-8'))
    try:
        request_data.get('access_token')
        data = {"id": 1, "firstname": "Mandarin"}
        return jsonify(data), status.HTTP_200_OK
    except KeyError as e:
        print(e.__cause__)
    return jsonify({'error': 'bad request'}), status.HTTP_400_BAD_REQUEST


@login_bp.route(f'/api/{API_VERSION}/users/<id>', methods=['GET'])
@cross_origin(allow_headers=['Content-Type', 'Authorization'],
              methods=['GET', 'OPTIONS'],
              expose_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Headers', 'Origin', 'Accept',
                              'Access-Control-Allow-Origin', 'X-Requested-With', 'Access-Control-Request-Headers'],
              supports_credentials=True,
              origins=['http://localhost:8086'])
def get_current_user(id):
    user = _find_user_with_id(id=id)
    data = {"firstname": user.get('firstname'), "name": user.get('name'), "username": user.get('username'),
            "primary_email": user.get('primary_email'), "all_emails": user.get('all_emails'),
            "admin": user.get('admin'), "k8s_serviceaccount": user.get('k8s_serviceaccount'),
            "k8s_namespace": user.get('k8s_namespace'), "k8s_token": user.get('k8s_token')}
    return jsonify(data), status.HTTP_200_OK


@login_bp.route(f'/api/{API_VERSION}/users/<id>/webapps', methods=['GET'])
@cross_origin(allow_headers=['Content-Type', 'Authorization'],
              methods=['GET', 'OPTIONS'],
              expose_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Headers', 'Origin', 'Accept',
                              'Access-Control-Allow-Origin', 'X-Requested-With', 'Access-Control-Request-Headers'],
              supports_credentials=True,
              origins=['http://localhost:8086'])
def get_user_webapps(id):
    webapps = mock.webapps
    data = []
    for webapp in webapps:
        data.append({"link_name": webapp.get('link_name'), "link_url": webapp.get("link_url")})
    return jsonify(data), status.HTTP_200_OK


@login_bp.route(f'/api/{API_VERSION}/users/<id>/groups', methods=['GET'])
@cross_origin(allow_headers=['Content-Type', 'Authorization'],
              methods=['GET', 'OPTIONS'],
              expose_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Headers', 'Origin', 'Accept',
                              'Access-Control-Allow-Origin', 'X-Requested-With', 'Access-Control-Request-Headers'],
              supports_credentials=True,
              origins=['http://localhost:8086'])
def get_user_groups(id):
    user = mock.users[0]
    data = {"name": user.get('groups')}
    return jsonify(data), status.HTTP_200_OK


@login_bp.route(f'/api/{API_VERSION}/users/<id>', methods=['PATCH'])
@cross_origin(allow_headers=['Content-Type', 'Authorization'],
              methods=['GET', 'OPTIONS'],
              expose_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Headers', 'Origin', 'Accept',
                              'Access-Control-Allow-Origin', 'X-Requested-With', 'Access-Control-Request-Headers'],
              supports_credentials=True,
              origins=['http://localhost:8086'])
def update_user(id):
    request_data = json.loads(request.data.decode('utf-8'))
    user = _find_user_with_id(id=id)
    if user:
        for (key, value) in request_data:
            if key in user.keys():
                user[key] = value
            else:
                return status.HTTP_404_NOT_FOUND
        return jsonify(user), status.HTTP_200_OK
    return jsonify({'error': 'not found'}), status.HTTP_404_NOT_FOUND


def _find_user_with_username(username):
    users = mock.users
    return next((user for user in users if user['username'] == username), {'user': None})


def _find_user_with_id(id):
    users = mock.users
    return next((user for user in users if user['id'] == int(id)), {'user': None})


class User:
    def __init__(self, user):
        self.active = 'true'
        self.authenticated = 'false'
        self.id = user.get('id')
        self.name = user.get('name')
        self.username = user.get('username')
        self.firstname = user.get('firstname')
        self.primary_email = user.get('primary_email')
        self.all_emails = user.get('all_emails')
        self.webapps = user.get('webapps')
        self.admin = user.get('admin')
        self.portal_groups = user.get('portal_groups')
        self.k8s_accounts = user.get('k8s_accounts')
        self.k8s_namespace = user.get('k8s_namespace')
        self.k8s_token = user.get('k8s_token')
        self.k8s_apiserver = user.get('k8s_apiserver')
        self.k8s_clustername = user.get('clustername')

    def is_active(self):
        """True, as all users are active."""
        if self.active == 'true':
            return True

    def get_id(self):
        """Return the username to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        if self.authenticated == "true":
            return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
