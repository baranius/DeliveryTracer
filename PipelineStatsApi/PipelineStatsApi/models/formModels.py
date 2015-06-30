from flask_wtf import Form
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired 
import flask_wtf

class RepositoryForm(Form):
    """representation of repository"""

    id = IntegerField('repositoryId')
    uri = StringField('uri', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
