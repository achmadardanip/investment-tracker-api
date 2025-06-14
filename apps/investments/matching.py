from django.db import transaction
from .models import P2POrder

class MatchingEngine:
    """Simple order matching engine."""

    def match(self):
        with transaction.atomic():
            buy_orders = P2POrder.objects.filter(order_type='BUY', is_filled=False).order_by('created_at')
            sell_orders = P2POrder.objects.filter(order_type='SELL', is_filled=False).order_by('created_at')
            for buy in buy_orders:
                for sell in sell_orders:
                    if sell.is_filled or buy.is_filled:
                        continue
                    if sell.price <= buy.price and sell.currency == buy.currency:
                        buy.is_filled = True
                        sell.is_filled = True
                        buy.matched_order = sell
                        sell.matched_order = buy
                        buy.save()
                        sell.save()
                        break
