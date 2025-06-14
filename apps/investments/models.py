# ----------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
import uuid


class Currency(models.Model):
    code = models.CharField(max_length=10)
    network = models.CharField(max_length=20)
    contract_address = models.CharField(max_length=255)
    decimal_places = models.IntegerField()

    def __str__(self):
        return self.code


class UserWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, unique=True)
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    locked_balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)

    def __str__(self):
        return f"{self.user.username} - {self.currency.code}"

class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    asset_name = models.CharField(max_length=255)
    amount_invested = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_date = models.DateTimeField()
    current_value = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True)
    yield_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    last_yield_payment = models.DateTimeField(null=True, blank=True)
    auto_compound = models.BooleanField(default=False)

    class Meta:
        db_table = 'investments_userinvestment'

    def __str__(self):
        return f"{self.user.username}'s investment in {self.asset_name}"

    @property
    def profit_loss(self):
        return self.current_value - self.amount_invested

    @property
    def profit_loss_percentage(self):
        if self.amount_invested == 0:
            return 0.0
        return (self.profit_loss / self.amount_invested) * 100

class TransactionLog(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('PURCHASE', 'Purchase'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} by {self.user.username}"


class YieldPayment(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    payment_date = models.DateTimeField()
    transaction_hash = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'pending'),
        ('processing', 'processing'),
        ('completed', 'completed'),
        ('failed', 'failed'),
    ])


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=50)
    resource_id = models.IntegerField()
    old_value = models.JSONField(null=True)
    new_value = models.JSONField(null=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class ExternalTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=[("pending","pending"), ("reconciled","reconciled"), ("mismatch","mismatch")], default="pending")
    transaction = models.ForeignKey(TransactionLog, null=True, blank=True, on_delete=models.SET_NULL)

class P2POrder(models.Model):
    ORDER_TYPES = (("BUY","BUY"),("SELL","SELL"))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=4, choices=ORDER_TYPES)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    is_filled = models.BooleanField(default=False)
    matched_order = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

class YieldStrategy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delegatee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="delegated_strategies")
    strategy_name = models.CharField(max_length=100)
    parameters = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

