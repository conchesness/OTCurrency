from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField
from app.Data import User
from flask import session
# full_name = session["displayName"]

class JobForm(FlaskForm):
    title = StringField("Short Description")
    desc = TextAreaField("Reason")
    hours = IntegerField("How many hours approximately")
    submit = SubmitField("Submit")
