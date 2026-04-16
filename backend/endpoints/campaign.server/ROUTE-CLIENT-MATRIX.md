# campaign.server — gateway route matrix (Era 3)

| `CampaignServiceClient` method | HTTP |
|-------------------------------|------|
| `list_campaigns` | `GET /campaigns` |
| `create_campaign` | `POST /campaigns` |
| `pause_campaign` | `POST /campaigns/{id}/pause` |
| `resume_campaign` | `POST /campaigns/{id}/resume` |
| `delete_campaign` | `DELETE /campaigns/{id}` |
| `list_sequences` | `GET /sequences` |
| `create_sequence` | `POST /sequences` |
| `get_sequence` | `GET /sequences/{id}` |
| `pause_sequence` | `POST /sequences/{id}/pause` |
| `resume_sequence` | `POST /sequences/{id}/resume` |
| `delete_sequence` | `DELETE /sequences/{id}` |
| `add_sequence_step` | `POST /sequences/{id}/steps` |
| `update_sequence_step` | `PUT /sequences/{id}/steps/{step_id}` |
| `delete_sequence_step` | `DELETE /sequences/{id}/steps/{step_id}` |
| `trigger_sequence` | `POST /sequences/{id}/trigger` |
| `list_campaign_templates` | `GET /campaign-templates` |
| `get_campaign_template` | `GET /campaign-templates/{id}` |
| `create_campaign_template` | `POST /campaign-templates` |
| `update_campaign_template` | `PUT /campaign-templates/{id}` |
| `delete_campaign_template` | `DELETE /campaign-templates/{id}` |
