from .models import ExternalTransaction, TransactionLog

class ReconciliationService:
    """Match external transactions with internal logs."""

    def reconcile(self):
        for ext in ExternalTransaction.objects.filter(status='pending'):
            try:
                tx = TransactionLog.objects.get(reference_id=ext.external_id)
                ext.transaction = tx
                ext.status = 'reconciled'
                ext.save()
            except TransactionLog.DoesNotExist:
                ext.status = 'mismatch'
                ext.save()
