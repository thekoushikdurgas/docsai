# Pipelines

## Contact / company CRUD

UI → GraphQL `contacts` / `companies` → `ConnectraClient` → sync.server.

## Email / phone enrichment

UI → GraphQL `email` or `phone` → respective satellite → optional Connectra upsert.

## AI chat

UI → `aiChats.sendMessage` → `AIServerClient.send_message` (non-streaming). For token streaming, the **client** exposes `send_message_stream` (SSE over HTTP); GraphQL mutation uses the JSON response path today.

## Campaigns

UI → `campaignSatellite` / `campaigns` mutations → `CampaignServiceClient` → campaign.server.

## Logs (admin)

Admin GraphQL `admin.logs` / `searchLogs` → `LogsServerClient` when configured.
