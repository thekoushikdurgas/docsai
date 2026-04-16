<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Read all the above and previous prompts and then think about my contact360 project in under 4.x.x - Contact360 Extension and Sales Navigator maturity , break into x.y and x.y.z with unique file name , Learn, understand, and analyse this deeply, and then break your tasks into smaller tasks.

Here is a **4.x.x roadmap** for your **Contact360 extension and sales navigator maturity**, broken into:

- **4.x** phases (major themes),
- **4.x.y** milestones,
- **4.x.y.z** granular tasks with **unique filenames** for your docs.

This sits on top of your 0.x.x foundation, 1.x.x billing, 2.x.x email/phone, and 3.x.x contacts/companies systems.

***

## 4.x.x – Contact360 Extension and Sales Navigator Maturity

### 4.1.x – Chrome Extension Architecture \& MV3 Fundamentals

#### 4.1.0 – Extension Project Setup

- **4.1.0.1 – MV3 manifest design (permissions, content scripts, background worker)**
File: `docs/60-extension/01-mv3-manifest-design.md`
- **4.1.0.2 – Extension folder structure \& build tooling (Vite, TypeScript, testing)**
File: `docs/60-extension/02-extension-project-structure.md`
- **4.1.0.3 – Extension versioning \& release strategy**
File: `docs/60-extension/03-extension-versioning-and-release.md`


#### 4.1.1 – Core Extension Components

- **4.1.1.1 – Background service worker (event listener, storage, OAuth token refresh)**
File: `docs/60-extension/04-background-service-worker-design.md`
- **4.1.1.2 – Content scripts (LinkedIn, Gmail, Sales Navigator, web)**
File: `docs/60-extension/05-content-scripts-multi-site-design.md`
- **4.1.1.3 – Popup UI (quick view, add to CRM, enrichment results)**
File: `docs/60-extension/06-extension-popup-ui-design.md`


#### 4.1.2 – Extension Authentication \& Security

- **4.1.2.1 – OAuth2 login flow (user authenticates with Contact360 via extension)**
File: `docs/60-extension/07-extension-oauth2-login-flow.md`
- **4.1.2.2 – Token management (refresh tokens, secure storage, expiry)**
File: `docs/60-extension/08-token-management-and-storage.md`
- **4.1.2.3 – Extension sandbox \& CSP (Content Security Policy) compliance**
File: `docs/60-extension/09-extension-sandbox-and-csp.md`

***

### 4.2.x – LinkedIn Data Extraction \& Enrichment

#### 4.2.0 – LinkedIn Profile Scraping

- **4.2.0.1 – LinkedIn profile page structure \& selector strategy**
File: `docs/61-linkedin/01-linkedin-profile-selectors.md`
- **4.2.0.2 – Profile data extraction (name, title, company, location, about)**
File: `docs/61-linkedin/02-profile-data-extraction-logic.md`
- **4.2.0.3 – LinkedIn API alternative (Sales Navigator API vs scraping trade-offs)**
File: `docs/61-linkedin/03-linkedin-api-vs-scraping-strategy.md`


#### 4.2.1 – LinkedIn Search Results \& List Views

- **4.2.1.1 – Search results page scraping (detect \& extract multiple profiles)**
File: `docs/61-linkedin/04-search-results-page-scraping.md`
- **4.2.1.2 – LinkedIn lists \& organization scraping (members, contacts)**
File: `docs/61-linkedin/05-linkedin-lists-and-org-scraping.md`
- **4.2.1.3 – Batch operations (scrape multiple profiles, queue for processing)**
File: `docs/61-linkedin/06-batch-profile-scraping-queue.md`


#### 4.2.2 – LinkedIn-Specific Enrichment

- **4.2.2.1 – LinkedIn URL → email finding (use extracted name/company)**
File: `docs/61-linkedin/07-linkedin-to-email-enrichment.md`
- **4.2.2.2 – LinkedIn URL → phone finding**
File: `docs/61-linkedin/08-linkedin-to-phone-enrichment.md`
- **4.2.2.3 – LinkedIn profile health \& verification (outdated info detection)**
File: `docs/61-linkedin/09-linkedin-profile-freshness-scoring.md`


#### 4.2.3 – LinkedIn Legal \& Rate Limiting

- **4.2.3.1 – LinkedIn ToS compliance \& abuse prevention (rate limiting, IP rotation)**
File: `docs/61-linkedin/10-linkedin-tos-and-compliance.md`
- **4.2.3.2 – Rate limiting strategy per user \& org (requests/hour, backoff)**
File: `docs/61-linkedin/11-linkedin-rate-limiting-strategy.md`
- **4.2.3.3 – LinkedIn session handling \& detection avoidance**
File: `docs/61-linkedin/12-linkedin-session-handling-evasion.md`

