from werkzeug.security import safe_str_cmp
import jwt

USER_DB_MOCK = [{'id': 1, 'username': 's77518', 'password': 'test'}, {'id': 2, 'username': 's12345', 'password': 'test' }]


def authenticate(username, password):
    user = next((user for user in USER_DB_MOCK if user['username'] == username), {'user': None})
    if user and safe_str_cmp(user['password'].encode('utf-8'), password.encode('utf-8')):
        return user


def token_verify(token):
    verify_user = token['user']
    verified = next((user for user in USER_DB_MOCK if user['username'] == verify_user['username']
                     and user['password'] == verify_user['password']), {'user': None})
    return verified