from mongoengine import Document, DateTimeField, StringField, ReferenceField, ListField
from .User import User
from datetime import datetime

class Event(Document):
    owner = ReferenceField(User)
    participants = ListField(ReferenceField(User))
    related = StringField() # Contains the exact name of a data collection that holds a related record.  ie Job
    datetime = DateTimeField()
    title = StringField()
    desc = StringField()
    place = StringField()
    contacttype = StringField()
