from mongoengine import Document, StringField, BooleanField, EmailField

class Contact(Document):
    full_name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    is_sent = BooleanField(default=False)
    meta = {'collection': 'contacts'}
