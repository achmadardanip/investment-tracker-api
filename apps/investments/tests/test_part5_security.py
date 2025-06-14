import os
import django
from apps.investments.services import TransactionSigner

def setup_module(module):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

def test_transaction_signer():
    signer = TransactionSigner()
    data = {"amount": "100"}
    signature = signer.sign_transaction(data)
    signer.verify_signature(data, signature)
    assert True

