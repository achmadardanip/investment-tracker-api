from django.db.models import Sum, Avg, F
from django.utils import timezone
from .models import UserInvestment

class InvestmentService:
    def calculate_portfolio_performance(self, user):
        """Calculate overall portfolio ROI and other key metrics."""
        investments = UserInvestment.objects.filter(user=user, is_active=True)

        if not investments.exists():
            return {
                'total_invested': 0,
                'current_portfolio_value': 0,
                'total_profit_loss': 0,
                'overall_roi_percentage': 0,
            }

        aggregation = investments.aggregate(
            total_invested=Sum('amount_invested'),
            current_portfolio_value=Sum('current_value')
        )
        
        total_invested = aggregation['total_invested'] or 0
        current_portfolio_value = aggregation['current_portfolio_value'] or 0
        total_profit_loss = current_portfolio_value - total_invested

        if total_invested > 0:
            overall_roi_percentage = (total_profit_loss / total_invested) * 100
        else:
            overall_roi_percentage = 0

        return {
            'total_invested': total_invested,
            'current_portfolio_value': current_portfolio_value,
            'total_profit_loss': total_profit_loss,
            'overall_roi_percentage': round(overall_roi_percentage, 2),
        }

    def get_investment_insights(self, user):
        """Return insights like average holding period, preferred investment size."""
        investments = UserInvestment.objects.filter(user=user)
        
        if not investments.exists():
            return {
                'average_holding_period_days': 0,
                'preferred_investment_size': 0,
            }

        # Average Holding Period
        total_holding_days = 0
        now = timezone.now()
        for inv in investments:
            total_holding_days += (now - inv.purchase_date).days
        
        average_holding_period_days = total_holding_days / investments.count() if investments.exists() else 0

        # Preferred (Average) Investment Size
        preferred_investment_size = investments.aggregate(avg_size=Avg('amount_invested'))['avg_size'] or 0
        
        return {
            'average_holding_period_days': round(average_holding_period_days, 2),
            'preferred_investment_size': round(preferred_investment_size, 2)
        }

