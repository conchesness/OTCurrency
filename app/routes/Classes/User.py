import flask_mongoengine as mgo
from mongoengine import Document, StringField, IntField


class User(mgo.Document):
    name = StringField(unique=True)
    email = StringField()
    student_id = StringField()
    wallet = IntField()
    reputation = IntField()
    image = StringField()
    googleid = StringField()
    gaveto = StringField()