***

### 4.3.x – Gmail \& Email Integration

#### 4.3.0 – Gmail Data Access

- **4.3.0.1 – Gmail API integration (OAuth2, permission scopes, email read)**
File: `docs/62-gmail/01-gmail-api-integration.md`
- **4.3.0.2 – Content script: detect email sender/recipient (parse from page)**
File: `docs/62-gmail/02-gmail-sender-recipient-detection.md`
- **4.3.0.3 – Email metadata extraction (subject, from, to, date, message ID)**
File: `docs/62-gmail/03-gmail-metadata-extraction.md`


#### 4.3.1 – Email Activity Logging

- **4.3.1.1 – Auto-log emails to Contact360 (sender → contact mapping)**
File: `docs/62-gmail/04-gmail-auto-email-logging.md`
- **4.3.1.2 – Email thread detection \& grouping (same contact, same company)**
File: `docs/62-gmail/05-gmail-thread-detection-and-grouping.md`
- **4.3.1.3 – Email attachment tracking (files sent/received)**
File: `docs/62-gmail/06-gmail-attachment-tracking.md`


#### 4.3.2 – Gmail-Specific Enrichment

- **4.3.2.1 – Email sender → contact lookup (does this email exist in CRM?)**
File: `docs/62-gmail/07-gmail-sender-contact-lookup.md`
- **4.3.2.2 – Email sender → enrichment (if not in CRM, enrich name/company/phone)**
File: `docs/62-gmail/08-gmail-sender-enrichment.md`
- **4.3.2.3 – Email signature parsing (extract contact info, phone)**
File: `docs/62-gmail/09-gmail-signature-parsing.md`


#### 4.3.3 – Gmail Compliance \& Privacy

- **4.3.3.1 – Gmail privacy \& data minimization (what data to access, retention)**
File: `docs/62-gmail/10-gmail-privacy-and-data-minimization.md`
- **4.3.3.2 – GDPR consent for email logging (user disclosure, opt-in)**
File: `docs/62-gmail/11-gmail-consent-and-gdpr-compliance.md`
- **4.3.3.3 – Email sync conflicts \& resolution (same email logged twice)**
File: `docs/62-gmail/12-gmail-sync-conflict-resolution.md`

***

### 4.4.x – Sales Navigator \& LinkedIn Premium Features

#### 4.4.0 – Sales Navigator Profile Access

- **4.4.0.1 – Sales Navigator page structure \& selectors (InMail credits, notes, tags)**
File: `docs/63-sales-navigator/01-sales-navigator-page-structure.md`
- **4.4.0.2 – Sales Navigator lead notes \& saved notes extraction**
File: `docs/63-sales-navigator/02-sales-navigator-lead-notes-extraction.md`
- **4.4.0.3 – Sales Navigator account insights (company info, employees, buying signals)**
File: `docs/63-sales-navigator/03-sales-navigator-account-insights.md`


#### 4.4.1 – Sales Navigator Buying Signals

- **4.4.1.1 – Lead activity tracking (profile views, post engagement, updates)**
File: `docs/63-sales-navigator/04-sales-navigator-lead-activity-signals.md`
- **4.4.1.2 – Job change detection \& alerts (new role, company change)**
File: `docs/63-sales-navigator/05-sales-navigator-job-change-detection.md`
- **4.4.1.3 – Hiring signals (company hiring, new departments opening)**
File: `docs/63-sales-navigator/06-sales-navigator-hiring-signals.md`


#### 4.4.2 – Sales Navigator Workflow Integration

- **4.4.2.1 – Sales Navigator sequence automation (scheduled messages, reminders)**
File: `docs/63-sales-navigator/07-sales-navigator-sequence-automation.md`
- **4.4.2.2 – Sales Navigator saved leads → Contact360 list sync**
File: `docs/63-sales-navigator/08-sales-navigator-saved-leads-sync.md`
- **4.4.2.3 – InMail credit tracking \& send optimization**
File: `docs/63-sales-navigator/09-inmail-credit-tracking.md`

***

### 4.5.x – Extension Popup UI \& UX

#### 4.5.0 – Popup Layout \& Components

