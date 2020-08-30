from flask import jsonify, Blueprint
from flask_login import login_required

from api import mock
from api.consts import API_VERSION
from api.login import User
api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/')
def hello_world():
    return jsonify({'Json sagt': 'Hallo, I bims, der Json ' + API_VERSION})


@api_bp.route(API_VERSION + '/users/<uid>', methods=['GET'])
@login_required
def get_current_user(uid):
    users = mock.users
    user = User(next((user for user in users if user['username'] == uid), {'user': None}))
    return jsonify(user)


@api_bp.route(API_VERSION + '/webapps', methods=['GET'])
@login_required
def get_all_webapps():
    return jsonify(mock.webapps)


@api_bp.route(API_VERSION + '/statistics/<metricname>', methods=['GET'])
@login_required
def get_cluster_statistics(metricname):
    metrics = mock.metrics
    '''
    iterate through the list of metrics, remove whitespaces in key and convert key to lowerspace to match with url param
    '''
    for metric in metrics:
        if next(iter(metric)).lower().replace(' ', '') == metricname:
            return jsonify(metric)
    return jsonify({'metric': None})