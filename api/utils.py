from flask import jsonify


def bad_request(msg):
    return jsonify({'response': 'Could not verify. ' + msg, 'status': 401})