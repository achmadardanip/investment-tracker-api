# ----------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
import uuid

class UserInvestment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    asset_name = models.CharField(max_length=255)
    amount_invested = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_date = models.DateTimeField()
    current_value = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)

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
