from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, IPAddress


class SearchForm(FlaskForm):
    ip = StringField('IP Address', validators=[IPAddress()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[])
    password = StringField('Password', validators=[])
    submit = SubmitField('Submit')
