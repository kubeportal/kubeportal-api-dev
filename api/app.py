from flask import Flask
from flask_login import LoginManager

from api.consts import SECRET_KEY

login_manager = LoginManager()


def register_blueprints():
    from api.user import login_bp
    from api.api import api_bp
    app.register_blueprint(login_bp)
    app.register_blueprint(api_bp)


def create_app():
    app = Flask(__name__)
    login_manager.init_app(app)
    return app


app = create_app()
register_blueprints()
app.config['SECRET_KEY'] = SECRET_KEY

