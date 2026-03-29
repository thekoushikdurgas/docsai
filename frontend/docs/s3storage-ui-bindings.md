# `s3storage` Frontend UX Surface Bindings (`0.x`-`10.x`)

## Primary UI surfaces using storage behavior

- `contact360.io/app` dashboard files/jobs flows (`files`, `jobs`, `email` surfaces)
- `contact360.io/root` marketing/storage narrative and product-explainer surfaces
- `contact360.io/admin` DocsAI/admin governance views for storage-linked docs and operations
- Billing/profile flows for proof and avatar related uploads
- Extension-origin flows (where storage-backed artifacts are surfaced)
- Campaign and integration surfaces in later eras

## Key UI components and hooks

- Components:
  - `FilesUploadModal`
  - `FilesUploadPanel`
  - `FilesCreateJobModal`
  - `FilesSchemaPanel`
  - `FilesColumnStatsPanel`
  - `DataPreviewTable`
  - `UpiPaymentModal`
- Hooks/services:
  - `useNewExport`
  - `useCsvUpload`
  - `useFilePreview`
  - `s3Service`
  - `jobsService`

## Era-driven UI small-task packs

- `1.x`: strengthen user/billing upload validation and user feedback.
- `2.x`: multipart progress, retry, and recovery UX for bulk flows.
- `3.x`: show ingestion-ready metadata and file lineage indicators.
- `4.x`: extension-origin upload and sync status visibility.
- `6.x`: reliability-focused retry/error patterns in file and jobs surfaces.
- `8.x`: API/integration-facing storage status and diagnostics affordances.
- `10.x`: campaign artifact upload/review/provenance UX.

## Root/App/Admin binding notes

- **`root`**: storage features are represented via product/feature storytelling and auth CTA handoff to dashboard operations.
- **`app`**: primary storage operations (multipart upload, preview/schema/stats, export artifacts, progress UI, checkbox/radio workflow controls).
- **`admin`**: governance and observability overlays for storage-related docs/endpoints/flows and release evidence.

## Flow references

- `docs/flowchart.md` (`s3storage` multipart and metadata flow)
- `docs/codebases/s3storage-codebase-analysis.md`

## 2026 addendum

- Multipart UI should explicitly represent initiate -> part upload -> complete -> metadata worker lifecycle.
- CSV analysis bindings must include schema/preview/stats surfaces for uploaded artifacts.
- Admin-side storage calls require auth-header parity with storage API hardening (`S3S-0.1`).
