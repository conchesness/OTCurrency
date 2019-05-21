from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField, DateTimeField
from app.Data import User
from flask import session
from datetime import datetime

class EventForm(FlaskForm):
    title = StringField(u'Title')
    desc = StringField(u'Description')
    location = StringField(u'Location')
    datetime = DateTimeField(u'Date and Time', default = datetime.now())
