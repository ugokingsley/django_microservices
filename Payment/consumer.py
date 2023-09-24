import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Payment.settings")
django.setup()

from paymentapp.models import *

params = pika.URLParameters('amqps://lyirbsyn:7P4k5a0TEqwvS_vebvTnPNr66ecp_o1e@rat.rmq2.cloudamqp.com/lyirbsyn')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='userauth')


def callback(ch, method, properties, body):
    print('Received in UserAuth')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'user_token':
        instance = UserToken(user_id=data['id'], user_email=data['email'], user_token=data['token'])
        instance.save()
        print('User Token Created for Payment')


channel.basic_consume(queue='userauth', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
