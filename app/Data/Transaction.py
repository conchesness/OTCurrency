from mongoengine import Document, StringField, ReferenceField, IntField, SortedListField, BooleanField, DateTimeField
import mongoengine as mgo
from datetime import datetime
from .User import User


class Transaction(mgo.Document):
    giver = ReferenceField(User)
    recipient = ReferenceField(User)
    amount = mgo.IntField(required='true')
    reason = StringField()
    category = StringField()
    upvote = IntField()
    downvote = IntField()
    voters = SortedListField(ReferenceField(User), ordering='name')
    thanks = BooleanField()
    # createdate = DateTimeField(default=datetime.now())
    createdate = DateTimeField()
    meta = {
        'ordering': ['+createdate']
    }
