import os
import django
from django.contrib.auth.models import User
from apps.investments.models import Currency, UserWallet

def setup_module(module):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

def test_create_wallet(db):
    user = User.objects.create_user('alice', password='pass')
    currency = Currency.objects.create(code='USDT', network='ERC20', contract_address='0x1', decimal_places=6)
    wallet = UserWallet.objects.create(user=user, currency=currency, address='0xtest', balance=0, locked_balance=0)
    assert wallet.address == '0xtest'
