# campaign.server — deploy (Era 7)

- **Port:** **9800** (`CAMPAIGN_PORT`)
- **Git:** `https://github.com/thekoushikdurgas/campanign.server.git`
- **Docker:** [`EC2/campaign.server/Dockerfile`](../../../../EC2/campaign.server/Dockerfile), [`docker-compose.yml`](../../../../EC2/campaign.server/docker-compose.yml) (redis + api + worker)
- **Workflow:** [`.github/workflows/deploy-campaign-server.yml`](../../../../.github/workflows/deploy-campaign-server.yml)
- **Migrations:** `db/migrations/003_campaign_overhaul.sql` after baseline `001_init.sql`
