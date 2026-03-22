from confluent_kafka import Producer
import json
import os

producer = Producer({
    'bootstrap.servers': os.getenv('KAFKA_BROKER_URL', 'localhost:9092')
})

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def send_like_event(post_id):
    message = {'post_id': post_id}
    producer.produce('like_topic', key=str(post_id), value=json.dumps(message).encode('utf-8'), callback=delivery_report)
    print('Sent to Kafka')
    producer.flush()