from mongoengine import Document, StringField, IntField, ReferenceField
import flask_mongoengine as mgo
from .Role import Role

class User(mgo.Document):
    name = StringField()
    googleid = StringField(unique=True)
    fname = StringField()
    lname = StringField()
    numtrans = IntField()
    email = StringField()
    student_id = StringField()
    wallet = IntField()
    reputation = IntField()
    image = StringField()
    gaveto = StringField()
    role = ReferenceField(Role)
