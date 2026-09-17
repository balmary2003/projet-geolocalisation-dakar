import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("tracking", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("tracking", self.channel_name)

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            "tracking",
            {
                "type": "send_location",
                "data": text_data
            }
        )

    async def send_location(self, event):
        await self.send(text_data=event["data"])
