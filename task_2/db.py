import configparser
import pika
from mongoengine import connect


config = configparser.ConfigParser()
config.read('config.ini')

# MongoDB
mongo_db = config.get('MONGODB', 'DB')
mongo_host = config.get('MONGODB', 'HOST')
mongo_port = config.getint('MONGODB', 'PORT')

connect(db=mongo_db, host=mongo_host, port=mongo_port)

# RabbitMQ
rabbitmq_user = config.get('RABBITMQ', 'USER')
rabbitmq_password = config.get('RABBITMQ', 'PASSWORD')
rabbitmq_host = config.get('RABBITMQ', 'HOST')
rabbitmq_port = config.getint('RABBITMQ', 'PORT')

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)

def get_rabbitmq_connection():
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbitmq_host,
            port=rabbitmq_port,
            credentials=credentials
        )
    )
