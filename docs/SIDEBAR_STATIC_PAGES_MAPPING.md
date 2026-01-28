# Static Pages Mapping - Complete Reference

**Date:** 2026-01-28  
**Purpose:** Document all static pages and their relationships to dynamic parent pages

---

## Overview

This document maps all static pages (forms, confirmations, info pages) to their parent dynamic pages and documents navigation patterns.

---

## 1. Documentation App Static Pages

### 1.1 Pages Section

#### Parent: List Pages (`/docs/pages/list/`)
- **Type:** Dynamic (List page)
- **App:** `documentation`
- **URL Name:** `pages_list`

#### Child: Create Page Form (`/docs/pages/create/`)
- **Type:** Static (Form)
- **App:** `documentation`
- **URL Name:** `page_create`
- **Access Via:** `via_list` (accessed from list page)
- **Redirect Target:** `page_detail` (redirects to new page detail after creation)
- **Return URL:** Generated to point back to list page
- **Badge:** "New"

#### Edit Page Form (`/docs/pages/<page_id>/edit/`)
- **Type:** Static (Form)
- **App:** `documentation`
- **URL Name:** `page_edit`
- **Access Via:** `via_detail` (accessed from detail page)
- **Redirect Target:** `page_detail` (redirects back to detail page)
- **Return URL:** Preserved from detail page
- **NOT in sidebar:** Accessed via detail page "Edit" button

#### Delete Confirmation (`/docs/pages/<page_id>/delete/`)
- **Type:** Static (Confirmation)
- **App:** `documentation`
- **URL Name:** `page_delete`
- **Access Via:** `via_detail` (accessed from detail page)
- **Redirect Target:** `pages_list` (redirects to list after deletion)
- **NOT in sidebar:** Accessed via detail page "Delete" button

---

### 1.2 Endpoints Section

#### Parent: List Endpoints (`/docs/endpoints/list/`)
- **Type:** Dynamic (List page)
- **App:** `documentation`
- **URL Name:** `endpoints_list`

#### Child: Create Endpoint Form (`/docs/endpoints/create/`)
- **Type:** Static (Form)
- **App:** `documentation`
- **URL Name:** `endpoint_create`
- **Access Via:** `via_list`
- **Redirect Target:** `endpoint_detail`
- **Return URL:** Generated to point back to list page
- **Badge:** "New"

#### Edit Endpoint Form (`/docs/endpoints/<endpoint_id>/edit/`)
- **Type:** Static (Form)
- **Access Via:** `via_detail`
- **NOT in sidebar:** Accessed via detail page

#### Delete Confirmation (`/docs/endpoints/<endpoint_id>/delete/`)
- **Type:** Static (Confirmation)
- **Access Via:** `via_detail`
- **NOT in sidebar:** Accessed via detail page

---

### 1.3 Relationships Section

#### Parent: List Relationships (`/docs/relationships/list/`)
- **Type:** Dynamic (List page)
- **App:** `documentation`
- **URL Name:** `relationships_list`

#### Child: Create Relationship Form (`/docs/relationships/create/`)
- **Type:** Static (Form)
- **App:** `documentation`
- **URL Name:** `relationship_create`
- **Access Via:** `via_list`
- **Redirect Target:** `relationship_detail`
- **Return URL:** Generated to point back to list page
- **Badge:** "New"

#### Edit Relationship Form (`/docs/relationships/<relationship_id>/edit/`)
- **Type:** Static (Form)
- **Access Via:** `via_detail`
- **NOT in sidebar:** Accessed via detail page

---

### 1.4 Postman Section

#### Parent: Postman Dashboard (`/docs/postman/` or `/postman/dashboard/`)
- **Type:** Dynamic (Dashboard)
- **App:** `postman`
- **URL Name:** `dashboard`

#### Child: Create Postman Config Form (`/docs/postman/create/`)
- **Type:** Static (Form)
- **App:** `documentation`
- **URL Name:** `postman_create`
- **Access Via:** `via_list`
- **Redirect Target:** `postman_detail`
- **Return URL:** Generated to point back to dashboard
- **Badge:** "New"

