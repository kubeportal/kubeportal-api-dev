from flask import Blueprint
from api.consts import API_VERSION
from api.app import login_manager

login_bp = Blueprint('login_bp', __name__)


@login_bp.route(API_VERSION + '/login', methods=['POST'])
def login():
    pass


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class User:
    def __init__(self):
        self.active = 'true'
        self.id = 1
        self.authenticated = 'false'

    def is_active(self):
        """True, as all users are active."""
        if self.active == 'true':
            return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        if self.authenticated == "true":
            return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False