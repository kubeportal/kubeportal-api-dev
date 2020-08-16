from werkzeug.security import safe_str_cmp

USER_DB_MOCK = [
    {'id': 1, 'username': 's77518', 'password': 'test', 'email': 'anira.schas@gmail.com', 'cluster_access': 'approved'},
    {'id': 2, 'username': 's12345', 'password': 'test', 'email': 'anira.schas@gmail.com', 'cluster_access': 'rejected'},
    {'id': 1, 'username': 'peter', 'password': 'troeger', 'email': 'ptr.troeger@gmail.com', 'cluster_access': 'approved'}]


def authenticate(auth_key, auth_value, identifier):
    '''
    :param:
    - login with google: ( auth_key, auth_value, identifier ) = 'email', user email, email_verified
    - login ( auth_key, auth_value, identifier ) = 'username', username, password
    '''
    user = next((user for user in USER_DB_MOCK if user[auth_key] == auth_value), None)
    if auth_key == 'email':
        if user and user['cluster_access'] == 'approved' and identifier:
            return {'authenticated_and_authorized' : True, 'user': user }
    else:
        if user and safe_str_cmp(user['password'].encode('utf-8'), identifier.encode('utf-8')) and user['cluster_access'] == 'approved':
            return {'authenticated_and_authorized' : True, 'user': user }
    return {'authenticated_and_authorized' : False, 'user': None }


def token_verify(decoded_token):
    decoded_user = decoded_token['user']
    if 'email' in decoded_user.keys():
        print('email in keys')
        verified = next((user for user in USER_DB_MOCK if user['email'] == decoded_user['email']
                         and user['username'] == decoded_user['username']), None)
        return verified
    elif 'username' in decoded_user.keys():
        print('username in keys')
        verified = next((user for user in USER_DB_MOCK if user['username'] == decoded_user['username']
                         and user['password'] == decoded_user['password']), None)
        return verified
    else:
        print('token verify failed')
        return 'failed'
