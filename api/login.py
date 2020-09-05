from flask import Blueprint, request, jsonify, session
from api.consts import API_VERSION
from api.mock import users
from functools import wraps

import json

login_bp = Blueprint('login_bp', __name__)


def log_info(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print(f'request data: {request.headers["Host"]}')
        print(f'request data: {request.headers["Content-Length"]}')
        return f(*args, **kwargs)
    return decorated


@login_bp.route(API_VERSION + '/login', methods=['POST'])
@log_info
def login():
    request_data = json.loads(request.data.decode('utf-8'))
    print(request_data)
    try:
        userdata = find_user(request_data.get('username'))
        if userdata is not None:
            session['username'] = request_data.get('username')
            return userdata
    except KeyError as e:
        print(e.__cause__)
        return jsonify({'username': None, 'status': 400})
    return jsonify({'username': None, 'status': 400})


def find_user(username):
    return next((user for user in users if user['username'] == username), {'user': None})


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