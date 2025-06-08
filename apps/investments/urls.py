from django.urls import path
from .views import InvestmentListCreateAPIView, InvestmentSummaryAPIView

urlpatterns = [
    path('', InvestmentListCreateAPIView.as_view(), name='investment-list-create'),
    path('summary/', InvestmentSummaryAPIView.as_view(), name='investment-summary'),
]