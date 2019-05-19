from mongoengine import Document, StringField, IntField, ReferenceField

class User(Document):
    name = StringField(unique=True)
    email = StringField()
    student_id = StringField()
    wallet = IntField()
    reputation = IntField()
    image = StringField()
    googleid = StringField()
    gaveto = StringField()
