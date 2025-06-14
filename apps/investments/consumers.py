from channels.generic.websocket import AsyncWebsocketConsumer

class InvestmentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive_json(self, content, **kwargs):
        # Placeholder for real-time commands
        pass
