from flask import Blueprint, request, jsonify, session
from api.consts import API_VERSION
from api.mock import users
from functools import wraps

import json

login_bp = Blueprint('login_bp', __name__)


def log_info(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print(f'request data: {request.headers}')
        return f(*args, **kwargs)
    return decorated


@login_bp.route(f'{API_VERSION}/login', methods=['POST'])
@log_info
def login():
    request_data = json.loads(request.data.decode('utf-8'))
    print(request_data)
    try:
        userdata = _find_user(request_data.get('username'))
        request_data.get('password') # only testing
        if userdata:
            session['username'] = request_data.get('username')
            response = {"id": userdata.get('id'), "firstname": userdata.get('firstname')}
            return response
    except KeyError as e:
        print(e.__cause__)
    return jsonify({'username': None, 'status': 400})

@login_bp.route(f'{API_VERSION}/login_google', methods=['POST'])
def google_login():
    request_data = json.loads(request.data.decode('utf-8'))
    request_data.get('access_token')
    response = {"id": 1, "firstname": "Mandarin"}
    return jsonify(response)


@login_bp.route(f'{API_VERSION}/users/<id>', methods=['GET'])
def get_current_user(id):
    user = _find_user_with_id(id=id)
    return jsonify(user)


@login_bp.route(f'{API_VERSION}/<id>/webapps', methods=['GET'])
def get_user_webapps(id):
    user = _find_user_with_id(id=id)
    webapps = user.get('webapps')
    response = []
    @TODO
    for webapp in webapps:
        response.append({"link_name": webapp.get('link_name'), "link_url": webapp.get("link_url")})
    return jsonify(user.get('webapps'))

@login_bp.route(f'{API_VERSION}/users/<id>', methods=['PATCH'])
def update_user(id):
    request_data = json.loads(request.data.decode('utf-8'))
    user = _find_user_with_id(id=id)
    for (key, value) in request_data:
        user[key] = value
    return jsonify(user)


def _find_user_with_username(username):
    return next((user for user in users if user['username'] == username), {'user': None})

def _find_user_with_id(id):
    return next((user for user in users if user['id'] == id), {'user': None})

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
