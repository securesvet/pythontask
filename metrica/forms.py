from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, IPAddress


class SearchForm(FlaskForm):
    submit = SubmitField('Submit')


class IpForm(SearchForm):
    ip = StringField('IP Address', validators=[IPAddress()])
    submit = SubmitField('Submit')


class UserAgentForm(SearchForm):
    user_agent = StringField('User Agent', validators=[DataRequired()])


class DateForm(SearchForm):
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])


class IpDateForm(IpForm, DateForm):
    submit = SubmitField('Submit')
