from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync

class OrderProgress(WebsocketConsumer):
    def connect(self):
        from home.models import Order

        self.room_name = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f'order_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        order_details = Order.give_order_details(self.room_name)

        self.accept()

        self.send(text_data=json.dumps({
            'message': order_details
        }, default=str))

    def send_notification(self, event):
        self.send(text_data=json.dumps({
            'message': event['message']
        }))

    def disconnect(self, close_code):
        print("Disconnected:", close_code)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    