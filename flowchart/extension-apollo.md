# Extension Apollo capture flow

End-to-end path for the **Apollo** side panel tab: optional client-side DOM parse, optional server HTML parse, CSV download, optional CRM save.

```mermaid
flowchart TD
  subgraph ext [contact360.extension]
    apolloTab[ApolloPage]
    sw[Service worker runApolloCapture]
    cs[Content script C360_SCRAPE_APOLLO]
    csv[chrome.downloads CSV]
  end
  subgraph api [contact360.io/api]
    gql["POST /graphql scrapeApolloHtml saveApolloProfiles"]
  end
  subgraph sat [extension.server]
    apollo[POST /v1/apollo-scrape]
    save[POST /v1/save-profiles]
  end
  subgraph sync [sync.server]
    comp[POST /companies/batch-upsert]
    cont[POST /contacts/batch-upsert]
  end
  apolloTab --> sw
  sw --> cs
  cs -->|"contacts companies rows"| apolloTab
  apolloTab --> csv
  sw -->|"JWT if server parse or save"| gql
  gql --> apollo
  gql --> save
  apollo -->|"optional save true"| save
  save --> comp --> cont
```

- **Offline reference:** [`docs/scripts/apollo_html/main.py`](../scripts/apollo_html/main.py) — same CSV field lists and UUID5 rules.
- **Contracts:** [`DECISIONS.md`](../DECISIONS.md) § Sales Navigator / extension satellite.

See also: [`extension-capture.md`](extension-capture.md).
