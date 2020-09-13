from flask import jsonify, Blueprint
from flask_api import status
from api import mock
from api.consts import API_VERSION

api_bp = Blueprint('api_bp', __name__)


@api_bp.route('/')
def hello_json():
    return jsonify({'Json sagt': 'Hallo, I bims der Json.'})


@api_bp.route('/version', methods=['GET'])
def get_api_version():
    return jsonify({'Json sagt': API_VERSION}), status.HTTP_200_OK


@api_bp.route(f'{API_VERSION}/cluster/<slug>', methods=['GET'])
def get_cluster_info(slug):
    cluster_info = mock.cluster_info
    for key, value in cluster_info.items():
        if slug == key:
            response = jsonify({slug: value})
            return response, status.HTTP_200_OK
    return jsonify(status.HTTP_404_NOT_FOUND)


@api_bp.route(f'{API_VERSION}/webapps/<id>', methods=['GET'])
def get_webapp(id):
    webapps = mock.webapps
    webapp = next((webapp for webapp in webapps if webapp['id'] == id), None)
    if webapp:
        response = jsonify({"link_name": webapp.get('link_name')}, {"link_url": webapp.get('link_url')})
        return response, status.HTTP_200_OK
    return jsonify(status.HTTP_400_BAD_REQUEST)


@api_bp.route(f'{API_VERSION}/groups/<id>', methods=['GET'])
def get_group(id):
    groups = mock.groups
    group = next((group for group in groups if group['id'] == id), None)
    if group:
        response = jsonify({"name": group.get('group_name')})
        return response, status.HTTP_200_OK
    return jsonify(status.HTTP_400_BAD_REQUEST)
