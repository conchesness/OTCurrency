from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField
from app.Data import User
from flask import session
# full_name = session["displayName"]

class JobForm(FlaskForm):
    title = StringField("Short Description")
    desc = TextAreaField("Longer description (optional)")
    difficulty = SelectField("How musch effort is required (scale of 1-5)",
                            choices=[("1 - a few mins, maybe just by email","1 - a few mins, maybe just by email"),
                                     ("2 - an hr max","2 - an hr max"),
                                     ("3 - a couple hours","3 - a couple hours"),
                                     ("4 - a couple sessions","4 - a couple sessions"),
                                     ("5 - regular sessions","5 - regular sessions")])
    category = SelectField(u"Select a Category: ", choices=[("academic","academic"),("labor","labor"),("other","other")])
    submit = SubmitField("Submit")
