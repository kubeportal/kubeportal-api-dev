from flask import Flask, jsonify
from flask_cors import CORS
from . import mock

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return jsonify({'Json sagt' : 'Hallo, I bims, der Json'})

@app.route('/users/<uid>', methods=['GET'])
def get_current_user(uid):
    users = mock.users
    for user in users:
        if user['username'] == uid:
            return jsonify(user)

@app.route('/webapps', methods=['GET'])
def get_all_webapps():
    return jsonify(mock.webapps)

@app.route('/statistics', methods=['GET'])
def get_cluster_statistics():
    return jsonify(mock.statistics)