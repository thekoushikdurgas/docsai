

| CONTACT 360 Staffing Intelligence Platform ──────────────────── Product Requirements & Roadmap Documentation Version 1.x Series  •  Internal Use Only  •  June 2026 |
| :---: |

| Field | Details |
| :---- | :---- |
| Document Title | Contact 360 — Product Requirements & Roadmap |
| Platform Name | Contact 360 |
| Document Version | v2.0 (Updated) |
| Date Updated | June 2026 |
| Document Owner | Product Team |
| Classification | Internal — Confidential |
| Target Audience | Product, Engineering, Design, QA, Leadership |

| 1\. Executive Summary Platform Overview & Vision |
| :---- |

## **1.1 Product Overview**

Contact 360 is a B2B SaaS platform purpose-built for the staffing industry. It aggregates live job postings from across the US job market — including LinkedIn Jobs, Indeed, Glassdoor, and other major platforms — into a single unified dashboard. Staffing companies use Contact 360 to identify business development opportunities, find prospect companies actively hiring, and access contact information of key decision-makers.

## **1.2 The Problem We Solve**

Staffing agencies today face a fragmented, manual process to discover which companies are hiring and who to contact. Business development teams spend hours switching between platforms, exporting job data, and cross-referencing contact directories. Contact 360 eliminates this friction by bringing everything into one intelligent platform.

## **1.3 Target Users**

Version 1.x serves three primary customer segments:

| \# | Segment | Use Case |
| :---- | :---- | :---- |
| 1 | IT Industry — Staff Augmentation | Find companies actively hiring IT talent to pitch augmentation services and place consultants |
| 2 | IT Industry — Bench Sales | Identify open positions matching benched consultants and reach decision-makers quickly |
| 3 | Staffing Industry | Discover hiring signals across industries to drive business development and placements |

**Version 2 — Planned Expansion:**

| \# | Segment | Use Case |
| :---- | :---- | :---- |
| 1 | Colleges & Training Industry | Identify hiring trends and employer demand to align curricula, placement drives, and industry partnerships |

## **1.4 Geographic Coverage**

* United States — primary and only market for v1.x series

* Country filter is fixed to US; no global expansion planned in this version series

## **1.5 Integrated Job Platforms**

* LinkedIn Jobs

* Indeed

* Glassdoor

* ZipRecruiter

* Monster

* CareerBuilder

* SimplyHired

* Additional US job boards (phased)

| 2\. Complete Filter System All filters mapped to their release version |
| :---- |

Below is the full filter specification for Contact 360, organized by version. Filters marked v1 ship at initial launch. Filters marked v1.1 ship in the second release. Filters marked v1.2 ship in the third release.

## **2.1 Company Filters**

| Filter | Description | Version | Notes |
| :---- | :---- | :---- | :---- |
| Company Name | Search by exact or partial company name | v1 | Text search, core filter |
| Country | US only — fixed, no multi-country selection | v1 | Defaults to and locked to United States |
| Industry | Filter by industry vertical (Tech, Healthcare, Finance, etc.) | v1 | Multi-select dropdown |
| Employee Size | Filter by company headcount ranges (1-50, 51-200, 201-1000, 1000+) | v1 | Range selector |
| Revenue | Filter by estimated annual revenue bands | v1.2 | Requires enrichment data |
| Funding | Filter by funding stage (Seed, Series A/B/C, Public, etc.) | v1.1 | Multi-select dropdown |

## **2.2 Job Filters**

| Filter | Description | Version | Notes |
| :---- | :---- | :---- | :---- |
| Title | Search by job title keywords (e.g. Software Engineer, Sales Manager) | v1 | Text search |
| Location | Filter by US state (state-wise geographical selection) | v1 | US states dropdown |
| Date Posted | Filter by posting recency (Today, Last 7 days, Last 30 days, Any time) | v1 | Dropdown selector |
| Experience Level | Entry, Mid, Senior, Director, Executive | v1 | Multi-select |
| Job Type | Full-time, Part-time, Contract, Internship, Freelance | v1 | Multi-select |
| LinkedIn Apply | Filter to jobs with LinkedIn Easy Apply enabled | v1 | Toggle |
| Department | Job department: Sales, Marketing, Engineering, Finance, HR, etc. | v1 | Renamed from Category/Topic. Multi-select |
| Job Function | Specific function within a Department | v1 | Lives under Department filter |
| Education | Minimum education requirement (High School, Bachelor's, Master's, PhD) | v1.1 | Multi-select |
| Required Skills | Filter by specific skills listed in the job description | v1.1 | Tag-based multi-select, NLP parsed |
| Compliance & Preferences | Visa sponsorship, security clearance, EEO flags | v1.1 | Multi-select |
| Compensation | Filter by salary range or compensation type (hourly / annual) | v1.1 | Range selector |

## **2.3 Removed Filters**

