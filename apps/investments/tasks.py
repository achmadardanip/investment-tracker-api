from celery import shared_task

@shared_task
def process_yield_payments():
    """Run daily at 00:00 UTC and process yield payments."""
    pass

@shared_task
def update_currency_rates():
    """Update currency rates every 5 minutes."""
    pass

@shared_task
def generate_monthly_statements():
    """Generate PDF statements on the 1st of each month."""
    pass


@shared_task
def reconcile_external_transactions():
    from .services import ReconciliationService
    ReconciliationService().reconcile_pending()


@shared_task
def run_p2p_matching():
    from .services import MatchingEngineService
    MatchingEngineService().run()


@shared_task
def process_delegated_yields():
    from .services import DelegatedYieldServiceWrapper
    DelegatedYieldServiceWrapper().process()
