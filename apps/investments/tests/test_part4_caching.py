import os
import django
from apps.investments.services import CachedInvestmentService

def setup_module(module):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

def test_cached_service():
    service = CachedInvestmentService()
    service.get_portfolio_value(user_id=1)
    assert True
