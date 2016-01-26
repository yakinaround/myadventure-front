"""
models.py

User module models.
"""
import flask_login


class User(flask_login.UserMixin):
    pass


def get_user(email):
    user = User()
    user.id = email
    return user