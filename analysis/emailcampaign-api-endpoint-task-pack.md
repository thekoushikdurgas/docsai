# Email Campaign API Endpoint Task Pack (8.x)

## Contract
- GraphQL schema for `Campaign`, `Recipient`, `Template`, `Sequence`
- public REST contract `/v1/campaigns`
- webhook events: `campaign.created`, `campaign.completed`, `recipient.unsubscribed`

## Service
- GraphQL resolver module for create/get/list campaign operations
- webhook dispatcher with exponential backoff retry
- public API rate limit: 100 req/min per API key

## Data
- migrations for `webhook_subscriptions`
- migrations for `webhook_delivery_log`
- endpoint usage metrics by key/endpoint/version

## Ops
- completion gate checkboxes for schema, resolver, webhooks, metrics
