import os
import django
from apps.investments.services import YieldCalculationService

def setup_module(module):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

def test_yield_service():
    service = YieldCalculationService()
    service.calculate_daily_yields()
    assert True
