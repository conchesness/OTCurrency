from mongoengine import Document, StringField, ReferenceField, IntField, SortedListField, BooleanField
from .User import User


class Transaction(Document):
    giver = ReferenceField(User)
    recipient = ReferenceField(User)
    amount = IntField()
    reason = StringField()
    category = StringField()
    upvote = IntField()
    downvote = IntField()
    voters = SortedListField(ReferenceField(User), ordering='name')
    thanks = BooleanField()
