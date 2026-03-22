import pika
import pandas as pd
import json
import uuid


def generateExcel(message):
    message = json.loads(message)
    df = pd.DataFrame(message)
    df.to_excel(f'OutputReport_{uuid.uuid4().hex[:8]}.xlsx', index=False)
    # print(type(message))
    # data = json.loads(message)
    # df = pandas.DataFrame(data)
    # df.to_csv('data.csv', index=False, encoding='utf-8')

def callback(ch, method, properties, body):
    message = body.decode()
    # print(message)
    generateExcel(message)
    # print(ch, method, properties, body)
    # print(" [x] Received %r" % body.decode())


params = pika.URLParameters('amqps://bjtgjtul:VMWqXcTJ5FRBB1FX5EKvWTPd04VFmLmZ@fuji.lmq.cloudamqp.com/bjtgjtul')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='my_queue')
channel.basic_consume(
    queue='my_queue',
    auto_ack=True,
    on_message_callback=callback)
print('Consumer Started...')
channel.start_consuming()
connection.close()
