from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from app.Data import User
from flask import session
from app.Data import User

# full_name = session["displayName"]

class GiveForm(FlaskForm):
    amount = IntegerField("Amount")
    recipient = SelectField(label="To", choices=[(row.name, row.name) for row in User.objects()])
    reason = StringField("Reason")
    category = SelectField(label="Category", choices = [('Helped others','Helped others'),('Did me a favor','Did me a favor'),('Did something for a teacher','Did something for a teacher'),('Class participation','Class participation'),('Community beautification','Community beautification')])
    submit = SubmitField("Submit")

    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        recipientChoices = [("----","----")]
        for row in User.objects():
            recipientChoices.append((row.name, row.name))
        recipientChoices.sort()
        # Update the choices for the agency field
        form.recipient.choices = recipientChoices
        return form
