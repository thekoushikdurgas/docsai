# campaign.server — events boundary (Era 9)

- **Inbound:** HTTP only; **Asynq** tasks in Redis.
- **No Kafka** producers/consumers in this service.
- **No webhooks** outbound from campaign.server.
