import os
import django
import pytest
from channels.testing import WebsocketCommunicator
from config.asgi import application

def setup_module(module):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

@pytest.mark.asyncio
async def test_websocket_connect():
    communicator = WebsocketCommunicator(application, "/ws/investments/")
    connected, _ = await communicator.connect()
    assert connected
    await communicator.disconnect()
