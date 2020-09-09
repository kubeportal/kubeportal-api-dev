from flask import jsonify, Blueprint
from api import mock
from api.consts import API_VERSION

api_bp = Blueprint('api_bp', __name__)


@api_bp.route('/')
def hello_json():
    return jsonify({'Json sagt': 'Hallo, I bims der Json.'})


@api_bp.route('/version', methods=['GET'])
def get_api_version():
    return jsonify({'Json sagt': API_VERSION })


@api_bp.route(f'{API_VERSION}/cluster/<info>', methods=['GET'])
def get_api_version(info):
    cluster_info = mock.cluster_info
    for (key, value) in cluster_info:
        if key == info:
            return value
    return jsonify({'metric': None})


@api_bp.route(f'{API_VERSION}/webapps/<id>', methods=['GET'])
def get_webapp(id):
    webapps = mock.webapps
    webapp = next((webapp for webapp in webapps if webapp['id'] == id), None)
    if webapp:
        return jsonify({"link_name": webapp.get('link_name')}, {"link_url": webapp.get('link_url')})
    return jsonify(mock.webapps)


@api_bp.route(f'{API_VERSION}/groups/<id>', methods=['GET'])
def get_group(id):
    groups = mock.groups
    group = next((group for group in groups if group['id'] == id), None)
    if group:
        return group.get('group_name')
    return jsonify(mock.webapps)

