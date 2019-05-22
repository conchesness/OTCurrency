from mongoengine import Document, StringField, IntField, ReferenceField
import flask_mongoengine as mgo

class Role(mgo.Document):
    name = StringField()
    desc = StringField()