- **4.5.0.1 – Popup frame design (header, contact info, actions, enrichment results)**
File: `docs/64-popup-ui/01-popup-layout-and-components.md`
- **4.5.0.2 – Contact card (name, title, company, email, phone, source)**
File: `docs/64-popup-ui/02-contact-card-component.md`
- **4.5.0.3 – Quick actions (add to CRM, enrichment, send message)**
File: `docs/64-popup-ui/03-quick-actions-menu.md`


#### 4.5.1 – Real‑Time Enrichment Display

- **4.5.1.1 – Enrichment status UI (loading, success, partial, failed)**
File: `docs/64-popup-ui/04-enrichment-status-indicators.md`
- **4.5.1.2 – Email/phone enrichment results display (with confidence scores)**
File: `docs/64-popup-ui/05-enrichment-results-display.md`
- **4.5.1.3 – Source attribution (which provider found this email/phone)**
File: `docs/64-popup-ui/06-source-attribution-display.md`


#### 4.5.2 – Add-to-CRM Workflow

- **4.5.2.1 – Add to CRM button flow (creates contact, enriches, logs activity)**
File: `docs/64-popup-ui/07-add-to-crm-workflow.md`
- **4.5.2.2 – Duplicate detection \& merge UI (contact already in CRM)**
File: `docs/64-popup-ui/08-duplicate-detection-ui.md`
- **4.5.2.3 – Quick field editing in popup (name, title, company edit before save)**
File: `docs/64-popup-ui/09-quick-edit-before-save.md`


#### 4.5.3 – Extension Settings \& Preferences

- **4.5.3.1 – Settings page (API key, auto-enrichment, logging preferences)**
File: `docs/64-popup-ui/10-extension-settings-page.md`
- **4.5.3.2 – Per-site controls (enable/disable on LinkedIn, Gmail, etc.)**
File: `docs/64-popup-ui/11-per-site-controls-and-toggles.md`
- **4.5.3.3 – Notification preferences (toast, badge, background enrichment)**
File: `docs/64-popup-ui/12-notification-preferences.md`

***

### 4.6.x – Extension Data Sync \& Local Storage

#### 4.6.0 – Local Storage Strategy

- **4.6.0.1 – Chrome storage APIs (local, sync, session; quota \& limits)**
File: `docs/65-extension-sync/01-chrome-storage-strategy.md`
- **4.6.0.2 – Cache layer (recently viewed contacts, enrichment results, API responses)**
File: `docs/65-extension-sync/02-extension-cache-and-ttl.md`
- **4.6.0.3 – Offline mode (graceful degradation, local queue)**
File: `docs/65-extension-sync/03-offline-mode-and-local-queue.md`


#### 4.6.1 – Real‑Time Sync

- **4.6.1.1 – Sync with Contact360 backend (background periodic sync)**
File: `docs/65-extension-sync/04-background-sync-to-backend.md`
- **4.6.1.2 – Push notifications from backend (new contact added, enriched)**
File: `docs/65-extension-sync/05-push-notifications-from-backend.md`
- **4.6.1.3 – Conflict resolution (user added contact on web, extension has local copy)**
File: `docs/65-extension-sync/06-sync-conflict-resolution.md`


#### 4.6.2 – Data Export from Extension

- **4.6.2.1 – Export cache to file (for debugging, user request)**
File: `docs/65-extension-sync/07-extension-cache-export.md`
- **4.6.2.2 – Activity log in extension (all actions taken via popup)**
File: `docs/65-extension-sync/08-extension-activity-log.md`

***

### 4.7.x – Extension Analytics \& Instrumentation

#### 4.7.0 – Telemetry \& Tracking

- **4.7.0.1 – Extension event tracking (popup open, enrichment triggered, add to CRM)**
File: `docs/66-extension-analytics/01-extension-event-tracking.md`
- **4.7.0.2 – Performance metrics (enrichment latency, popup render time)**
File: `docs/66-extension-analytics/02-extension-performance-metrics.md`
- **4.7.0.3 – User engagement analytics (active users, daily active usage)**
File: `docs/66-extension-analytics/03-extension-engagement-analytics.md`


#### 4.7.1 – Error Tracking \& Debugging

- **4.7.1.1 – Error logging \& reporting (Sentry, Rollbar)**
File: `docs/66-extension-analytics/04-extension-error-logging.md`
- **4.7.1.2 – Debug mode (verbose logs, local storage inspection)**
File: `docs/66-extension-analytics/05-extension-debug-mode.md`
- **4.7.1.3 – User support \& troubleshooting (reproduce user issues)**
File: `docs/66-extension-analytics/06-extension-troubleshooting-support.md`

***

