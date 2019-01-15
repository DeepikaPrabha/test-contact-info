import hashlib
import os

from flask_httpauth import HTTPBasicAuth

PASSWORD = os.environ['password']
USERNAME = os.environ['username']

auth = HTTPBasicAuth()

@auth.get_password
def get_pw(username):
    has_pwd = PASSWORD
    return has_pwd


@auth.hash_password
def hash_pw(password):
    return hashlib.md5(password.encode()).hexdigest()


@auth.verify_password
def verify_password(username, password):
    if hash_pw(password) == get_pw(username) and username == USERNAME:
        return True

    return False
