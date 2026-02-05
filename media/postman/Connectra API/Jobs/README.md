Jobs API endpoints for asynchronous background job processing. Supports CSV import/export with S3 integration, automatic retries, and distributed processing.

**Features**:
- **Asynchronous Processing**: Jobs are queued and processed in the background
- **Distributed Processing**: Multiple workers can process jobs concurrently
- **Automatic Retries**: Failed jobs can be automatically retried with configurable intervals
- **Memory Efficient**: Streaming CSV processing for large files (multi-GB support)
- **State Management**: Complete job lifecycle tracking with status updates

**Job Types**:
1. **Insert CSV File** (`insert_csv_file`): Import CSV data from S3 into PostgreSQL and Elasticsearch
2. **Export CSV File** (`export_csv_file`): Export filtered contact/company data to S3 as CSV

**Job States**:
- `open` → `in_queue` → `processing` → `completed` (or `failed` → `retry_in_queued` → `processing`)

**See**: [Jobs API Guide](../../docs/filters/jobs.md) | [API Reference](../../docs/filters/06-api-reference.md#jobs-endpoints)