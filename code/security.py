from user import User
from werkzeug.security import safe_str_cmp

users = [
    User(1, 'Bibek', 'asdf')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


def authenticate(username, password):  # creates JWT  token
    username = username_mapping.get(username, None)
    if username and safe_str_cmp(username.password, password):
        return username


def identity(payload):  # validate JWT passed in header
    user_id = payload.get('identity')
    return userid_mapping.get(user_id, None)

