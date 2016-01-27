"""
models.py

User module models.
"""
from app.mod_auth.models import MyAdventure

api = MyAdventure()


class User:
    email = None
    facebook_id = None
    name = None

    def __init__(self, user_id):
        self.id = user_id

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

