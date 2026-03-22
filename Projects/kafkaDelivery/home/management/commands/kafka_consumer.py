import sys

from django.core.management.base import BaseCommand
from confluent_kafka import Consumer, KafkaError, KafkaException
import json
from home.models import LocationUpdate
import os

class Command(BaseCommand):
    help = 'Consume location updates from Kafka'

    def handle(self, *args, **options):
        consumer = Consumer({
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'location-updates-consumer',
            'auto.offset.reset': 'earliest',
        })
        consumer.subscribe(['location_updates'])

        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(msg.error())
                        break
                data = json.loads(msg.value().decode('utf-8'))
                LocationUpdate.objects.create(
                    latitude=data['latitude'][0] if isinstance(data['latitude'], list) else data['latitude'],
                    longitude=data['longitude'][0] if isinstance(data['longitude'], list) else data['longitude'],
                )
                print(f'Received location update: {data}')
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()