"""
Initialize user module

"""
from app.mod_user.models import User


def get_user(email):
    user = User()
    user.id = email
    return user
