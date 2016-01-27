"""
models.py

User module models.
"""
from app.mod_auth.models import MyAdventure

api = MyAdventure()


class User:
    def __init__(self, token):
        res = api.get('/user/', token=token)
        self.id = token
        self.email = res['user']['email']

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

