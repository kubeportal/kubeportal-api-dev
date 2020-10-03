from flask import Blueprint, jsonify
from flask_cors import cross_origin
from flask_api import status

from api import mock
from api.consts import API_VERSION

api_bp = Blueprint('/api_bp', __name__)


@api_bp.route('/')
def hello_json():
    print()
    return jsonify({'Json sagt': 'Hallo, I bims der Json.'}), status.HTTP_200_OK


@api_bp.route('/version', methods=['GET'])
def get_api_version():
    return jsonify({'Json sagt': API_VERSION}), status.HTTP_200_OK


@api_bp.route(f'/api/{API_VERSION}/cluster/<slug>', methods=['GET'])
@cross_origin(allow_headers=['Content-Type', 'Authorization'],
              methods=['GET', 'OPTIONS'],
              expose_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Headers', 'Origin', 'Accept',
                              'Access-Control-Allow-Origin', 'X-Requested-With', 'Access-Control-Request-Headers'],
              supports_credentials=True,
              origins=['http://localhost:8086'])
def get_cluster_info(slug):
    cluster_info = mock.cluster_info
    for key, value in cluster_info.items():
        if slug == key:
            data = {slug: value}
            return jsonify(data), status.HTTP_200_OK
    return jsonify({'error': 'not found'}), status.HTTP_404_NOT_FOUND


@api_bp.route(f'/api/{API_VERSION}/webapps/<id>', methods=['GET'])
@cross_origin(allow_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Origin'],
              methods=['GET', 'OPTIONS'],
              expose_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Headers', 'Origin', 'Accept',
                              'Access-Control-Allow-Origin', 'X-Requested-With', 'Access-Control-Request-Headers'],
              supports_credentials=True,
              origins=['http://localhost:8086'])
def get_webapp(id):
    webapps = mock.webapps
    webapp = next((webapp for webapp in webapps if webapp['id'] == id), None)
    if webapp:
        data = {"link_name": webapp.get('link_name')}, {"link_url": webapp.get('link_url')}
        return jsonify(data), status.HTTP_200_OK
    return jsonify({'error': 'bad request'}), status.HTTP_400_BAD_REQUEST


@api_bp.route(f'/api/{API_VERSION}/groups/<id>', methods=['GET'])
@cross_origin(allow_headers=['Content-Type', 'Authorization'],
              methods=['GET', 'OPTIONS'],
              expose_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Headers', 'Origin', 'Accept',
                              'Access-Control-Allow-Origin', 'X-Requested-With', 'Access-Control-Request-Headers'],
              supports_credentials=True,
              origins=['http://localhost:8086'])
def get_group(id):
    groups = mock.groups
    group = next((group for group in groups if group['id'] == id), None)
    if group:
        data = {"name": group.get('group_name')}
        return jsonify(data), status.HTTP_200_OK
    return jsonify({'error': 'bad request'}), status.HTTP_400_BAD_REQUEST
