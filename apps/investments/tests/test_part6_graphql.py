import os
import django
import json
from django.test import Client


def setup_module(module):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()


def test_graphql_portfolio():
    client = Client()
    query = '{ portfolio(userId: 1) { id } }'
    response = client.post('/graphql/', data=json.dumps({'query': query}), content_type='application/json')
    assert response.status_code in [200, 401]
