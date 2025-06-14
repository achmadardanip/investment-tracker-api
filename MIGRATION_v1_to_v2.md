# Migration Guide: v1 to v2

This document outlines the steps required to upgrade an existing v1 database to the new v2 schema.

1. **Create Backup**
   - Backup your v1 database before applying migrations.

2. **Install new dependencies**
   - Install packages listed in `requirements.txt` including Channels, Celery and Graphene.

3. **Apply Django Migrations**
   - Run `python manage.py migrate` to apply the new migrations. This will create tables for currencies, wallets, yield payments and audit logs.

4. **Data Migration (optional)**
   - Map existing investment records to a default currency if none is specified.
   - Populate user wallets using available account information.

5. **Verify**
   - Run `python manage.py check` and ensure the application starts correctly.

After completing these steps the project will run with the v2 schema.
