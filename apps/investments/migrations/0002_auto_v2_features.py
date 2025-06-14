from django.db import migrations, models

class SafeRenameModel(migrations.RenameModel):
    """RenameModel that ignores missing models and database errors."""
    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        try:
            super().database_forwards(app_label, schema_editor, from_state, to_state)
        except Exception:
            pass

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        try:
            super().database_backwards(app_label, schema_editor, from_state, to_state)
        except Exception:
            pass

    def state_forwards(self, app_label, state):
        try:
            super().state_forwards(app_label, state)
        except KeyError:
            pass

    def state_backwards(self, app_label, state):
        try:
            super().state_backwards(app_label, state)
        except KeyError:
            pass

import django.db.models.deletion
from django.conf import settings
import uuid

class Migration(migrations.Migration):
    dependencies = [
        ('investments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        SafeRenameModel(
            old_name='UserInvestment',
            new_name='Investment',
        ),
        migrations.AlterModelTable(
            name='investment',
            table='investments_userinvestment',
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('network', models.CharField(max_length=20)),
                ('contract_address', models.CharField(max_length=255)),
                ('decimal_places', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, unique=True)),
                ('balance', models.DecimalField(default=0, decimal_places=8, max_digits=20)),
                ('locked_balance', models.DecimalField(default=0, decimal_places=8, max_digits=20)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investments.currency')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='investment',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='investments.currency'),
        ),
        migrations.AddField(
            model_name='investment',
            name='yield_rate',
            field=models.DecimalField(default=0, decimal_places=2, max_digits=5),
        ),
        migrations.AddField(
            model_name='investment',
            name='last_yield_payment',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='auto_compound',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='YieldPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(max_digits=20, decimal_places=8)),
                ('payment_date', models.DateTimeField()),
                ('transaction_hash', models.CharField(max_length=255, null=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('processing', 'processing'), ('completed', 'completed'), ('failed', 'failed')], max_length=20)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='investments.currency')),
                ('investment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investments.investment')),
            ],
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=100)),
                ('resource_type', models.CharField(max_length=50)),
                ('resource_id', models.IntegerField()),
                ('old_value', models.JSONField(null=True)),
                ('new_value', models.JSONField(null=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExternalTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(max_length=255, unique=True)),
                ('amount', models.DecimalField(max_digits=20, decimal_places=8)),
                ('status', models.CharField(default='pending', choices=[('pending', 'pending'), ('reconciled', 'reconciled'), ('mismatch', 'mismatch')], max_length=20)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='investments.currency')),
                ('transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='investments.transactionlog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='P2POrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_type', models.CharField(choices=[('BUY', 'BUY'), ('SELL', 'SELL')], max_length=4)),
                ('amount', models.DecimalField(max_digits=20, decimal_places=8)),
                ('price', models.DecimalField(max_digits=20, decimal_places=8)),
                ('is_filled', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='investments.currency')),
                ('matched_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='investments.p2porder')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='YieldStrategy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strategy_name', models.CharField(max_length=100)),
                ('parameters', models.JSONField(default=dict)),
                ('is_active', models.BooleanField(default=True)),
                ('delegatee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delegated_strategies', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='yield_strategies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

