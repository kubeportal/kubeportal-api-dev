from flask import Flask
from flask_cors import CORS
from functools import wraps
import jwt
import datetime
import os
import json

from . import mock
from . import security
from .utils import bad_request

from api.consts import SECRET_KEY

login_manager = LoginManager()


def register_blueprints():
    from api.login import login_bp
    from api.api import api_bp
    app.register_blueprint(login_bp)
    app.register_blueprint(api_bp)


def create_app():
    app = Flask(__name__)
    CORS(app)
    login_manager.init_app(app)
    return app


app = create_app()
register_blueprints()
app.config['SECRET_KEY'] = SECRET_KEY


