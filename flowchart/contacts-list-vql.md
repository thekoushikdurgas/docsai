# Flow sketch — Contacts list query (dashboard)

Text-only flow for alignment with `docs/docs/flowchart.json` diagrams.

```mermaid
flowchart LR
  subgraph ui [contact360.io_app]
    Sidebar[Sidebar filters\nfacets multi]
    Adv[Advanced_VQL_modal]
    Table[Contacts_table]
  end
  subgraph gw [contact360.io_api]
    GQL[GraphQL_POST]
    Conv[vql_converter]
  end
  subgraph sync [Connectra]
    FD[filters_data]
    VQL[POST_contacts]
  end
  Sidebar --> GQL
  Adv --> GQL
  GQL --> Conv
  GQL --> FD
  Conv --> VQL
  Table --> GQL
```

**Reference:** [`../docs/contacts-filter-vql-ui.md`](../docs/contacts-filter-vql-ui.md).
