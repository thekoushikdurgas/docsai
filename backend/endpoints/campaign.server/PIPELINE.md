# campaign.server — pipeline (Era 4)

1. **Create campaign** (`POST /campaigns`) → row in `campaigns` → Asynq task by `channel` (`campaign:email` | `phone` | `linkedin` | legacy `campaign:send`).
2. **Worker** loads CSV recipients, inserts `recipients`, runs SMTP send (email) or stub (phone/LinkedIn).
3. **Sequence trigger** (`POST /sequences/:id/trigger`) → Connectra contact → recipient row → `campaign:sequence_step` → single SMTP send.