#### Edit Postman Config Form (`/docs/postman/<postman_id>/edit/`)
- **Type:** Static (Form)
- **Access Via:** `via_detail`
- **NOT in sidebar:** Accessed via detail page

---

## 2. Knowledge App Static Pages

### 2.1 Knowledge Base Section

#### Parent: List Knowledge (`/knowledge/`)
- **Type:** Dynamic (List page)
- **App:** `knowledge`
- **URL Name:** `list`

#### Child: Create Knowledge Entry Form (`/knowledge/create/`)
- **Type:** Static (Form)
- **App:** `knowledge`
- **URL Name:** `create`
- **Access Via:** `via_list`
- **Redirect Target:** `detail`
- **Return URL:** Generated to point back to list page
- **Badge:** "New"

#### Edit Knowledge Entry Form (`/knowledge/<knowledge_id>/edit/`)
- **Type:** Static (Form)
- **Access Via:** `via_detail`
- **NOT in sidebar:** Accessed via detail page

#### Delete Confirmation (`/knowledge/<knowledge_id>/delete/`)
- **Type:** Static (Confirmation)
- **Access Via:** `via_detail`
- **NOT in sidebar:** Accessed via detail page

---

## 3. Tasks App Static Pages

### 3.1 Tasks Section

#### Parent: List Tasks (`/tasks/`)
- **Type:** Dynamic (List page)
- **App:** `tasks`
- **URL Name:** `list`

#### Child: Create Task Form (`/tasks/create/`)
- **Type:** Static (Form)
- **App:** `tasks`
- **URL Name:** `create`
- **Access Via:** `via_list`
- **Redirect Target:** `detail`
- **Return URL:** Generated to point back to list page
- **Badge:** "New"

#### Edit Task Form (`/tasks/<task_id>/edit/`)
- **Type:** Static (Form)
- **Access Via:** `via_detail`
- **NOT in sidebar:** Accessed via detail page

---

## 4. Durgasflow App Static Pages

### 4.1 Workflows Section

#### Parent: List Workflows (`/durgasflow/workflows/`)
- **Type:** Dynamic (List page)
- **App:** `durgasflow`
- **URL Name:** `workflow_list`

#### Child: Create Workflow Form (`/durgasflow/workflow/create/`)
- **Type:** Static (Form)
- **App:** `durgasflow`
- **URL Name:** `workflow_create`
- **Access Via:** `via_list`
- **Redirect Target:** `workflow_detail`
- **Return URL:** Generated to point back to list page
- **Badge:** "New"

#### Child: New Editor (`/durgasflow/editor/new/`)
- **Type:** Static (Editor UI)
- **App:** `durgasflow`
- **URL Name:** `editor_new`
- **Access Via:** `direct` (standalone editor)
- **Icon:** Edit icon

#### Edit Workflow Form (`/durgasflow/workflow/<workflow_id>/edit/`)
- **Type:** Static (Form)
- **Access Via:** `via_detail`
- **NOT in sidebar:** Accessed via detail page

#### Delete Confirmation (`/durgasflow/workflow/<workflow_id>/delete/`)
- **Type:** Static (Confirmation)
- **Access Via:** `via_detail`
- **NOT in sidebar:** Accessed via detail page

---

### 4.2 Credentials Section

#### Parent: List Credentials (`/durgasflow/credentials/`)
- **Type:** Dynamic (List page)
- **App:** `durgasflow`
- **URL Name:** `credential_list`

#### Child: Create Credential Form (`/durgasflow/credential/create/`)
- **Type:** Static (Form)
- **App:** `durgasflow`
- **URL Name:** `credential_create`
- **Access Via:** `via_list`
- **Redirect Target:** `credential_detail`
- **Return URL:** Generated to point back to list page
- **Badge:** "New"

#### Edit Credential Form (`/durgasflow/credential/<credential_id>/edit/`)
- **Type:** Static (Form)
- **Access Via:** `via_detail`
- **NOT in sidebar:** Accessed via detail page

#### Delete Confirmation (`/durgasflow/credential/<credential_id>/delete/`)
- **Type:** Static (Confirmation)
- **Access Via:** `via_detail`
- **NOT in sidebar:** Accessed via detail page

---

## 5. Public/Info Pages

### 5.1 API Documentation Pages

