"""
models.py

Login module models.
"""

from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class LoginForm(Form):
    name = StringField('name', validators=[DataRequired()])
    name = StringField('password', validators=[DataRequired()])