### 4.8.x – Multi-Site \& Cross-Platform Support

#### 4.8.0 – Multi-Site Content Scripts

- **4.8.0.1 – Content script for LinkedIn.com (profile, search, feed)**
File: `docs/67-multi-site/01-linkedin-content-script.md`
- **4.8.0.2 – Content script for Gmail (compose, inbox, email view)**
File: `docs/67-multi-site/02-gmail-content-script.md`
- **4.8.0.3 – Content script for other sites (HubSpot, Salesforce, Outreach, Apollo)**
File: `docs/67-multi-site/03-generic-content-script-framework.md`


#### 4.8.1 – Site-Specific Adapters

- **4.8.1.1 – HubSpot CRM integration (extract contact, auto-sync)**
File: `docs/67-multi-site/04-hubspot-integration-adapter.md`
- **4.8.1.2 – Salesforce integration (contact lookup, match-to-lead)**
File: `docs/67-multi-site/05-salesforce-integration-adapter.md`
- **4.8.1.3 – Outreach/Apollo integration (detect contact, enrich, log call)**
File: `docs/67-multi-site/06-outreach-apollo-integration-adapter.md`


#### 4.8.2 – Platform Consistency

- **4.8.2.1 – UI consistency across sites (same popup design, same actions)**
File: `docs/67-multi-site/07-ui-consistency-across-sites.md`
- **4.8.2.2 – Feature parity (all sites get same enrichment, same logging)**
File: `docs/67-multi-site/08-feature-parity-across-sites.md`
- **4.8.2.3 – A/B testing across sites (test UI changes, feature flags)**
File: `docs/67-multi-site/09-ab-testing-across-sites.md`

***

### 4.9.x – Sales Navigator Maturity \& Advanced Features

#### 4.9.0 – Advanced Sales Navigator Features

- **4.9.0.1 – Competitor tracking (monitor competitor accounts, hiring)**
File: `docs/68-sales-navigator-advanced/01-competitor-tracking.md`
- **4.9.0.2 – Account expansion plays (upsell, cross-sell signals)**
File: `docs/68-sales-navigator-advanced/02-account-expansion-plays.md`
- **4.9.0.3 – Multi-threading (find all stakeholders in company, build network)**
File: `docs/68-sales-navigator-advanced/03-multi-threading-orchestration.md`


#### 4.9.1 – Buying Signals \& Alerts

- **4.9.1.1 – Real-time buying signal alerts (company raised funding, new exec)**
File: `docs/68-sales-navigator-advanced/04-realtime-buying-signal-alerts.md`
- **4.9.1.2 – Market expansion signals (new office, new market entry)**
File: `docs/68-sales-navigator-advanced/05-market-expansion-signals.md`
- **4.9.1.3 – Trigger-based automations (job change → send email, new hire → add to list)**
File: `docs/68-sales-navigator-advanced/06-trigger-based-automations.md`


#### 4.9.2 – AI-Powered Sales Navigator

- **4.9.2.1 – AI-generated outreach templates (personalized per contact)**
File: `docs/68-sales-navigator-advanced/07-ai-generated-outreach-templates.md`
- **4.9.2.2 – AI-recommended next steps (based on profile, engagement history)**
File: `docs/68-sales-navigator-advanced/08-ai-recommended-next-steps.md`
- **4.9.2.3 – AI conversation starters (icebreaker suggestions)**
File: `docs/68-sales-navigator-advanced/09-ai-conversation-starters.md`

***

### 4.10.x – Extension Compliance, Privacy \& Legal

#### 4.10.0 – Privacy \& Data Protection

- **4.10.0.1 – User privacy policy \& consent (extension collects what, shares what)**
File: `docs/69-extension-compliance/01-extension-privacy-policy.md`
- **4.10.0.2 – Data minimization (scrape only what needed, delete after use)**
File: `docs/69-extension-compliance/02-data-minimization-strategy.md`
- **4.10.0.3 – GDPR \& CCPA compliance (user rights, data deletion)**
File: `docs/69-extension-compliance/03-extension-gdpr-ccpa-compliance.md`


#### 4.10.1 – Third-Party ToS Compliance

- **4.10.1.1 – LinkedIn ToS review \& compliance (scraping allowed? Detection risk?)**
File: `docs/69-extension-compliance/04-linkedin-tos-review.md`
- **4.10.1.2 – Gmail API ToS compliance (what we can access, use, share)**
File: `docs/69-extension-compliance/05-gmail-api-tos-compliance.md`
- **4.10.1.3 – HubSpot/Salesforce/others ToS (what integrations are allowed)**
File: `docs/69-extension-compliance/06-3rd-party-tos-compliance.md`


