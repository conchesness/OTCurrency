from mongoengine import Document, StringField, ReferenceField, IntField, SortedListField, BooleanField, DateTimeField
from .User import User
from .Event import Event
from datetime import datetime

class Job(Document):
    requestedby = ReferenceField(User)
    claimedby = ReferenceField(User)
    event = ReferenceField(Event)
    category = StringField()
    title = StringField()
    desc = StringField()
    difficulty = StringField()
    createdatetime = DateTimeField()