| Filter | Decision | Reason |
| :---- | :---- | :---- |
| View | Removed | Replaced by tab navigation (All Signals / Today's Jobs / Saved) |
| Remote / Workplace | Removed | Not required for v1.x scope |

| 3\. Product Roadmap — Version 1.x Series v1  •  v1.1  •  v1.2 |
| :---- |

## **3.0 Versioning Philosophy**

Contact 360 follows a structured versioning model. Each version has a fixed, pre-defined core scope that the team commits to delivering. This ensures predictability and focus across product and engineering teams.

| Principle | Detail |
| :---- | :---- |
| Fixed core scope | Every version (v1, v1.1, v1.2 and beyond) has a locked set of features defined before development begins. The core scope does not change mid-version. |
| Market-driven additions | In addition to the fixed core, v1.2 and v1.3 will each include 2 additional requirements sourced from real customer and market feedback collected during earlier releases. |
| Evaluation process | The 2 additional requirements per version are evaluated, prioritized, and confirmed by the product team before that version's development cycle begins. |
| Stability gate | By the time v1.2 is released, v1 must be completely stable. Version stability is a hard prerequisite before the next version ships. |
| Continuous feedback loop | Customer requests are collected throughout the product lifecycle. Only the most impactful 2 requests per version are selected for inclusion. |

| VERSION 1 |
| :---- |

## **3.1 v1 Objectives**

Establish the core platform. Users can log in, see live job signals from integrated platforms, apply all primary filters, and receive email notifications for new matching jobs. This version is the first working product delivered to internal stakeholders.

### **3.1.1 Platform Setup**

* User authentication (email/password)

* Team/organization onboarding flow

* Role-based access: Admin and Viewer

* Basic subscription and billing scaffolding

### **3.1.2 Job Aggregation**

* LinkedIn Jobs integration

* Indeed integration

* Job normalization engine: map all fields to Contact 360 schema

* Deduplication logic: same job from multiple sources shown once

* Real-time fetch cadence: every 15–30 minutes

### **3.1.3 Dashboard**

* Main job signals list: Title, Company, Location, Type, Posted, Actions columns

* Tab navigation: All Signals | Today's Jobs | Saved

* Total signal count display

* Pagination: 50 jobs per page

* Refresh button with last-updated timestamp

* Export to XLSX (up to 500 rows)

### **3.1.4 Filters — v1 Live Set**

Company Filters:

* Company Name (text search)

* Country (US only, fixed)

* Industry (multi-select)

* Employee Size (range selector)

Job Filters:

* Title (text search)

* Location (US state-wise dropdown)

* Date Posted

* Experience Level

* Job Type

* LinkedIn Apply (toggle)

* Department (Sales, Marketing, Engineering, Finance, HR, etc.)

* Job Function (lives under Department)

### **3.1.5 Email Notifications — v1 Core Feature**

Users receive email notifications whenever new job signals match their active filter selections.

* Trigger: new job posted that matches user's active filters

* Delivery: email only

* Frequency options: Real-time (instant) or custom duration set by the user (e.g. every 2 hours, every 6 hours, every 12 hours)

* User configures their preferred frequency from their notification settings

* User can enable/disable notifications per saved filter set

* Email includes: job title, company, location, date posted, and link to dashboard

### **3.1.6 Contact Intelligence Module — v1 Core Feature**

When a staffing company sees a company posting jobs, they need to know who to contact. This module surfaces decision-makers — HR leaders, hiring managers, C-suite — at those companies.

| Contact Field | Visibility | Version |
| :---- | :---- | :---- |
| First Name | Always visible | v1 |
| Job Title | Always visible | v1 |
| Department | Always visible | v1 |
| Work Email | Always visible | v1 |
| LinkedIn Profile | Always visible | v1 |
| Phone Number | Planned | v1.3 (TBD) |

Note: Credit system for contact reveals will be defined ahead of v1.3 when Phone Number is introduced.

### **3.1.7 v1 Success Criteria**

| Metric | Target |
| :---- | :---- |
| Job platforms integrated | 2 (LinkedIn, Indeed) |
| Company filters live | 4 (Name, Country, Industry, Employee Size) |
| Job filters live | 8 (Title, Location, Date Posted, Experience, Job Type, LinkedIn Apply, Department, Job Function) |
| Email notifications | Live and functional |
| Dashboard load time | \< 3 seconds |
| Job fetch freshness | \< 30 minutes |
| Contact Intelligence | Live (5 fields: First Name, Job Title, Department, Work Email, LinkedIn) |

| VERSION 1.1 |
| :---- |

## **3.2 v1.1 Objectives**

Expand the filter system with the four advanced job filters. Improve platform stability, performance, and data quality based on v1 learnings. Suitable for a closed beta with select staffing company clients.

### **3.2.1 Additional Job Integrations**

* Add Indeed integration (expanded data feed)

* One additional platform TBD — to be confirmed by the team

* Improved deduplication across multiple sources

### **3.2.2 New Filters — v1.1**

* Education — minimum education requirement (High School, Bachelor's, Master's, PhD)

* Required Skills — tag-based multi-select, NLP-parsed from job descriptions

* Compliance & Preferences — visa sponsorship, security clearance, EEO flags

* Compensation — salary range filter (hourly / annual), min-max range selector

* Funding — filter by funding stage: Seed, Series A, Series B, Series C, Public, Bootstrapped

### **3.2.3 Stability & Performance**

* Dashboard load time target: \< 2.5 seconds

* Data freshness: \< 20 minutes

* Integration failure monitoring and alerting

* Platform status page (internal)

### **3.2.4 v1.1 Success Criteria**

| Metric | Target |
| :---- | :---- |
| Job platforms integrated | 2+ (Indeed \+ 1 TBD platform) |
| Total filters live | All 12 job \+ company filters (excl. Revenue) |
| Closed beta clients | 3–5 staffing companies |
| Dashboard load time | \< 2.5 seconds |
| Data freshness | \< 20 minutes |
| Critical bugs | 0 P0 bugs |

| VERSION 1.2 |
| :---- |

## **3.3 v1.2 Objectives**

Complete the company filter set with enrichment-powered Revenue filter. Harden the platform for General Availability with stability, security, and compliance targets met.

### **3.3.1 New Company Filters — v1.2**

* Revenue — filter by estimated annual revenue bands (requires enrichment data)

### **3.3.2 Platform Stability for GA**

* 99.9% uptime SLA

* Load testing: 500 concurrent users with no degradation

* SOC 2 Type I readiness

* GDPR-compliant data handling

* Full audit log for all user actions

* WCAG 2.1 AA accessibility compliance

### **3.3.3 Market-Driven Requirements — v1.2**

As part of the versioning philosophy, v1.2 will include 2 additional requirements gathered from customer and market feedback collected during v1 and v1.1. These will be evaluated and confirmed before v1.2 development begins.

| \# | Requirement | Source | Status |
| :---- | :---- | :---- | :---- |
| 1 | TBD — to be defined based on v1 customer feedback | Customer / Market | To be confirmed |
| 2 | TBD — to be defined based on v1.1 customer feedback | Customer / Market | To be confirmed |

### **3.3.4 v1.2 Launch Readiness Checklist**

| Category | Criteria | Target |
| :---- | :---- | :---- |
| Uptime | Platform availability | 99.9% SLA |
| Performance | Dashboard load | \< 2 seconds |
| Performance | Filter response | \< 500ms |
| Data | Job freshness | \< 15 minutes |
| Integrations | Live job platforms | 6+ |
| Filters | Company filters | All 6 live |
| Filters | Job filters | All 12 live |
| Features | Contact intelligence | Live with credits |
| Security | Audit log | All actions tracked |
| Quality | P0 bugs | 0 |
| Quality | QA test coverage | \> 80% core flows |

| 4\. Job Signal Data Schema Normalized fields across all integrated platforms |
| :---- |

| Field | Type | Source | Notes |
| :---- | :---- | :---- | :---- |
| signal\_id | UUID | System | Unique ID per signal |
| title | String | Platform | Job title as posted |
| company\_name | String | Platform | Hiring company name |
| company\_id | UUID | System | Links to company profile |
| location\_state | String | Platform | US state |
| location\_city | String | Platform | City of job |
| job\_type | Enum | Platform | full-time, part-time, contract, internship |
| experience\_level | Enum | Platform/Parsed | entry, mid, senior, director, executive |
| department | String | Platform/Parsed | Sales, Marketing, Engineering, etc. |
| job\_function | String | Platform/Parsed | Sub-function within department |
| date\_posted | Timestamp | Platform | Original posting date |
| date\_fetched | Timestamp | System | When Contact 360 ingested this |
| source\_platform | String | System | linkedin, indeed, glassdoor, etc. |
| source\_url | URL | Platform | Original job posting URL |
| description\_raw | Text | Platform | Full job description |
| required\_skills | String\[\] | Parsed (v1.1) | NLP-extracted from description |
| salary\_min | Number | Platform/Parsed (v1.1) | Minimum salary if disclosed |
| salary\_max | Number | Platform/Parsed (v1.1) | Maximum salary if disclosed |
| education\_required | String | Parsed (v1.1) | Minimum education level |
| visa\_sponsorship | Boolean | Parsed (v1.1) | From description |
| linkedin\_easy\_apply | Boolean | Platform | LinkedIn-specific flag |
| industry | String | Company data | From company enrichment |
| company\_size | String | Company data | Headcount range |
| revenue | String | Enrichment (v1.2) | Annual revenue band |
| funding\_stage | String | Enrichment (v1.2) | Seed, Series A, etc. |
| is\_saved | Boolean | User | Per-user saved state |

| *This document is confidential and intended for internal use only.* Contact 360 — Product Team — June 2026 |
| :---: |

