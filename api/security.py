from werkzeug.security import safe_str_cmp

USER_DB_MOCK = [{'id': 1, 'username': 's77518', 'password': 'test'}, {'id': 2, 'username': 's12345', 'password': 'test' }]

def authenticate(username, password):
    user = next((user for user in USER_DB_MOCK if user['username'] == username), {'user': None})
    if user and safe_str_cmp(user['password'].encode('utf-8'), password.encode('utf-8')):
        return user
