Common API endpoints for batch operations, file uploads, and shared functionality.

**Endpoints**:
- **Batch Upsert**: `POST /common/batch-upsert` - Insert/update companies and contacts from CSV-like data
- **Upload URL**: `GET /common/upload-url` - Generate presigned S3 URL for file uploads

**Note**: Filter endpoints (`GET /common/:service/filters`, `POST /common/:service/filters/data`) are included in the Companies and Contacts sections. Job endpoints (`POST /common/jobs`, `POST /common/jobs/create`) are in the Jobs section.