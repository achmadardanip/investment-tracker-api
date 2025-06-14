from rest_framework import serializers
from .models import Investment, TransactionLog, Currency, UserWallet, YieldPayment
from decimal import Decimal

class InvestmentSerializer(serializers.ModelSerializer):
    profit_loss = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    profit_loss_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = Investment
        fields = [
            'id', 'asset_name', 'amount_invested', 'purchase_date',
            'current_value', 'is_active', 'currency',
            'yield_rate', 'auto_compound',
            'profit_loss', 'profit_loss_percentage'
        ]
        read_only_fields = ['id', 'is_active']
    
    def validate_amount_invested(self, value):
        """
        Check that the investment is at least $1000.
        """
        if value < Decimal('1000.00'):
            raise serializers.ValidationError("Minimum investment amount is $1000.")
        return value

class InvestmentSummarySerializer(serializers.Serializer):
    # This serializer is for representing the summary data structure, not for a model
    total_invested = serializers.DecimalField(max_digits=15, decimal_places=2)
    current_portfolio_value = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_profit_loss = serializers.DecimalField(max_digits=15, decimal_places=2)
    overall_roi_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    active_investments_count = serializers.IntegerField()
    best_performing_investment = InvestmentSerializer(required=False)
    worst_performing_investment = InvestmentSerializer(required=False)
    insights = serializers.DictField(child=serializers.FloatField())

