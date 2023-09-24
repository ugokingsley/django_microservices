import pika, json

params = pika.URLParameters('amqps://lyirbsyn:7P4k5a0TEqwvS_vebvTnPNr66ecp_o1e@rat.rmq2.cloudamqp.com/lyirbsyn')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='payment', body=json.dumps(body), properties=properties)
