# Extension capture flow (Contact360)

End-to-end path from the browser extension to Connectra: **GraphQL gateway** → **extension.server** → **sync.server**.

```mermaid
flowchart TD
  subgraph ext [contact360.extension]
    panel[Side panel]
    sw[Service worker]
    cs[Content script LinkedIn]
  end
  subgraph api [contact360.io/api]
    gql[POST /graphql]
    healthApi[GET /health]
  end
  subgraph sat [extension.server]
    save[POST /v1/save-profiles]
    scrape[POST /v1/scrape]
  end
  subgraph sync [sync.server Connectra]
    bulk[POST /internal/extension/upsert-bulk]
  end
  panel --> sw
  sw --> cs
  sw --> healthApi
  sw -->|"JWT saveSalesNavigatorProfiles"| gql
  sw -->|"JWT scrapeSalesNavigatorHtml"| gql
  gql --> save
  gql --> scrape
  save --> bulk
  scrape --> bulk
```

- **Default path:** content script collects profile/company **links** from the DOM → GraphQL `saveSalesNavigatorProfiles` → gateway → `save-profiles` (chunks up to 1000 profiles).
- **Optional path (Sales Navigator pages only):** user enables server HTML parse → capped `outerHTML` → GraphQL `scrapeSalesNavigatorHtml` → gateway → `POST /v1/scrape` with `save: true` → SN-oriented parser → same Connectra bulk upsert. Public `linkedin.com/search/` and `/in/` use link extraction + save mutation only (not the SN HTML parser).

See also: [`docs/backend/endpoints/extension.server/ROUTES.md`](../backend/endpoints/extension.server/ROUTES.md).
