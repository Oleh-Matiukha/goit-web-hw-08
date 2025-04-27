import configparser

from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE


config = configparser.ConfigParser()
config.read('config.ini')

connect(
    db=config['database']['db'],
    username=config['database']['username'],
    password=config['database']['password'],
    host=config['database']['host'],
    tls=config.getboolean('database', 'tls'),
    retryWrites=config.getboolean('database', 'retryWrites'),
    w=config['database']['w'],
    appName=config['database']['appName']
)


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=15))
    quote = StringField()
    meta = {"collection": "quotes"}
