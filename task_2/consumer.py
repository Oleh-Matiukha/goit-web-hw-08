import json
import os
import sys
import pika

from mongoengine import DoesNotExist

from models import Contact
from db import get_rabbitmq_connection


connection = get_rabbitmq_connection()
channel = connection.channel()


def send_email_stub(contact: Contact):
    print(f"Sending email to {contact.full_name} at {contact.email}.")

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='web_hw_08 queue', durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        contact_id = message.get('id')

        try:
            contact = Contact.objects.get(id=contact_id)
            send_email_stub(contact)

            contact.is_sent = True
            contact.save()

            print(f" [x] Email sent to {contact.email}, updated is_sent=True")

        except DoesNotExist:
            print(f" [!] Contact with id {contact_id} does not exist.")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='web_hw_08 queue', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
