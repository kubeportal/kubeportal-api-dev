from flask import Blueprint, request
from flask_login import (current_user, login_required, login_user, logout_user)
from api.consts import API_VERSION
from api.app import login_manager
from api.mock import users

import json

login_bp = Blueprint('login_bp', __name__)


@login_bp.route(API_VERSION + '/login', methods=['POST'])
def login():
    request_data = json.loads(request.data.decode('utf-8'))
    try:
        user = load_user(request_data.get('username'))
        if user is not None:
            login_user(user, remember=True)
    except KeyError as e:
        print(e.__cause__)


@login_manager.user_loader
def load_user(username):
    authenticated_user = next((user for user in users if user['username'] == username), {'user': None})
    return User(authenticated_user)


class User:
    def __init__(self, user):
        self.active = 'false'
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