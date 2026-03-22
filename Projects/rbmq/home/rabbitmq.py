import pika
import json

def public_message(message):
    params = pika.URLParameters('amqps://bjtgjtul:VMWqXcTJ5FRBB1FX5EKvWTPd04VFmLmZ@fuji.lmq.cloudamqp.com/bjtgjtul')
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='my_queue')
    message = json.dumps(message).encode() # the reason we are using encode is to convert the message into bytes which will help us to send the message to the queue. Without this, we will get an error.
    channel.basic_publish(
        exchange='',
        routing_key='my_queue',
        body=message)
    print(" [x] Sent %r" % message)
    connection.close()