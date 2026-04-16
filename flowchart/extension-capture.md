# Extension capture flow (Contact360)

End-to-end path from the browser extension to Connectra via extension.server.

```mermaid
flowchart TD
  subgraph ext [contact360.extension]
    popup[Popup]
    panel[Side panel]
    sw[Service worker]
    cs[Content script LinkedIn]
  end
  subgraph gw [extension.server]
    health[GET /health]
    save[POST /v1/save-profiles]
    scrape[POST /v1/scrape]
  end
  subgraph sync [sync.server Connectra]
    bulk[POST /internal/extension/upsert-bulk]
  end
  popup --> sw
  panel --> sw
  sw --> cs
  sw --> health
  sw --> save
  sw --> scrape
  save --> bulk
  scrape --> bulk
```

- **Default path:** content script returns profile/company URL rows → `save-profiles` (client chunks large arrays).
- **Optional path:** user enables server HTML parse → capped `outerHTML` → `POST /v1/scrape` with `save: true` → parser extracts entities → same Connectra bulk upsert.

See also: [`docs/docs/architecture.json`](../docs/architecture.json) (`user_extension`), [`docs/backend/endpoints/extension.server/ROUTES.md`](../backend/endpoints/extension.server/ROUTES.md).
