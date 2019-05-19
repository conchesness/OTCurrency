from mongoengine import Document, StringField, ReferenceField, IntField, SortedListField, BooleanField, DateTimeField
from .User import User
from datetime import datetime

class Job(Document):
    requestedby = ReferenceField(User)
    claimedby = ReferenceField(User)
    title = StringField()
    desc = StringField()
    hours = IntField()
    createdatetime = DateTimeField()
