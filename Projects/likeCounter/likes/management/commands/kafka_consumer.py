from django.core.management.base import BaseCommand
from confluent_kafka import Consumer
import os
import json
from collections import defaultdict
from django.db import transaction
from likes.models import Post


class Command(BaseCommand):
    help = 'Consume messages from Kafka'

    def process_batch(self, like_batch):
        with transaction.atomic():
            for post_id, like_count in like_batch.items():
                post = Post.objects.get(id=post_id)
                post.like += like_count
                post.save()
        # print(like_batch)

    def handle(self, *args, **options):
        print('***Kafka Consumer Started***')
        like_batch = defaultdict(int)
        consumer = Consumer({
            'bootstrap.servers': os.getenv('KAFKA_BROKER_URL', 'localhost:9092'),
            'group.id': 'location_group',
            'auto.offset.reset': 'earliest'
        })

        consumer.subscribe(['like_topic'])
        total_messages = 0

        try:
            while True:
                print('**Listening...**')
                msg = consumer.poll(timeout=1.0)

                if msg is None:
                    continue
                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue

                data = json.loads(msg.value().decode('utf-8'))
                print(data)
                post_id = data['post_id']
                like_batch[post_id] += 1
                total_messages += 1
                print(f'Total Messages: {total_messages}, Batch: {like_batch}')
                if total_messages >= 10: # It is batch processing, it will update the like only when total like count is gte 10.
                    self.process_batch(like_batch)
                    like_batch.clear()
                    total_messages = 0


                print(f"Received message: {msg.value().decode('utf-8')}")

        except KeyboardInterrupt:
            pass

        finally:
            consumer.close()