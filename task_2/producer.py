import pika
import json

from faker import Faker

from db import get_rabbitmq_connection
from models import Contact


connection = get_rabbitmq_connection()
channel = connection.channel()

channel.exchange_declare(exchange='Web_hw_08 exchange', exchange_type='direct')
channel.queue_declare(queue='web_hw_08 queue', durable=True)
channel.queue_bind(exchange='Web_hw_08 exchange', queue='web_hw_08 queue')

fake = Faker('uk-UA')

def create_contacts_and_publish(count: int):
    for _ in range(count):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email()
        ).save()

        message = {
            'id': str(contact.id)
        }


        channel.basic_publish(
            exchange='Web_hw_08 exchange',
            routing_key='web_hw_08 queue',
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

    connection.close()

if __name__ == "__main__":
    create_contacts_and_publish(10)
