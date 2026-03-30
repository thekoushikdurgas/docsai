#!/usr/bin/env python3
"""
Generate Connectra GraphQL Postman collection from Connectra REST structure.
Run: python generate_connectra_graphql.py
Output: Connectra_GraphQL_API.postman_collection.json
"""
import json
import os

COLLECTION_ID = "connectra-graphql-via-appointment360"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "{{baseUrl}}/graphql"
HEADERS = [
    {"key": "Content-Type", "value": "application/json"},
    {"key": "Authorization", "value": "Bearer {{accessToken}}"},
]
HEADERS_NO_AUTH = [{"key": "Content-Type", "value": "application/json"}]


def req(name, body, desc="", headers=None):
    return {
        "name": name,
        "request": {
            "method": "POST",
            "header": headers or HEADERS,
            "body": {"mode": "raw", "raw": body},
            "url": {"raw": BASE_URL, "host": ["{{baseUrl}}"], "path": ["graphql"]},
            "description": desc or f"REST→GraphQL: {name}",
        },
    }


def gql_query(op_name, query_str, variables):
    return json.dumps({"query": query_str, "variables": variables})


# --- Auth ---
auth_login = req(
    "Login",
    gql_query(
        "Login",
        "mutation Login($input:LoginInput!){ auth{ login(input:$input){ accessToken refreshToken user{ uuid email name}}}}",
        {"input": {"email": "{{email}}", "password": "{{password}}"}},
    ),
    "REST Connectra uses X-API-Key; Appointment360 uses JWT. Run first.",
    HEADERS_NO_AUTH,
)
auth_login["event"] = [
    {
        "listen": "test",
        "script": {
            "exec": [
                "if (pm.response.code === 200){",
                "const d = pm.response.json();",
                "const r = d.data?.auth?.login;",
                "if (r){ if(r.accessToken) pm.environment.set('accessToken',r.accessToken); if(r.refreshToken) pm.environment.set('refreshToken',r.refreshToken); if(r.user?.uuid) pm.environment.set('userId',r.user.uuid); }",
                "}",
            ],
            "type": "text/javascript",
        },
    }
]

# --- System ---
health = req(
    "Health Check",
    gql_query("Health", "query{ health{ apiHealth{ status environment}}}", {}),
    "REST: GET /health → GraphQL: health.apiHealth",
    HEADERS_NO_AUTH,
)

# --- Load filter data from JSON (avoids Python parser issue with deeply nested inline dicts) ---
with open(os.path.join(SCRIPT_DIR, "filters_data.json"), encoding="utf-8") as f:
    _filters_data = json.load(f)
company_filters = [tuple(x) for x in _filters_data["company_filters"]]
company_use_cases = [tuple(x) for x in _filters_data["company_use_cases"]]
contact_filters = [tuple(x) for x in _filters_data["contact_filters"]]
contact_use_cases = [tuple(x) for x in _filters_data["contact_use_cases"]]


def make_company_query(name, q):
    body = gql_query("CompanyQuery", "query($query:VQLQueryInput!){ companies{ companyQuery(query:$query){ items{ uuid name industries employeesCount annualRevenue totalFunding city country website} total limit offset}}}", {"query": q})
    return req(name, body, f"REST: POST /companies/ → GraphQL: companies.companyQuery. {name}")


def make_contact_query(name, q):
    body = gql_query("ContactQuery", "query($query:VQLQueryInput!){ contacts{ contactQuery(query:$query){ items{ uuid firstName lastName email title departments seniority emailStatus} total limit offset}}}", {"query": q})
    return req(name, body, f"REST: POST /contacts/ → GraphQL: contacts.contactQuery. {name}")


