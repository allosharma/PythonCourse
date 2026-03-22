from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MainConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are connected'
        }))

    async def receive(self, text_data):
        print("Received in terminal:", text_data)

        try:
            data = json.loads(text_data)
            message = data.get("message")
        except:
            message = text_data   # fallback if plain text

        await self.send(text_data=json.dumps({
            "message": f"Echo: {message}"
        }))
        
    async def disconnect(self, close_code):
        
        pass