from django.contrib import admin
from .models import UserInvestment, TransactionLog

admin.site.register(UserInvestment)
admin.site.register(TransactionLog)