#### 4.10.2 – Extension Security \& Trust

- **4.10.2.1 – Chrome Web Store review process (what's required to publish)**
File: `docs/69-extension-compliance/07-chrome-web-store-review.md`
- **4.10.2.2 – Security headers \& XSS prevention (extension popup injection safety)**
File: `docs/69-extension-compliance/08-extension-security-headers.md`
- **4.10.2.3 – User trust \& transparency (why request this permission, how is data used)**
File: `docs/69-extension-compliance/09-user-trust-and-transparency.md`

***

### 4.11.x – Testing, QA \& Release

#### 4.11.0 – Extension Testing Strategy

- **4.11.0.1 – Unit tests for content scripts (DOM parsing, data extraction)**
File: `docs/70-extension-testing/01-content-script-unit-tests.md`
- **4.11.0.2 – Integration tests (extension ↔ API, local storage, OAuth)**
File: `docs/70-extension-testing/02-extension-integration-tests.md`
- **4.11.0.3 – E2E tests (real LinkedIn profile, Gmail inbox, full flow)**
File: `docs/70-extension-testing/03-extension-e2e-tests.md`


#### 4.11.1 – Manual QA \& Browser Testing

- **4.11.1.1 – Browser compatibility (Chrome, Edge, Brave, other Chromium)**
File: `docs/70-extension-testing/04-browser-compatibility-matrix.md`
- **4.11.1.2 – Manual QA checklist (popup renders, enrichment works, data saved)**
File: `docs/70-extension-testing/05-manual-qa-checklist.md`
- **4.11.1.3 – Regression testing (update doesn't break existing flows)**
File: `docs/70-extension-testing/06-regression-testing-protocol.md`


#### 4.11.2 – Release \& Versioning

- **4.11.2.1 – Extension versioning \& changelog (semver, what's new per version)**
File: `docs/70-extension-testing/07-extension-versioning-and-changelog.md`
- **4.11.2.2 – Release process (test → Chrome Web Store → auto-update)**
File: `docs/70-extension-testing/08-extension-release-process.md`
- **4.11.2.3 – Rollback strategy (if new version breaks, revert)**
File: `docs/70-extension-testing/09-extension-rollback-strategy.md`

***

### 4.12.x – Observability, Monitoring \& Support

#### 4.12.0 – Metrics \& SLOs

- **4.12.0.1 – Extension install/active user metrics (DAU, retention, churn)**
File: `docs/71-extension-observability/01-extension-install-and-dau-metrics.md`
- **4.12.0.2 – Enrichment success SLOs (latency, success rate, accuracy)**
File: `docs/71-extension-observability/02-extension-enrichment-slos.md`
- **4.12.0.3 – API integration SLOs (sync latency, backend uptime)**
File: `docs/71-extension-observability/03-extension-api-slos.md`


#### 4.12.1 – User Support \& Help

- **4.12.1.1 – FAQ \& troubleshooting (common issues, debugging steps)**
File: `docs/71-extension-observability/04-extension-faq-and-troubleshooting.md`
- **4.12.1.2 – Support portal (link from extension settings)**
File: `docs/71-extension-observability/05-extension-support-portal.md`
- **4.12.1.3 – Feedback collection (in-extension survey, feature requests)**
File: `docs/71-extension-observability/06-extension-feedback-collection.md`


#### 4.12.2 – Runbooks \& Incident Response

- **4.12.2.1 – LinkedIn scraping broken (LinkedIn changed selectors)**
File: `docs/71-extension-observability/07-linkedin-scraping-failure-runbook.md`
- **4.12.2.2 – Gmail OAuth token expired (refresh fails)**
File: `docs/71-extension-observability/08-gmail-oauth-failure-runbook.md`
- **4.12.2.3 – High enrichment failure rate (API issues, provider down)**
File: `docs/71-extension-observability/09-high-enrichment-failure-runbook.md`

***

If you'd like, the next step can be:

- a **bash script** to scaffold this `docs/` structure and empty files, or
- taking one deep slice (e.g. **4.2.x LinkedIn Extraction**, **4.3.x Gmail Integration**, **4.5.x Popup UI**, or **4.4.x Sales Navigator**) and turning it into a detailed, implementation-ready checklist with content script examples, API specs, and UI mockups.
<span style="display:none">[^1][^2]</span>

<div align="center">⁂</div>

[^1]: Pasted-text.txt

[^2]: deep-research-report-1.md

