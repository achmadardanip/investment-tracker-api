import os
import django
from apps.investments.matching import MatchingEngine
from apps.investments.fraud_detection import FraudDetector
from apps.investments.delegated_yield import DelegatedYieldService


def setup_module(module):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()


def test_matching_engine():
    engine = MatchingEngine()
    engine.match()
    assert True


def test_fraud_detector_training():
    detector = FraudDetector()
    accuracy = detector.train_from_csv('data/creditcard_sample.csv')
    assert 0 <= accuracy <= 1


def test_delegated_yield_service():
    service = DelegatedYieldService()
    service.process()
    assert True
