# emailapis UI bindings

## Purpose
Map `lambda/emailapis` and `lambda/emailapigo` to dashboard surfaces including pages, tabs, buttons, inputs, components, hooks, contexts, and data-flow/graph elements.

## Binding matrix
| Era | Pages/tabs | Components | Inputs/controls | Hooks/services/contexts |
| --- | --- | --- | --- | --- |
| `0.x` | root landing shell + dashboard base email placeholders + admin docs shell | `Button3D`, `Input3D`, `MainLayout`, admin base template blocks | baseline CTA/input states | root/app auth+theme contexts; admin auth/session context |
| `1.x` | billing/profile impact zones | credit banners, alerts | submit buttons, validation inputs | `RoleContext`, billing/usage services |
| `2.x` | email finder/verifier tabs | `EmailFinderSingle`, `EmailVerifierSingle`, `EmailMappingModal`, `EmailBulkDropZone` | first/last/domain inputs, email input, progress bars, mapping checkboxes, retry radio buttons | `useEmailFinderSingle`, `useEmailVerifierSingle`, `useEmailVerifierBulk`, `useCsvUpload`, `emailService.ts`, `AuthContext`, `RoleContext` |
| `3.x` | contact/company pages with email enrichment | contact/company rows + detail cards | filter inputs, row checkboxes, export controls | contact/company hooks + email service bridge |
| `4.x` | extension/SN touchpoints | extension status + ingestion panels | sync toggles, retry controls | extension clients + email endpoints |
| `5.x` | assistant tab | `EmailAssistantPanel` + result cards | text area, action buttons | AI hooks + email verification services |
| `6.x` | reliability views | job cards, execution flow, error banners | retry buttons, progress bars, health toggles | jobs polling hooks + observability services |
| `7.x` | admin/governance tabs | audit panels, diagnostics cards | date filters, checkbox/radio filters | role-gated admin hooks/services |
| `8.x` | API/integrations tabs | API usage panels | endpoint filters, key selectors | integration services + GraphQL bridge |
| `9.x` | ecosystem/productization tabs | connector configuration cards | entitlement toggles, plan controls | profile/integration contexts |
| `10.x` | campaign flows | campaign send + compliance components | audience selectors, approval checkboxes, progress indicators | campaign services + verifier integration |

## Surface-specific bindings

- **`contact360.io/root`**: email-system messaging and product pages bind to marketing services and route authenticated actions to dashboard email workflows.
- **`contact360.io/app`**: primary finder/verifier operational UI (single + bulk), progress bars, checkbox/radio mapping and retry controls.
- **`contact360.io/admin`**: endpoint/docs governance, status visibility, and graph-linked docs administration for email-related modules.

## End-to-end binding graph

`UI component -> Hook -> GraphQL emailService -> Appointment360 email resolvers -> LambdaEmailClient -> emailapis/emailapigo -> provider clients -> cache/pattern tables`

## 2026 addendum

- UI status rendering must stay aligned with canonical email status vocabulary and fallback-chain semantics.
- Bulk finder/verifier flows should expose polling/retry and replay-safe progress states.
