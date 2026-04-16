# Satellite parity (gateway)

| Satellite | GraphQL surface | Client | Notes |
|-----------|-----------------|--------|--------|
| sync.server | contacts, companies, jobs | ConnectraClient | VQL |
| email.server | `email` | EmailServerClient | |
| phone.server | **`phone`** | PhoneServerClient | Era 0–11 adds GraphQL module |
| ai.server | `aiChats` | AIServerClient | |
| s3storage.server | `s3`, `upload` | S3StorageEC2Client | |
| log.server | `admin` logs | LogsServerClient | |
| extension.server | `salesNavigator` | SalesNavigatorServerClient | |
| campaign.server | `campaignSatellite`, `campaigns` | CampaignServiceClient | CQL + preview wired in queries |