def build_collection():
    items = []

    # Auth
    items.append({"name": "Auth", "item": [auth_login]})

    # System
    items.append({"name": "System", "item": [health]})

    # CRUD Operations
    items.append({
        "name": "CRUD Operations",
        "item": [
            {
                "name": "Contacts",
                "item": [
                    req("CREATE: POST /contacts/batch-upsert (UPSERT)", gql_query("BatchCreateContacts", "mutation BatchCreateContacts($input:BatchCreateContactsInput!){ contacts{ batchCreateContacts(input:$input){ uuid firstName lastName email}}}", {"input": {"contacts": [{"firstName": "John", "lastName": "Doe", "email": "john.doe@acme.com", "companyUuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890", "title": "Senior Software Engineer", "departments": ["Engineering"], "seniority": "senior"}]}}), "REST: POST /contacts/batch-upsert → GraphQL: contacts.batchCreateContacts"),
                    req("READ: POST /contacts/ (VQL filter query)", gql_query("ContactQuery", "query ContactQuery($query:VQLQueryInput!){ contacts{ contactQuery(query:$query){ items{ uuid firstName lastName email title} total limit offset}}}", {"query": {"filters": {"conditions": [{"field": "country", "operator": "in", "value": ["united states"]}, {"field": "seniority", "operator": "eq", "value": "senior"}]}, "selectColumns": ["uuid", "first_name", "last_name", "email", "title"], "limit": 25}}), "REST: POST /contacts/ with VQL → GraphQL: contacts.contactQuery"),
                    req("UPDATE: POST /contacts/batch-upsert (UPSERT by UUID)", gql_query("UpdateContact", "mutation UpdateContact($uuid:ID!,$input:UpdateContactInput!){ contacts{ updateContact(uuid:$uuid,input:$input){ uuid firstName lastName email title}}}", {"uuid": "{{contactUuid}}", "input": {"firstName": "John", "lastName": "Doe", "email": "john.doe@acme.com", "title": "Senior Engineering Manager", "departments": ["Engineering", "Product"], "seniority": "lead"}}), "REST: POST /contacts/batch-upsert with uuid → GraphQL: contacts.updateContact(uuid, input)"),
                ],
            },
            {
                "name": "Companies",
                "item": [
                    req("CREATE: POST /companies/batch-upsert (UPSERT)", gql_query("CreateCompany", "mutation CreateCompany($input:CreateCompanyInput!){ companies{ createCompany(input:$input){ uuid name industries employeesCount website}}}", {"input": {"name": "Acme Corporation", "employeesCount": 500, "industries": ["Technology", "Software"], "keywords": ["SaaS", "B2B", "Enterprise"]}}), "REST: POST /companies/batch-upsert → GraphQL: companies.createCompany"),
                    req("READ: POST /companies/ (VQL filter query)", gql_query("CompanyQuery", "query CompanyQuery($query:VQLQueryInput!){ companies{ companyQuery(query:$query){ items{ uuid name industries employeesCount website} total limit offset}}}", {"query": {"filters": {"conditions": [{"field": "country", "operator": "in", "value": ["united states"]}, {"field": "industries", "operator": "in", "value": ["Technology"]}, {"field": "employees_count", "operator": "gte", "value": 100}, {"field": "employees_count", "operator": "lte", "value": 5000}]}, "selectColumns": ["uuid", "name", "industries", "employees_count", "website"], "limit": 25}}), "REST: POST /companies/ with VQL → GraphQL: companies.companyQuery"),
                    req("UPDATE: POST /companies/batch-upsert (UPSERT by UUID)", gql_query("UpdateCompany", "mutation UpdateCompany($uuid:ID!,$input:UpdateCompanyInput!){ companies{ updateCompany(uuid:$uuid,input:$input){ uuid name industries employeesCount}}}", {"uuid": "{{companyUuid}}", "input": {"name": "Acme Corporation", "employeesCount": 750, "industries": ["Technology", "Software", "AI"]}}), "REST: POST /companies/batch-upsert with uuid → GraphQL: companies.updateCompany(uuid, input)"),
                ],
            },
        ],
    })

    # Companies folder
    company_filter_items = [make_company_query(n, q) for n, q in company_filters]
    company_use_case_items = [make_company_query(n, q) for n, q in company_use_cases]
    items.append({
        "name": "Companies",
        "item": [
            {"name": "Filter Examples", "item": company_filter_items},
            {"name": "Use Cases", "item": company_use_case_items},
            req("Get Companies Count", gql_query("CompanyCount", "query($query:VQLQueryInput){ companies{ companyCount(query:$query)}}", {"query": {"filters": {"conditions": [{"field": "industries", "operator": "in", "value": ["Technology"]}, {"field": "country", "operator": "in", "value": ["united states"]}]}}}), "REST: POST /companies/count → GraphQL: companies.companyCount"),
            req("Get Filters", gql_query("CompanyFilters", "query{ companies{ filters{ items{ filterKey filterType} total}}}", {}), "REST: GET /common/companies/filters → GraphQL: companies.filters"),
            req("Get Filter Data", gql_query("CompanyFilterData", "query($input:CompanyFilterDataInput!){ companies{ filterData(input:$input){ items{ value count} total}}}", {"input": {"filterKey": "industries", "searchText": "", "page": 1, "limit": 100}}), "REST: POST /common/companies/filters/data → GraphQL: companies.filterData(input)"),
            req("Batch Upsert Companies", gql_query("CreateCompany", "mutation($input:CreateCompanyInput!){ companies{ createCompany(input:$input){ uuid name industries employeesCount}}}", {"input": {"name": "Acme Corporation", "employeesCount": 500, "industries": ["Technology", "Software"], "keywords": ["SaaS", "B2B"], "address": "123 Main St", "annualRevenue": 50000000, "technologies": ["React", "Node.js", "AWS"]}}), "REST: POST /companies/batch-upsert → GraphQL: companies.createCompany (no batch; call per company)"),
        ],
    })

    # Contacts folder
    contact_filter_items = [make_contact_query(n, q) for n, q in contact_filters]
    contact_use_case_items = [make_contact_query(n, q) for n, q in contact_use_cases]
    pagination_items = [
        make_contact_query("Get Contacts with Cursor Pagination", {"filters": {"conditions": [{"field": "country", "operator": "in", "value": ["united states"]}]}, "orderBy": [{"orderBy": "last_name", "orderDirection": "asc"}, {"orderBy": "uuid", "orderDirection": "asc"}], "searchAfter": ["smith", "abc-123"], "limit": 25}),
        make_contact_query("Pagination - Page-Based (First Page)", {"limit": 25, "page": 1, "offset": 0}),
        make_contact_query("Pagination - Page-Based (Multiple Sorts)", {"orderBy": [{"orderBy": "seniority", "orderDirection": "desc"}, {"orderBy": "last_name", "orderDirection": "asc"}], "limit": 25, "page": 1}),
        make_contact_query("Pagination - Cursor with Multiple Sorts", {"filters": {"conditions": [{"field": "departments", "operator": "in", "value": ["Engineering"]}]}, "orderBy": [{"orderBy": "seniority", "orderDirection": "desc"}, {"orderBy": "uuid", "orderDirection": "asc"}], "searchAfter": ["senior", "uuid-here"], "limit": 25}),
    ]
    select_columns_items = [
        make_contact_query("Select Columns - Essential Fields Only", {"selectColumns": ["uuid", "first_name", "last_name", "email"], "limit": 25}),
        make_contact_query("Select Columns - All Core Fields", {"selectColumns": ["uuid", "first_name", "last_name", "email", "title", "departments", "seniority", "email_status", "company_id"], "limit": 25}),
        make_contact_query("Select Columns - With Metadata Fields", {"selectColumns": ["uuid", "first_name", "last_name", "email", "title", "created_at", "updated_at"], "limit": 25}),
        make_contact_query("Select Columns - Companies Essential Fields", {"selectColumns": ["uuid", "first_name", "last_name", "email", "company_id", "company_name", "company_employees_count"], "limit": 25, "filters": {"conditions": [{"field": "company_industries", "operator": "in", "value": ["Software"]}]}}),
        make_contact_query("Select Columns - Companies All Fields", {"selectColumns": ["uuid", "first_name", "last_name", "email", "title", "company_id", "company_name", "company_industries", "company_employees_count", "company_annual_revenue", "company_country"], "limit": 25}),
    ]
    standalone_filters = [
        make_contact_query("Get Contacts by Filter", {"filters": {"conditions": [{"field": "departments", "operator": "in", "value": ["Engineering"]}, {"field": "seniority", "operator": "in", "value": ["senior"]}]}, "limit": 25}),
        make_contact_query("Filter Contacts by Company Attributes (Denormalized Fields)", {"filters": {"conditions": [{"field": "company_industries", "operator": "in", "value": ["Software"]}, {"field": "company_employees_count", "operator": "gte", "value": 100}]}, "limit": 25}),
        make_contact_query("Search Contacts by Company Name (Substring)", {"filters": {"conditions": [{"field": "company_name", "operator": "contains", "value": "Acme"}]}, "limit": 25}),
        make_contact_query("Complex Contact Search with must_not", {"filters": {"conditions": [{"field": "departments", "operator": "in", "value": ["Engineering"]}, {"field": "seniority", "operator": "in", "value": ["senior"]}]}, "limit": 25}),
        make_contact_query("Filter Contacts with Company Data (company_config)", {"filters": {"conditions": [{"field": "email_status", "operator": "eq", "value": "verified"}]}, "companyConfig": {"populate": True, "selectColumns": ["uuid", "name", "employees_count"]}, "limit": 25}),
        make_contact_query("Company Config - Minimal Company Data", {"companyConfig": {"populate": True, "selectColumns": ["uuid", "name"]}, "limit": 25}),
        make_contact_query("Company Config - Full Company Details", {"companyConfig": {"populate": True, "selectColumns": ["uuid", "name", "industries", "employees_count", "annual_revenue", "website", "city", "country"]}, "limit": 25}),
        make_contact_query("Company Config - With Denormalized Filtering", {"filters": {"conditions": [{"field": "company_industries", "operator": "in", "value": ["Software"]}]}, "companyConfig": {"populate": True}, "limit": 25}),
        make_contact_query("Account-Based: High-Value Account Targeting", {"filters": {"conditions": [{"field": "company_annual_revenue", "operator": "gte", "value": 10000000}, {"field": "company_employees_count", "operator": "gte", "value": 500}, {"field": "seniority", "operator": "in", "value": ["executive", "lead"]}]}, "limit": 50}),
        make_contact_query("Account-Based: Technology Stack Targeting", {"filters": {"conditions": [{"field": "company_technologies", "operator": "in", "value": ["AWS", "Python"]}, {"field": "departments", "operator": "in", "value": ["Engineering"]}]}, "limit": 50}),
        make_contact_query("Account-Based: Industry-Specific Targeting", {"filters": {"conditions": [{"field": "company_industries", "operator": "in", "value": ["Healthcare", "FinTech"]}, {"field": "title", "operator": "contains", "value": "director"}]}, "limit": 50}),
        make_contact_query("Account-Based: Geographic Targeting", {"filters": {"conditions": [{"field": "company_country", "operator": "in", "value": ["united states"]}, {"field": "company_state", "operator": "in", "value": ["california", "new york"]}]}, "limit": 50}),
        make_contact_query("Account-Based: Growth Stage Targeting", {"filters": {"conditions": [{"field": "company_total_funding", "operator": "gte", "value": 5000000}, {"field": "company_employees_count", "operator": "lte", "value": 500}]}, "limit": 50}),
    ]
    items.append({
        "name": "Contacts",
        "item": [
            {"name": "Filter Examples", "item": contact_filter_items},
            {"name": "Standalone filters", "item": standalone_filters},
            {"name": "Use Cases", "item": contact_use_case_items},
            {"name": "Pagination", "item": pagination_items},
            {"name": "Select Columns", "item": select_columns_items},
            req("Get Contacts Count", gql_query("ContactCount", "query($query:VQLQueryInput){ contacts{ contactCount(query:$query)}}", {"query": {"filters": {"conditions": [{"field": "country", "operator": "in", "value": ["united states"]}, {"field": "seniority", "operator": "eq", "value": "senior"}]}}}), "REST: POST /contacts/count → GraphQL: contacts.contactCount"),
            req("Get Filters", gql_query("ContactFilters", "query{ contacts{ filters{ items{ filterKey filterType} total}}}", {}), "REST: GET /common/contacts/filters → GraphQL: contacts.filters"),
            req("Get Filter Data", gql_query("ContactFilterData", "query($input:ContactFilterDataInput!){ contacts{ filterData(input:$input){ items{ value count} total}}}", {"input": {"filterKey": "departments", "searchText": "", "page": 1, "limit": 20}}), "REST: POST /common/contacts/filters/data → GraphQL: contacts.filterData(input)"),
            req("Bulk Upsert Contacts", gql_query("BatchCreateContacts", "mutation BatchCreateContacts($input:BatchCreateContactsInput!){ contacts{ batchCreateContacts(input:$input){ uuid firstName lastName email}}}", {"input": {"contacts": [{"firstName": "John", "lastName": "Doe", "email": "john.doe@acme.com", "title": "Senior Engineer"}, {"firstName": "Jane", "lastName": "Smith", "email": "jane.smith@tech.io", "title": "Product Manager"}]}}), "REST: POST /contacts/batch-upsert → GraphQL: contacts.batchCreateContacts"),
        ],
    })

    # Common
    items.append({
        "name": "Common",
        "item": [
            req("Batch Upsert (CSV Data)", gql_query("CreateContact360Import", "mutation CreateContact360Import($input:CreateContact360ImportInput!){ jobs{ createContact360Import(input:$input){ id jobId jobType status createdAt}}}", {"input": {"s3Key": "uploads/{{userId}}/contacts_import_2024.csv", "outputPrefix": "imports/contact360/", "chunkCount": 8, "retryCount": 3, "retryInterval": 5}}), "REST: POST /common/batch-upsert (CSV) → GraphQL: jobs.createContact360Import. SuperAdmin only."),
            req("Get Upload URL", gql_query("InitiateUpload", "mutation InitiateUpload($input:InitiateUploadInput!){ upload{ initiateUpload(input:$input){ uploadId fileKey}}}", {"input": {"filename": "contacts_import_2024.csv", "contentType": "text/csv"}}), "REST: GET /common/upload-url → GraphQL: upload.initiateUpload. Then upload.presignedUrl(uploadId, partNumber) for each part."),
            req("Get Presigned URL (for multipart)", gql_query("PresignedUrl", "query PresignedUrl($uploadId:String!,$partNumber:Int!){ upload{ presignedUrl(uploadId:$uploadId,partNumber:$partNumber)}}", {"uploadId": "{{uploadId}}", "partNumber": 1}), "For multipart upload: call after initiateUpload for each part."),
        ],
    })

    # Jobs (11 items) - complex job vars loaded from JSON to avoid Python parser issues
    _je = _filters_data.get("job_export_contacts_vars", {})
    _jec = _filters_data.get("job_export_companies_vars", {})
    _jecf = _filters_data.get("job_export_contacts_complex_vars", {})
    items.append({
        "name": "Jobs",
        "item": [
            req("Create Job - Import CSV File", gql_query("CreateContact360Import", "mutation CreateContact360Import($input:CreateContact360ImportInput!){ jobs{ createContact360Import(input:$input){ id jobId jobType status createdAt}}}", {"input": {"s3Key": "uploads/contacts.csv", "outputPrefix": "imports/", "chunkCount": 8, "retryCount": 3, "retryInterval": 5}}), "REST: POST /common/jobs/create (insert_csv_file) → GraphQL: jobs.createContact360Import"),
            req("Create Job - Export Contacts to CSV", gql_query("CreateContact360Export", "mutation CreateContact360Export($input:CreateContact360ExportInput!){ contacts{ exportContacts(input:$input){ id jobId jobType status createdAt}}}", {"input": _je}), "REST: POST /common/jobs/create (export_csv_file, contact) → GraphQL: contacts.exportContacts"),
            req("Create Job - Export Companies to CSV", gql_query("CreateContact360Export", "mutation CreateContact360Export($input:CreateContact360ExportInput!){ companies{ exportCompanies(input:$input){ id jobId jobType status createdAt}}}", {"input": _jec}), "REST: POST /common/jobs/create (export_csv_file, company) → GraphQL: companies.exportCompanies"),
            req("List Jobs - All Jobs", gql_query("ListJobs", "query ListJobs($limit:Int,$offset:Int){ jobs{ jobs(limit:$limit,offset:$offset){ jobs{ id jobId jobType status createdAt} pageInfo{ total limit offset hasNext hasPrevious}}}}", {"limit": 25, "offset": 0}), "REST: POST /common/jobs → GraphQL: jobs.jobs"),
            req("List Jobs - Filter by Status", gql_query("ListJobs", "query ListJobs($limit:Int,$offset:Int,$status:String){ jobs{ jobs(limit:$limit,offset:$offset,status:$status){ jobs{ id jobId jobType status} pageInfo{ total}}}}", {"limit": 50, "offset": 0, "status": "processing"}), "REST: POST /common/jobs with status filter"),
            req("List Jobs - Filter by Job Type", gql_query("ListJobs", "query ListJobs($limit:Int,$offset:Int,$jobType:String,$status:String){ jobs{ jobs(limit:$limit,offset:$offset,jobType:$jobType,status:$status){ jobs{ id jobId jobType status} pageInfo{ total}}}}", {"limit": 100, "offset": 0, "jobType": "contact360_export_stream", "status": "completed"}), "REST: POST /common/jobs with job_type filter"),
            req("List Jobs - Failed Jobs", gql_query("ListJobs", "query ListJobs($limit:Int,$status:String){ jobs{ jobs(limit:$limit,status:$status){ jobs{ id jobId jobType status requestPayload responsePayload} pageInfo{ total}}}}", {"limit": 100, "status": "failed"}), "REST: POST /common/jobs with status failed"),
            req("Create Job - Import CSV (Default Bucket)", gql_query("CreateContact360Import", "mutation CreateContact360Import($input:CreateContact360ImportInput!){ jobs{ createContact360Import(input:$input){ id jobId jobType status createdAt}}}", {"input": {"s3Key": "uploads/contacts_import_2024.csv", "outputPrefix": "imports/", "chunkCount": 8, "retryCount": 3}}), "REST: POST /common/jobs/create without s3_bucket"),
            req("Create Job - Export Contacts (Complex Filters)", gql_query("CreateContact360Export", "mutation CreateContact360Export($input:CreateContact360ExportInput!){ contacts{ exportContacts(input:$input){ id jobId jobType status createdAt}}}", {"input": _jecf}), "REST: Export with denormalized company filters"),
            req("List Jobs - Active Jobs (Open + Processing)", gql_query("ListJobs", "query ListJobs($limit:Int,$status:String){ jobs{ jobs(limit:$limit,status:$status){ jobs{ id jobId jobType status} pageInfo{ total}}}}", {"limit": 50, "status": "processing"}), "REST: List active jobs"),
            req("List Jobs - Completed Exports Only", gql_query("ListJobs", "query ListJobs($limit:Int,$jobType:String,$status:String){ jobs{ jobs(limit:$limit,jobType:$jobType,status:$status){ jobs{ id jobId jobType status} pageInfo{ total}}}}", {"limit": 100, "jobType": "contact360_export_stream", "status": "completed"}), "REST: List completed export jobs"),
            req("Get Job", gql_query("GetJob", "query GetJob($jobId:ID!){ jobs{ job(jobId:$jobId){ id jobId userId jobType status requestPayload responsePayload statusPayload createdAt updatedAt}}}", {"jobId": "{{jobUuid}}"}), "REST: Get single job by ID"),
        ],
    })

    collection = {
        "info": {
            "_postman_id": COLLECTION_ID,
            "name": "Connectra GraphQL API (via Appointment360)",
            "description": "GraphQL equivalent of Connectra REST API. Same folder structure. Setup: baseUrl, email, password. Run Auth > Login first. All requests use Authorization: Bearer {{accessToken}}.",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "variable": [
            {"key": "baseUrl", "value": "http://localhost:8000", "type": "string"},
            {"key": "accessToken", "value": "", "type": "string"},
            {"key": "refreshToken", "value": "", "type": "string"},
            {"key": "userId", "value": "", "type": "string"},
            {"key": "email", "value": "", "type": "string"},
            {"key": "password", "value": "", "type": "string"},
            {"key": "contactUuid", "value": "", "type": "string"},
            {"key": "companyUuid", "value": "", "type": "string"},
            {"key": "jobUuid", "value": "", "type": "string"},
            {"key": "uploadId", "value": "", "type": "string"},
        ],
        "auth": {"type": "bearer", "bearer": [{"key": "token", "value": "{{accessToken}}", "type": "string"}]},
        "item": items,
    }
    return collection


if __name__ == "__main__":
    out_path = "Connectra_GraphQL_API.postman_collection.json"
    collection = build_collection()
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)
    print(f"Generated {out_path}")
