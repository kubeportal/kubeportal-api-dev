from flask import jsonify, Blueprint, request
from flask_login import login_required
from functools import wraps
import json

from api import mock
from api.consts import API_VERSION
from api.login import User, find_user

api_bp = Blueprint('api_bp', __name__)


@api_bp.route('/')
def hello_world():
    return jsonify({'Json sagt': 'Hallo, I bims, der Json ' + API_VERSION})


@api_bp.route(API_VERSION + '/users/<uid>', methods=['GET'])
def get_current_user(uid):
    user = find_user(username=uid)
    return jsonify(user)


@api_bp.route(API_VERSION + '/webapps', methods=['GET'])
def get_all_webapps():
    return jsonify(mock.webapps)


@api_bp.route(API_VERSION + '/statistics/<metricname>', methods=['GET'])
def get_cluster_statistics(metricname):
    metrics = mock.metrics
    '''
    iterate through the list of metrics, remove whitespaces in key and convert key to lowerspace to match with url param
    '''
    for metric in metrics:
        if next(iter(metric)).lower().replace(' ', '') == metricname:
            return jsonify(metric)
    return jsonify({'metric': None})


