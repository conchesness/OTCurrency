from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField
from app.routes.Classes import User

from flask import session
from app.routes.Classes import User

# full_name = session["displayName"]

class JobForm(FlaskForm):
    title = StringField("Short Description")
    desc = TextAreaField("Reason")
    hours = IntegerField("How many hours approximately")
    submit = SubmitField("Submit")
