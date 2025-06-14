# Investment Tracker v2 Architecture

This document outlines the high level architecture changes introduced in v2.

## Overview

* Added multi-currency support via `Currency` and `UserWallet` models.
* Extended `Investment` model with yield information and currency reference.
* Introduced `YieldPayment` and `AuditLog` for payout tracking and auditing.
* Real-time updates implemented with Django Channels and WebSockets.
* GraphQL API added alongside existing REST endpoints.
* Background tasks managed via Celery.
* Caching layers and signing services are stubbed for future expansion.

The system is designed to scale to 1M users using Redis for caching and Celery
for background task processing. Channels provides websocket support for live
portfolio updates.

## v3 Additions

* Smart contract integration service for on-chain settlements.
* Machine learning module for fraud detection.
* Reconciliation service matching external transactions with internal logs.
* Simple P2P order matching engine.
* Delegated yield strategies allowing yield distribution to delegatees.
