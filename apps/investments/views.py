from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F

from .models import Investment, TransactionLog
from .serializers import InvestmentSerializer, InvestmentSummarySerializer
from .services import InvestmentService

class InvestmentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the investments
        for the currently authenticated user.
        """
        user = self.request.user
        return Investment.objects.filter(user=user).order_by('-purchase_date')

    def perform_create(self, serializer):
        """
        Create a new investment and a corresponding transaction log.
        """
        investment = serializer.save(user=self.request.user)
        # Create a transaction log for the purchase
        TransactionLog.objects.create(
            user=self.request.user,
            transaction_type='PURCHASE',
            amount=investment.amount_invested
        )

class InvestmentSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        service = InvestmentService()
        
        # Get portfolio performance
        performance_data = service.calculate_portfolio_performance(user)
        
        # Get investment insights
        insights_data = service.get_investment_insights(user)
        
        investments = Investment.objects.filter(user=user, is_active=True)
        
        # Find best and worst performing investments
        best_investment = None
        worst_investment = None
        if investments.exists():
            # Order by the calculated profit/loss.
            # We can't use the property directly in order_by with all DBs,
            # so we use annotate.
            investments_with_pl = investments.annotate(pl=F('current_value') - F('amount_invested'))
            best_investment = investments_with_pl.order_by('-pl').first()
            worst_investment = investments_with_pl.order_by('pl').first()

        summary_data = {
            **performance_data,
            'active_investments_count': investments.count(),
            'best_performing_investment': InvestmentSerializer(best_investment).data if best_investment else None,
            'worst_performing_investment': InvestmentSerializer(worst_investment).data if worst_investment else None,
            'insights': insights_data
        }
        
        serializer = InvestmentSummarySerializer(data=summary_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)