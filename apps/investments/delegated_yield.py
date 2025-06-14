from .models import YieldStrategy, Investment, YieldPayment
from django.utils import timezone
from decimal import Decimal

class DelegatedYieldService:
    """Distribute yields according to delegated strategies."""

    def process(self):
        for strategy in YieldStrategy.objects.filter(is_active=True):
            user_investments = Investment.objects.filter(user=strategy.user, is_active=True)
            for inv in user_investments:
                amount = inv.current_value * Decimal(inv.yield_rate) / Decimal('100')
                YieldPayment.objects.create(
                    investment=inv,
                    amount=amount,
                    currency=inv.currency,
                    payment_date=timezone.now(),
                    status='pending'
                )
