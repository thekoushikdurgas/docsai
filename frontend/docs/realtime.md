# Realtime patterns (frontend)

## AI chat

- **Default:** GraphQL mutations for send/receive; markdown rendering on the client.
- **Optional streaming:** Server-Sent Events may be used by the gateway for token streams — contract and boundaries are documented in `docs/backend/endpoints/contact360.io/EVENTS-BOUNDARY.md`.

## Campaigns / jobs

- **Polling:** Job status (exports, bulk email/phone) uses polling hooks such as `useJobPoller` against gateway GraphQL job fields.

## WebSockets

- Reserved for future collaborative editing; not required for current dashboard flows.
