from django.contrib import admin
from .models import (
    Investment,
    TransactionLog,
    Currency,
    UserWallet,
    YieldPayment,
    AuditLog,
    ExternalTransaction,
    P2POrder,
    YieldStrategy,
)

admin.site.register(Investment)
admin.site.register(TransactionLog)
admin.site.register(Currency)
admin.site.register(UserWallet)
admin.site.register(YieldPayment)
admin.site.register(AuditLog)
admin.site.register(ExternalTransaction)
admin.site.register(P2POrder)
admin.site.register(YieldStrategy)