#### API Documentation Index (`/api/docs/`)
- **Type:** Info (Static content)
- **URL:** `/api/docs/`
- **Access Via:** `direct`
- **Group:** DOCUMENTATION
- **External:** False

#### Swagger UI (`/api/swagger/`)
- **Type:** Info (Static UI, dynamic API calls)
- **URL:** `/api/swagger/`
- **Access Via:** `direct`
- **Group:** TOOLS & INFO
- **External:** False

#### ReDoc (`/api/redoc/`)
- **Type:** Info (Static UI, dynamic API calls)
- **URL:** `/api/redoc/`
- **Access Via:** `direct`
- **Group:** TOOLS & INFO
- **External:** False

---

### 5.2 Postman Homepage

#### Postman Homepage (`/postman/`)
- **Type:** Info (Mostly static, minimal stats)
- **App:** `postman`
- **URL Name:** `homepage`
- **Access Via:** `direct`
- **Group:** MANAGEMENT (or separate)

---

## 6. Tools & Info Pages

### 6.1 Architecture

#### Architecture Blueprint (`/architecture/`)
- **Type:** Info (Static structure info)
- **App:** `architecture`
- **URL Name:** `blueprint`
- **Access Via:** `direct`
- **Group:** TOOLS & INFO

---

### 6.2 Database

#### Database Schema Viewer (`/database/`)
- **Type:** Info (Static schema, dynamic data)
- **App:** `database`
- **URL Name:** `schema`
- **Access Via:** `direct`
- **Group:** TOOLS & INFO

---

### 6.3 Roadmap

#### Roadmap Dashboard (`/roadmap/`)
- **Type:** Info (Static roadmap, dynamic progress)
- **App:** `roadmap`
- **URL Name:** `dashboard`
- **Access Via:** `direct`
- **Group:** TOOLS & INFO

---

### 6.4 Accessibility

#### Accessibility Dashboard (`/accessibility/`)
- **Type:** Info (Static guidelines, dynamic checks)
- **App:** `accessibility`
- **URL Name:** `dashboard`
- **Access Via:** `direct`
- **Group:** TOOLS & INFO

---

### 6.5 Test Runner

#### Test Runner Dashboard (`/tests/`)
- **Type:** Dynamic (Static test framework, dynamic results)
- **App:** `test_runner`
- **URL Name:** `dashboard`
- **Access Via:** `direct`
- **Group:** TOOLS & INFO

---

## 7. Navigation Patterns Summary

### Pattern 1: Create Forms
- **Access:** Via list page button → Sidebar link
- **Location:** Under parent list page in sidebar
- **Redirect:** To detail page after creation
- **Return URL:** Points back to list page

### Pattern 2: Edit Forms
- **Access:** Via detail page button
- **Location:** NOT in sidebar
- **Redirect:** Back to detail page
- **Return URL:** Preserved from detail page

### Pattern 3: Delete Confirmations
- **Access:** Via detail page button
- **Location:** NOT in sidebar
- **Redirect:** To list page after deletion

### Pattern 4: Info Pages
- **Access:** Direct from sidebar
- **Location:** In appropriate group (DOCUMENTATION or TOOLS & INFO)
- **No redirect:** Standalone pages

---

## 8. Statistics

### Static Pages in Sidebar: 12
- Create Forms: 8
- Editor: 1
- Info Pages: 3

### Static Pages NOT in Sidebar: 18
- Edit Forms: 9
- Delete Confirmations: 9

### Total Static Pages: 30
- Forms: 17
- Confirmations: 9
- Info Pages: 4

---

## 9. Access Patterns

### Direct Access (Sidebar)
- All list/dashboard pages
- All create forms
- All info pages
- New editor

### Via Detail Page
- Edit forms
- Delete confirmations

### Via List Page
- Create forms (also in sidebar)

---

## 10. Return URL Flow

```
List Page → Create Form → Detail Page
  ↑                              ↓
  └──────── Return URL ──────────┘

Detail Page → Edit Form → Detail Page
  ↑                              ↓
  └──────── Return URL ──────────┘

Detail Page → Delete Confirmation → List Page
```

---

**Last Updated:** 2026-01-28  
**Status:** Complete
