# Contact360 Hooks, Services, Contexts, and Utilities

Complete catalog of all custom React hooks, GraphQL service modules, React context providers, and `lib/` utilities in `contact360.io/app/src/`.

**Related:** `docs/frontend.md` (overview), `docs/frontend/components.md` (component catalog), `docs/frontend/design-system.md` (design system)

---

## React Contexts

Contexts are defined in `context/` and provided at the root of the authenticated app.

### `AuthContext`
- **File:** `context/AuthContext.tsx`
- **Era:** `0.x` / `1.x`
- **Provides:**
  - `user` — current user object (`id`, `email`, `name`, `role`, `plan`)
  - `token` — current JWT access token
  - `isAuthenticated` — boolean
  - `login(credentials)` — async login, stores token
  - `logout()` — clears token, redirects to `/login`
  - `refreshToken()` — silently refreshes JWT before expiry
- **Consumed by:** All authenticated components, `useSessionGuard`, `graphqlClient`
- **Storage:** Token stored in memory + `localStorage` via `tokenManager`

### `RoleContext`
- **File:** `context/RoleContext.tsx`
- **Era:** `1.x` / `7.x`
- **Provides:**
  - `role` — current user role (`FreeUser` | `ProUser` | `Admin` | `SuperAdmin`)
  - `plan` — current plan name
  - `credits` — current credit balance
  - `isAdmin` — boolean (`Admin` or `SuperAdmin`)
  - `isSuperAdmin` — boolean
  - `hasFeature(featureKey)` — checks plan-based feature access via `featureAccess.ts`
  - `creditBalance` — formatted credit display string
- **Consumed by:** `Sidebar`, `DashboardAccessGate`, `CreditBudgetAlerts`, all gated components
- **Updates:** Refreshed on login, on billing mutations, on credit deduction events

### `ThemeContext`
- **File:** `context/ThemeContext.tsx`
- **Era:** `0.x`
- **Provides:**
  - `theme` — `'light'` | `'dark'`
  - `toggleTheme()` — toggles and persists to `localStorage`
- **Consumed by:** `MainLayout` (applies CSS class to root), profile settings toggle

---

## Custom Hooks

### Auth and session hooks

#### `useLoginForm`
- **File:** `hooks/useLoginForm.ts`
- **Era:** `1.x`
- **Purpose:** Complete login form management: controlled inputs, validation, submit handler.
- **Returns:** `{ email, password, errors, isLoading, handleSubmit, setEmail, setPassword }`
- **Validates:** Email format, password non-empty via `authValidation`
- **On success:** Calls `AuthContext.login()` → redirects via `useAuthRedirect`

#### `useRegisterForm`
- **File:** `hooks/useRegisterForm.ts`
- **Era:** `1.x`
- **Purpose:** Registration form: name, email, password, confirm password. Validates and submits.
- **Returns:** `{ formState, errors, isLoading, handleSubmit, setField }`
- **Validates:** Email format, password strength, password match, terms acceptance

#### `useAuthRedirect`
- **File:** `hooks/useAuthRedirect.ts`
- **Era:** `1.x`
- **Purpose:** Handles post-auth redirect logic (back to original URL or default `/dashboard`).
- **Returns:** `{ redirectAfterLogin() }`
- **Storage:** Uses `sessionStorage` to preserve intended URL across auth flow.

#### `useSessionGuard`
- **File:** `hooks/useSessionGuard.ts`
- **Era:** `1.x`
- **Purpose:** Enforces authenticated session on protected pages. Redirects to `/login` on expiry.
- **Behavior:** Checks token validity on mount and on visibility change; triggers `refreshToken()` before expiry.
- **Returns:** `{ isReady }` — false while checking, true when session confirmed.

#### `useSessions`
- **File:** `hooks/useSessions.ts`
- **Era:** `1.x` / `7.x`
- **Purpose:** Lists all active sessions for the user (device, IP, last active) and provides revoke action.
- **Returns:** `{ sessions, isLoading, revokeSession(sessionId), revokeAllOther() }`
- **Service:** (profile session management endpoint)

---

### Dashboard hooks

#### `useDashboardPage`
- **File:** `hooks/useDashboardPage.ts`
- **Era:** `1.x`
- **Purpose:** Batched data fetch for the dashboard page: user stats (admin only) + recent activities + pending exports.
- **Returns:** `{ stats, activities, pendingExports, isLoading, refetch }`
- **Uses:** `dashboardPageApi` (parallel batch fetch), auto-refetches exports every 60s.

#### `useDashboardPageAccess`
- **File:** `hooks/dashboard/useDashboardPageAccess.ts`
- **Era:** `1.x` / `7.x`
- **Purpose:** Determines what dashboard sections are visible based on user role.
- **Returns:** `{ showStats, showChart, showAdminActions }` booleans
- **Context:** `RoleContext`

#### `useDashboardData`
- **File:** `hooks/useDashboardData.ts`
- **Era:** `1.x`
- **Purpose:** Low-level hook for dashboard chart/stats data. Wraps `adminService` queries.
- **Returns:** `{ statsData, chartData, isLoading, error }`

---

### Email hooks

#### `useEmailFinderSingle`
- **File:** `hooks/useEmailFinderSingle.ts`
- **Era:** `2.x`
- **Purpose:** Complete email finder form: first name, last name, domain inputs + submit handler.
- **Returns:** `{ firstName, lastName, domain, result, isLoading, error, handleSubmit, reset, setField }`
- **Credit check:** Validates credits available before submitting.
- **Service:** `emailService.findEmail()`
- **Validates:** All three fields required; domain format check via `emailUtils`

#### `useEmailVerifierSingle`
- **File:** `hooks/useEmailVerifierSingle.ts`
- **Era:** `2.x`
- **Purpose:** Single email verification form: email input + submit.
- **Returns:** `{ email, result, isLoading, error, handleSubmit, setEmail, reset }`
- **Service:** `emailService.verifyEmail()`
- **Validates:** Email format via `emailValidation`

#### `useEmailVerifierBulk`
- **File:** `hooks/useEmailVerifierBulk.ts`
- **Era:** `2.x`
- **Purpose:** Bulk verifier job state: job tracking, polling, result download.
- **Returns:** `{ jobId, status, progress, results, isPolling, startJob, downloadResults }`
- **Polling:** 10s interval while job is `processing`, stops on `completed`/`failed`.
- **Service:** `jobsService`, `emailService`

---

### Contacts hooks

#### `useContactsPage`
- **File:** `hooks/contacts/useContactsPage.ts`
- **Era:** `3.x`
- **Purpose:** Full contacts page data: list with pagination, filters, and selection state.
- **Returns:** `{ contacts, total, page, pageSize, isLoading, error, selectedIds, setPage, setPageSize, setSelected, refetch }`
- **Uses:** `contactsPageApi` (batched contact list + filter metadata)

#### `useContactsFilters`
- **File:** `hooks/contacts/useContactsFilters.ts`
- **Era:** `3.x`
- **Purpose:** Manages VQL filter state for contacts. Builds VQL query from UI filter values.
- **Returns:** `{ filters, setFilter, clearFilters, vqlQuery, activeFilterCount }`
- **Integration:** `VQLQueryBuilder` component reads and writes this state.

#### `useSavedSearches`
- **File:** `hooks/contacts/useSavedSearches.ts`
- **Era:** `3.x`
- **Purpose:** Load, save, delete saved VQL search filter sets.
- **Returns:** `{ savedSearches, isLoading, save(name, filters), load(id), delete(id) }`
- **Service:** `savedSearchesService`

#### `useContactExport`
- **File:** `hooks/contacts/useContactExport.ts`
- **Era:** `3.x`
- **Purpose:** Initiates and tracks a contacts export job.
- **Returns:** `{ exportJob, startExport(columns, filters), downloadUrl, isExporting }`
- **Service:** `contactsService.exportContacts()`

#### `useContactColumns`
- **File:** `hooks/contacts/useContactColumns.ts`
- **Era:** `3.x`
- **Purpose:** Manages column visibility and order in the contacts table.
- **Returns:** `{ visibleColumns, toggleColumn, reorderColumns, resetColumns }`
- **Persistence:** Column preferences saved to `localStorage`.

---

### Companies hooks

#### `useCompaniesPage`
- **File:** `hooks/companies/useCompaniesPage.ts`
- **Era:** `3.x`
- **Purpose:** Companies page data with pagination, filters, and selection.
- **Returns:** `{ companies, total, page, pageSize, isLoading, selectedIds, setPage, refetch }`
- **Uses:** `companiesPageApi`

#### `useCompaniesFilters`
- **File:** `hooks/companies/useCompaniesFilters.ts`
- **Era:** `3.x`
- **Purpose:** Filter state for companies (industry, size, location, founded year).
- **Returns:** `{ filters, setFilter, clearFilters, activeFilterCount }`

#### `useCompaniesView`
- **File:** `hooks/companies/useCompaniesView.ts`
- **Era:** `3.x`
- **Purpose:** Toggles between list and grid view mode for companies.
- **Returns:** `{ viewMode, setViewMode }` — `'list'` | `'grid'`
- **Persistence:** Stored in `localStorage`.

#### `useCompanyExport`
- **File:** `hooks/companies/useCompanyExport.ts`
- **Era:** `3.x`
- **Purpose:** Company export job creation and status tracking.
- **Returns:** `{ startExport(columns, filters), downloadUrl, isExporting }`

---

### Files and upload hooks

#### `useNewExport`
- **File:** `hooks/useNewExport.ts`
- **Era:** `2.x`
- **Purpose:** Full multipart upload flow: file → S3 → job creation. The main orchestration hook for bulk CSV operations.
- **Returns:** `{ file, uploadProgress, uploadFile, createJob, jobId, step }` — step = `idle | uploading | creating | done`
- **Uses:** `useCsvUpload` (upload step) + `jobsService` (job creation step)
- **Services:** `s3Service` (presigned upload), `jobsService` (create job)

#### `useCsvUpload`
- **File:** `hooks/useCsvUpload.ts`
- **Era:** `2.x`
- **Purpose:** File selection, validation, and multipart S3 upload.
- **Returns:** `{ file, setFile, upload, progress, error, isUploading, uploadedKey }`
- **Validates:** File type (CSV), file size limit, header presence.
- **Service:** `s3Service`

#### `useFilePreview`
- **File:** `hooks/useFilePreview.ts`
- **Era:** `2.x`
- **Purpose:** Fetch and display first N rows of an uploaded file.
- **Returns:** `{ rows, headers, isLoading, error, pageSize, setPageSize }`
- **Service:** `s3Service` (fetch preview via presigned URL or API)

#### `useFiles`
- **File:** `hooks/useFiles.ts`
- **Era:** `2.x`
- **Purpose:** File list management: list, select, delete files from S3 bucket.
- **Returns:** `{ files, selectedFile, setSelectedFile, deleteFile, isLoading, refetch }`
- **Service:** `s3Service`

#### `useBucketMetadata`
- **File:** `hooks/useBucketMetadata.ts`
- **Era:** `2.x`
- **Purpose:** Fetch S3 bucket metadata (total objects, size, prefix tree structure).
- **Returns:** `{ metadata, tree, isLoading }` — `tree` built via `s3TreeUtils`
- **Service:** `s3Service`

#### `useFileStats`
- **File:** `hooks/useFileStats.ts`
- **Era:** `2.x`
- **Purpose:** Fetch per-column statistics for an uploaded CSV file (null %, unique values).
- **Returns:** `{ stats, isLoading }` keyed by column name

---

### Jobs hooks

#### `useJobs`
- **File:** `hooks/useJobs.ts`
- **Era:** `2.x`
- **Purpose:** Job list with status polling. Central hook for the jobs page.
- **Returns:** `{ jobs, isLoading, error, retryJob, cancelJob, refetch, pollingStatus }`
- **Polling:** Active jobs polled every 15s; completed/failed jobs not polled.
- **Service:** `jobsService`

#### `useExpandedJobDetails`
- **File:** `hooks/useExpandedJobDetails.ts`
- **Era:** `2.x`
- **Purpose:** Fetches detailed data for a single expanded job (logs, data sample, stats).
- **Returns:** `{ details, logs, isLoading }` for a given `jobId`

---

### Billing and usage hooks

#### `useBilling`
- **File:** `hooks/useBilling.ts`
- **Era:** `1.x`
- **Purpose:** Complete billing state: available plans, payment submission, payment history.
- **Returns:** `{ plans, currentPlan, history, submitPayment, isSubmitting, paymentStatus }`
- **Service:** `billingService`

#### `useUsage`
- **File:** `hooks/useUsage.ts`
- **Era:** `1.x`
- **Purpose:** Credit balance, usage history, and feature usage data.
- **Returns:** `{ credits, used, limit, history, featureUsage, isLoading }`
- **Service:** `usageService`
- **Formats:** Uses `usageFormatters` for display strings.

#### `useFeatureOverview`
- **File:** `hooks/useFeatureOverview.ts`
- **Era:** `1.x`
- **Purpose:** Feature-level usage summary (how many credits used per feature type).
- **Returns:** `{ features[], totalCreditsUsed, isLoading }`

---

### UI state hooks

#### `useModal`
- **File:** `hooks/useModal.ts`
- **Era:** `0.x`
- **Purpose:** Generic modal lifecycle: open/close state with optional data payload.
- **Returns:** `{ isOpen, open(data?), close, data }`
- **Usage:** `const deleteModal = useModal<Contact>()` — then `deleteModal.open(contactToDelete)`

#### `useViewMode`
- **File:** `hooks/useViewMode.ts`
- **Era:** `3.x`
- **Purpose:** Generic view mode toggle (e.g. list/grid/table).
- **Returns:** `{ viewMode, setViewMode }` with `localStorage` persistence.

#### `useResizablePanels`
- **File:** `hooks/useResizablePanels.ts`
- **Era:** `0.x`
- **Purpose:** Two-panel resize logic via mouse drag on `ResizeHandle`.
- **Returns:** `{ leftWidth, onDragStart }` — bind to `ResizeHandle`'s drag events.

#### `useSidebar`
- **File:** `hooks/useSidebar.ts`
- **Era:** `0.x`
- **Purpose:** Sidebar collapsed/expanded state with `localStorage` persistence.
- **Returns:** `{ isCollapsed, toggle, setCollapsed }`

#### `useDebouncedValue`
- **File:** `hooks/useDebouncedValue.ts`
- **Era:** `0.x`
- **Purpose:** Returns a debounced copy of a value, updated after `delay` ms of no changes.
- **Returns:** `debouncedValue`
- **Usage:** `const debouncedSearch = useDebouncedValue(searchInput, 300)`

---

### Platform and admin hooks

#### `useAnalytics`
- **File:** `hooks/useAnalytics.ts`
- **Era:** `8.x`
- **Purpose:** Fetch analytics data for dashboards and reports.
- **Returns:** `{ analyticsData, chartData, isLoading, dateRange, setDateRange }`
- **Service:** `analyticsService`

#### `useAdmin`
- **File:** `hooks/useAdmin.ts`
- **Era:** `1.x` / `7.x`
- **Purpose:** Admin actions: view users, adjust credits, review payments.
- **Returns:** `{ users, adjustCredits, paymentSubmissions, approvePayment, declinePayment, isLoading }`
- **Service:** `adminService`
- **Role gate:** Only usable by Admin/SuperAdmin (`RoleContext.isAdmin`)

#### `useTeam`
- **File:** `hooks/useTeam.ts`
- **Era:** `1.x`
- **Purpose:** Team member management: list, invite, update role, remove.
- **Returns:** `{ members, inviteMember, updateRole, removeMember, isLoading }`
- **Service:** `usersService`

#### `useLinkedIn`
- **File:** `hooks/useLinkedIn.ts`
- **Era:** `4.x`
- **Purpose:** LinkedIn/Sales Navigator integration state: profile sync, ingestion status.
- **Returns:** `{ linkedInProfile, syncStatus, triggerSync, isConnected }`
- **Service:** `linkedinService`

#### `useAPIKeys`
- **File:** `hooks/useAPIKeys.ts`
- **Era:** `8.x`
- **Purpose:** API key management: list, create, revoke.
- **Returns:** `{ apiKeys, createKey, revokeKey, isLoading }`
- **Service:** (profile / API key management endpoint)

#### `useActivities`
- **File:** `hooks/useActivities.ts`
- **Era:** `1.x`
- **Purpose:** Activity log with filtering and pagination.
- **Returns:** `{ activities, stats, filter, setFilter, page, setPage, isLoading }`
- **Service:** `activitiesService`

#### `useCompanies`
- **File:** `hooks/useCompanies.ts`
- **Era:** `3.x`
- **Purpose:** Top-level company data hook (lighter alternative to `useCompaniesPage`).
- **Returns:** `{ companies, isLoading, searchCompanies }`

---

## GraphQL Services

All services are in `services/graphql/` and use `graphqlClient` to execute typed GraphQL operations.

### `authService`
- **File:** `services/graphql/authService.ts`
- **Era:** `1.x`
- **Operations:**
  - `Login(email, password)` → `{ token, user }`
  - `Register(name, email, password)` → `{ token, user }`
  - `Logout()` → `{ success }`
  - `RefreshToken(refreshToken)` → `{ token }`
  - `ValidateToken()` → `{ user }` (used on app boot)

### `billingService`
- **File:** `services/graphql/billingService.ts`
- **Era:** `1.x`
- **Operations:**
  - `GetPlans()` → `Plan[]`
  - `GetCreditPacks()` → `CreditPack[]`
  - `CreatePayment(planId, proof)` → `{ paymentId, status }`
  - `GetPaymentHistory(page, pageSize)` → `Payment[]`
  - `ApprovePayment(paymentId)` → `{ success }` (admin)
  - `DeclinePayment(paymentId, reason)` → `{ success }` (admin)

### `contactsService`
- **File:** `services/graphql/contactsService.ts`
- **Era:** `3.x`
- **Operations:**
  - `ListContacts(filters, page, pageSize, sort)` → `{ contacts, total }`
  - `GetContact(id)` → `Contact`
  - `CreateContact(input)` → `Contact`
  - `UpdateContact(id, input)` → `Contact`
  - `DeleteContact(id)` → `{ success }`
  - `BulkDeleteContacts(ids[])` → `{ deletedCount }`
  - `ExportContacts(filters, columns)` → `{ jobId }`
  - `ImportContacts(fileKey, mapping)` → `{ jobId }`

### `companiesService`
- **File:** `services/graphql/companiesService.ts`
- **Era:** `3.x`
- **Operations:**
  - `ListCompanies(filters, page, pageSize, sort)` → `{ companies, total }`
  - `GetCompany(id)` → `Company`
  - `CreateCompany(input)` → `Company`
  - `UpdateCompany(id, input)` → `Company`
  - `DeleteCompany(id)` → `{ success }`
  - `ExportCompanies(filters, columns)` → `{ jobId }`
  - `ImportCompanies(fileKey, mapping)` → `{ jobId }`

### `emailService`
- **File:** `services/graphql/emailService.ts`
- **Era:** `2.x`
- **Operations:**
  - `FindEmail(firstName, lastName, domain)` → `{ emails[], bestEmail, confidence }`
  - `VerifyEmail(email)` → `{ status, confidence, checks{dns, smtp, spf, dmarc} }`
  - `BulkVerifyEmail(jobId)` → `{ jobId }` (triggers bulk job)
  - `GetEmailHistory(page, pageSize)` → `EmailHistoryItem[]`

### `jobsService`
- **File:** `services/graphql/jobsService.ts`
- **Era:** `2.x`
- **Operations:**
  - `CreateJob(type, fileKey, mapping, options)` → `{ jobId }`
  - `GetJob(jobId)` → `Job` (with status, progress, stats)
  - `ListJobs(status?, page, pageSize)` → `{ jobs, total }`
  - `RetryJob(jobId, scope)` → `{ success }`
  - `CancelJob(jobId)` → `{ success }`
  - `ScheduleJob(jobId, schedule)` → `{ success }`
  - `GetJobLogs(jobId, page)` → `LogEntry[]`
  - `GetJobData(jobId, page)` → `DataRow[]`

### `usageService`
- **File:** `services/graphql/usageService.ts`
- **Era:** `1.x`
- **Operations:**
  - `Usage()` → `{ credits, used, limit, plan }`
  - `GetUsageHistory(dateRange)` → `UsageHistoryItem[]`
  - `GetFeatureUsage()` → `FeatureUsageItem[]`

### `profileService`
- **File:** `services/graphql/profileService.ts`
- **Era:** `1.x`
- **Operations:**
  - `GetProfile()` → `Profile`
  - `UpdateProfile(input)` → `Profile`
  - `ChangePassword(current, new)` → `{ success }`
  - `UpdateAvatar(imageData)` → `{ avatarUrl }`

### `adminService`
- **File:** `services/graphql/adminService.ts`
- **Era:** `1.x` / `7.x`
- **Operations:**
  - `UserStats()` → `{ total, active, byRole, byPlan }`
  - `ListUsers(page, pageSize, filters)` → `{ users, total }`
  - `AdjustCredits(userId, amount, reason)` → `{ success }`
  - `ListPaymentSubmissions(status)` → `PaymentSubmission[]`
  - `ApprovePaymentSubmission(id)` → `{ success }`

### `activitiesService`
- **File:** `services/graphql/activitiesService.ts`
- **Era:** `1.x`
- **Operations:**
  - `GetActivities(filters, page, pageSize)` → `{ activities, total }`
  - `GetActivityStats()` → `ActivityStats`

### `analyticsService`
- **File:** `services/graphql/analyticsService.ts`
- **Era:** `8.x`
- **Operations:**
  - `GetAnalytics(dateRange)` → `AnalyticsData`
  - `GetUserAnalytics(userId, dateRange)` → `UserAnalytics`
  - `GetAdminAnalytics(dateRange)` → `AdminAnalytics`

### `savedSearchesService`
- **File:** `services/graphql/savedSearchesService.ts`
- **Era:** `3.x`
- **Operations:**
  - `ListSavedSearches()` → `SavedSearch[]`
  - `CreateSavedSearch(name, filters)` → `SavedSearch`
  - `DeleteSavedSearch(id)` → `{ success }`

### `linkedinService`
- **File:** `services/graphql/linkedinService.ts`
- **Era:** `4.x`
- **Operations:**
  - `GetLinkedInProfile(url)` → `LinkedInProfile`
  - `SyncSalesNavigator(profileData)` → `{ contact }`

### `s3Service`
- **File:** `services/graphql/s3Service.ts`
- **Era:** `2.x`
- **Operations:**
  - `GetPresignedUploadUrl(filename, contentType)` → `{ uploadUrl, key }`
  - `ListBucketObjects(prefix?, maxKeys?)` → `S3Object[]`
  - `GetPresignedDownloadUrl(key)` → `{ downloadUrl }`
  - `DeleteObject(key)` → `{ success }`

### `twoFactorService`
- **File:** `services/graphql/twoFactorService.ts`
- **Era:** `1.x` / `7.x`
- **Operations:**
  - `EnableTwoFactor()` → `{ qrCode, secret }`
  - `VerifyAndEnableTwoFactor(otp)` → `{ success, backupCodes[] }`
  - `DisableTwoFactor(otp)` → `{ success }`
  - `ValidateOTP(otp)` → `{ success }`

### `usersService`
- **File:** `services/graphql/usersService.ts`
- **Era:** `1.x` / `7.x`
- **Operations:**
  - `ListUsers(page, pageSize)` → `User[]`
  - `GetUser(id)` → `User`
  - `InviteUser(email, role)` → `{ success }`
  - `UpdateUserRole(userId, role)` → `User`
  - `RemoveUser(userId)` → `{ success }`

### `healthService`
- **File:** `services/graphql/healthService.ts`
- **Era:** `6.x`
- **Operations:**
  - `Health()` → `{ status, version }` (API connectivity check)

---

## Library Utilities (`lib/`)

### Core runtime

#### `graphqlClient`
- **File:** `lib/graphqlClient.ts`
- **Purpose:** HTTP GraphQL client wrapper. Injects auth token, handles network errors, and parses GraphQL errors.
- **Key exports:**
  - `gqlQuery<T>(query, variables?)` → `T`
  - `gqlMutation<T>(mutation, variables?)` → `T`
- **Error handling:** Throws typed `ApiError` (from `apiErrorTypes.ts`) on HTTP or GraphQL errors.
- **Token injection:** Reads token from `tokenManager` per request.

#### `config`
- **File:** `lib/config.ts`
- **Purpose:** App environment configuration object.
- **Key exports:** `API_URL`, `GRAPHQL_URL`, `APP_ENV`, `FEATURE_FLAGS`
- **Source:** `NEXT_PUBLIC_*` env vars, validated at build time.

#### `constants`
- **File:** `lib/constants.ts`
- **Purpose:** App-wide constant values used across multiple modules.
- **Includes:** Credit deduction values, pagination defaults, API limits, status values, role names.

#### `featureAccess`
- **File:** `lib/featureAccess.ts`
- **Purpose:** Plan-based feature access check function.
- **Key exports:**
  - `hasFeature(plan, featureKey)` → `boolean`
  - `FEATURE_KEYS` — enum of all gated feature keys
- **Used by:** `RoleContext`, all gated UI components

#### `utils`
- **File:** `lib/utils.ts`
- **Purpose:** General utility functions shared across the codebase.
- **Key exports:** `cn(...)` (classnames merge), `formatDate(date, format)`, `truncate(str, len)`, `debounce(fn, delay)`, `sleep(ms)`

#### `toast`
- **File:** `lib/toast.ts`
- **Purpose:** Imperative toast notification helper.
- **Key exports:**
  - `toast.success(message)`, `toast.error(message)`, `toast.info(message)`, `toast.warning(message)`
  - `toast.dismiss(id)`

#### `clipboard`
- **File:** `lib/clipboard.ts`
- **Purpose:** Copy text to clipboard with success callback.
- **Key exports:** `copyToClipboard(text, onSuccess?)` — uses `navigator.clipboard.writeText` with fallback.

#### `animationsConfig`
- **File:** `lib/animationsConfig.ts`
- **Purpose:** Shared animation presets (Framer Motion or CSS config).
- **Exports:** `fadeIn`, `slideUp`, `scaleIn`, `staggerChildren` — used by layout and modal components.

---

### Auth and session utilities

#### `tokenManager`
- **File:** `lib/tokenManager.ts`
- **Purpose:** JWT token storage, retrieval, and expiry checking.
- **Key exports:**
  - `setToken(token)`, `getToken()`, `clearToken()`
  - `isTokenExpired(token)` — reads JWT `exp` claim
  - `getTokenPayload(token)` → decoded payload

#### `sessionManager`
- **File:** `lib/sessionManager.ts`
- **Purpose:** Session lifecycle management (start, end, heartbeat).
- **Key exports:** `startSession()`, `endSession()`, `extendSession()`

#### `sessionUtils`
- **File:** `lib/profile/sessionUtils.ts`
- **Purpose:** Session data formatting helpers.
- **Key exports:** `formatDevice(session)`, `formatLastActive(session)`, `isCurrentSession(session)`

#### `authValidation`
- **File:** `lib/authValidation.ts`
- **Purpose:** Auth form field validation rules.
- **Key exports:**
  - `validateEmail(email)` → `string | null` (error message or null)
  - `validatePassword(password)` → `string | null`
  - `validatePasswordMatch(p1, p2)` → `string | null`
  - `validateName(name)` → `string | null`

#### `authErrorHandler`
- **File:** `lib/authErrorHandler.ts`
- **Purpose:** Maps authentication error codes to user-facing messages.
- **Key exports:** `getAuthErrorMessage(error)` → localized string

#### `apiErrorHandler`
- **File:** `lib/apiErrorHandler.ts`
- **Purpose:** Maps GraphQL/HTTP errors to toast messages and decides retry behavior.
- **Key exports:** `handleApiError(error)` — calls `toast.error(message)` with appropriate message.

#### `apiErrorTypes`
- **File:** `lib/apiErrorTypes.ts`
- **Purpose:** TypeScript type definitions for API errors.
- **Exports:** `ApiError`, `GraphQLError`, `NetworkError`, `AuthError`, `ValidationError`

---

### Domain utilities

#### `emailUtils`
- **File:** `lib/email/emailUtils.ts`
- **Purpose:** Email display and manipulation helpers.
- **Key exports:**
  - `formatEmail(email)` — lowercase, trim
  - `extractDomain(email)` → domain string
  - `isDisposable(email)` — basic disposable check
  - `generatePatterns(firstName, lastName, domain)` → candidate emails

#### `emailValidation`
- **File:** `lib/email/emailValidation.ts`
- **Purpose:** Email field validation for forms.
- **Key exports:**
  - `validateEmailInput(email)` → `string | null`
  - `validateDomain(domain)` → `string | null`
  - `validateEmailFinderInputs(firstName, lastName, domain)` → `Record<string, string | null>`

#### `jobsMapper`
- **File:** `lib/jobs/jobsMapper.ts`
- **Purpose:** Maps raw API job objects to typed UI models.
- **Key exports:** `mapJob(apiJob)` → `UIJob`, `mapJobList(apiJobs)` → `UIJob[]`

#### `jobsUtils`
- **File:** `lib/jobs/jobsUtils.ts`
- **Purpose:** Job display helpers (status label, status color, action availability).
- **Key exports:** `getStatusLabel(status)`, `getStatusColor(status)`, `canRetry(job)`, `canCancel(job)`

#### `jobsValidation`
- **File:** `lib/jobs/jobsValidation.ts`
- **Purpose:** Job creation form validation.
- **Key exports:** `validateJobInput(input)` → `ValidationErrors`

#### `jobsConstants`
- **File:** `lib/jobs/jobsConstants.ts`
- **Purpose:** Job status values, types, and limit constants.
- **Exports:** `JOB_STATUS` enum, `JOB_TYPE` enum, `MAX_CONCURRENT_FINDER_STREAMS = 3`, `MAX_CONCURRENT_VERIFIER_STREAMS = 5`

#### `contactsUtils`
- **File:** `lib/contacts/contactsUtils.ts`
- **Purpose:** Contact display and manipulation helpers.
- **Key exports:** `formatContactName(contact)`, `getContactInitials(contact)`, `contactToCSVRow(contact)`

#### `contactsConstants`
- **File:** `lib/contacts/contactsConstants.ts`
- **Purpose:** Contact field names, filter option values.
- **Exports:** `CONTACT_FIELDS`, `SENIORITY_OPTIONS`, `INDUSTRY_OPTIONS`, `COMPANY_SIZE_OPTIONS`

#### `usageFormatters`
- **File:** `lib/usageFormatters.ts`
- **Purpose:** Credit and usage display formatting.
- **Key exports:** `formatCredits(n)` → e.g. "1,234 credits", `formatPercent(used, total)` → "73%", `creditBalanceColor(pct)`

#### `dashboardMapper`
- **File:** `lib/dashboardMapper.ts`
- **Purpose:** Maps dashboard API responses to chart/display models.
- **Key exports:** `mapStatsToCards(stats)`, `mapToChartData(activities)`

#### `dashboardConstants`
- **File:** `lib/dashboardConstants.ts`
- **Purpose:** Dashboard stat labels, chart configuration defaults.
- **Exports:** `STATS_CONFIG`, `CHART_DEFAULTS`, `REFRESH_INTERVAL_MS = 60000`

#### `activitiesConstants`
- **File:** `lib/activitiesConstants.ts`
- **Purpose:** Activity type labels and icon mapping.
- **Exports:** `ACTIVITY_LABELS`, `ACTIVITY_ICONS`, `ACTIVITY_COLORS` keyed by `ActivityType`

#### `s3TreeUtils`
- **File:** `lib/s3/s3TreeUtils.ts`
- **Purpose:** Builds a tree structure from S3 object key prefixes for file browser display.
- **Key exports:** `buildTree(keys[])` → nested tree node object

---

### Page API layer

#### `pageApi`
- **File:** `lib/api/pageApi.ts`
- **Purpose:** Base helper for parallel-batched GraphQL fetches. Runs multiple queries concurrently and returns a combined result.
- **Key exports:** `batchFetch<T>(queries[])` → `T` (combined result object)

#### `queryBuilder`
- **File:** `lib/api/queryBuilder.ts`
- **Purpose:** Dynamically composes GraphQL query strings from field configurations.
- **Key exports:** `buildQuery(fields, operation)` → GraphQL query string

#### `dashboardPageApi`
- **File:** `lib/api/pages/dashboardPageApi.ts`
- **Purpose:** Batched dashboard page fetch (stats + activities + exports in parallel).
- **Used by:** `useDashboardPage`

#### `contactsPageApi`
- **File:** `lib/api/pages/contactsPageApi.ts`
- **Purpose:** Batched contacts page fetch (contact list + filter metadata in parallel).
- **Used by:** `useContactsPage`

#### `companiesPageApi`
- **File:** `lib/api/pages/companiesPageApi.ts`
- **Purpose:** Batched companies page fetch (company list + filter metadata in parallel).
- **Used by:** `useCompaniesPage`

---

## UI copy

#### `copy`
- **File:** `text/copy.ts`
- **Purpose:** Centralized UI text strings (labels, messages, placeholder text, empty states).
- **Usage:** Import named strings for consistent, maintainable copy.
- **Examples:** `COPY.EMPTY_CONTACTS`, `COPY.LOW_CREDIT_MESSAGE`, `COPY.JOB_PROCESSING_LABEL`

---

## Quick reference — hook × service × context

| Hook | Uses service | Uses context |
| --- | --- | --- |
| `useLoginForm` | `authService` | — |
| `useRegisterForm` | `authService` | — |
| `useSessionGuard` | — | `AuthContext` |
| `useDashboardPage` | `adminService`, `activitiesService`, `jobsService` | `RoleContext` |
| `useEmailFinderSingle` | `emailService` | `RoleContext` (credits) |
| `useEmailVerifierSingle` | `emailService` | — |
| `useContactsPage` | `contactsService` | — |
| `useContactsFilters` | — | — (state only) |
| `useSavedSearches` | `savedSearchesService` | — |
| `useContactExport` | `contactsService` | — |
| `useCompaniesPage` | `companiesService` | — |
| `useNewExport` | `s3Service`, `jobsService` | — |
| `useCsvUpload` | `s3Service` | — |
| `useJobs` | `jobsService` | — |
| `useBilling` | `billingService` | — |
| `useUsage` | `usageService` | `RoleContext` |
| `useAdmin` | `adminService` | `RoleContext` |
| `useAnalytics` | `analyticsService` | — |
| `useAPIKeys` | (profile API) | `AuthContext` |
| `useLinkedIn` | `linkedinService` | — |
| `useTeam` | `usersService` | `RoleContext` |

---

## Related docs

- `docs/frontend.md` — frontend map and overview
- `docs/frontend/components.md` — per-era component catalog
- `docs/frontend/design-system.md` — design tokens and UI patterns
- `docs/flowchart.md` — user journey and data flow diagrams

## Hook/service/context metadata normalization

Each hook, service, and context entry should include:

- `era`
- `introduced_in`
- `graphql_bindings`
- `surface_bindings`

## Marketing hooks (`contact360.io/root/src/hooks`)

| Hook | Path | Purpose | Era |
| --- | --- | --- | --- |
| `useMarketingPage` | `contact360.io/root/src/hooks/marketing/useMarketingPage.ts` | fetch and bind marketing page content | `0.x` |
| `useMarketingPages` | `contact360.io/root/src/hooks/marketing/useMarketingPages.ts` | page collection retrieval and filtering | `0.x` |
| `useDocumentation` | `contact360.io/root/src/hooks/useDocumentation.ts` | docs content retrieval for marketing/docs views | `8.x` |
| `useLandingContent` | `contact360.io/root/src/hooks/useLandingContent.ts` | landing section data wiring | `0.x` |
| `usePricing` | `contact360.io/root/src/hooks/usePricing.ts` | pricing plan and package data binding | `1.x` |
| `useUsageTracking` | `contact360.io/root/src/hooks/useUsageTracking.ts` | usage analytics events and counters | `1.x` |
| `useSessionGuard` | `contact360.io/root/src/hooks/useSessionGuard.ts` | auth session checks for guarded paths | `1.x` |
| `useForceLightTheme` | `contact360.io/root/src/hooks/common/useForceLightTheme.ts` | force light theme in marketing routes | `0.x` |
| `useAuthForm` | `contact360.io/root/src/hooks/auth/useAuthForm.ts` | shared auth form state/validation | `1.x` |
| `useDebounce` | `contact360.io/root/src/hooks/useDebounce.ts` | debounced search/input interactions | `0.x` |
| `useReveal` | `contact360.io/root/src/hooks/useReveal.ts` | reveal-on-scroll/visibility transitions | `0.x` |
| `useToast` | `contact360.io/root/src/hooks/useToast.ts` | toast state and notification behavior | `1.x` |

## Marketing GraphQL services (`contact360.io/root/src/services/graphql`)

| Service | Operations focus | Era |
| --- | --- | --- |
| `marketingService` | page/section marketing content | `0.x` |
| `pagesService` | page metadata and content blocks | `0.x` |
| `documentationService` | documentation fetch and categorization | `8.x` |
| `authService` | login/register/session operations | `1.x` |
| `billingService` | pricing/plan and billing state reads | `1.x` |
| `usageService` | usage and quota reads | `1.x` |
| `notificationsService` | notification retrieval/preferences | `1.x` |
| `exportsService` | export job metadata reads | `2.x` |
| `healthService` | service health/status checks | `6.x` |
| (testing) `usageService.test` | usage contract behavior tests | `1.x` |

## Admin surface equivalents (`contact360.io/admin`)

The admin surface is Django-template driven, so React hooks are replaced by view/controller and client patterns:

| Concern | Admin implementation equivalent |
| --- | --- |
| state and access gating | Django auth/session + decorators (`require_super_admin`, `require_admin_or_super_admin`) |
| service access | Python GraphQL clients (`graphql_client.py`, `appointment360_client.py`, `admin_client.py`) |
| UI interaction controllers | static JS component controllers under `static/js/components/` |
| context-like global behavior | template base shell + navigation constants (`SIDEBAR_MENU`) + server-rendered view context |

## Cross-surface flow mapping pattern

- `root`: hook -> GraphQL service -> gateway read/auth CTA flow
- `app`: hook -> GraphQL service -> page API aggregation -> dashboard UI states
- `admin`: Django view -> Python GraphQL client/service -> template/static JS components


---

## Extension surface — `extension/contact360`

> **Surface type:** Logic/transport utilities (JavaScript, not React). Imported by extension popup/content scripts.

### Auth utilities (`auth/graphqlSession.js`)

| Export | Type | Purpose | Era |
| --- | --- | --- | --- |
| `getValidAccessToken()` | async fn | Proactive token refresh if within 5-min expiry buffer | 1.x–4.x |
| `refreshAccessToken(refreshToken)` | async fn | Calls Appointment360 `auth.refreshToken` mutation; stores result | 1.x |
| `storeTokens({ accessToken, refreshToken })` | async fn | Writes to `chrome.storage.local` | 1.x |
| `getStoredTokens()` | async fn | Reads both tokens from `chrome.storage.local` | 1.x |
| `isTokenExpired(token, bufferSeconds?)` | fn | JWT `exp` check with configurable buffer (default 300 s) | 1.x |
| `decodeJWT(token)` | fn | Pure base64url JWT payload decode; no library | 0.x |

**Context equivalent:** None — functions are standalone utilities called imperatively by content scripts. Mirrors the role of `AuthContext` in the dashboard but without React.

### REST client (`utils/lambdaClient.js`)

| Export | Type | Purpose | Era |
| --- | --- | --- | --- |
| `saveProfiles(profiles[])` | async fn | Batch-save to `POST /v1/save-profiles`; returns `{ saved, errors }` | 3.x |
| `BATCH_SIZE` | const (10) | Max profiles per HTTP request | 3.x |
| `MAX_RETRIES` | const (3) | Retry limit with exponential back-off + jitter | 6.x |
| `buildRequestOptions(token)` | fn | Builds fetch options: auth header, content-type, adaptive timeout | 4.x |
| `pruneProfile(profile)` | fn | Removes `null`/`undefined` keys before serialization | 3.x |

**Hook equivalent:** None — imperative utility. Mirrors the batching/retry pattern found in `useEmailFinderBulk` on the dashboard.

### Data utilities (`utils/profileMerger.js`)

| Export | Type | Purpose | Era |
| --- | --- | --- | --- |
| `deduplicateProfiles(profiles[])` | fn | Groups by `profile_url`; merges each group | 3.x |
| `mergeProfiles(a, b)` | fn | Field-level merge preferring completeness | 3.x |
| `scoreProfile(profile)` | fn | Returns 0–1 completeness float | 3.x |

### Cross-surface mapping

| Pattern | `contact360.io/app` equivalent | `extension/contact360` implementation |
| --- | --- | --- |
| Auth/session | `AuthContext` + `useAuth` hook | `getValidAccessToken()` imperative call |
| API calls | `graphqlService.ts` via `useGraphQLClient` | `lambdaClient.saveProfiles()` REST |
| Data dedup | Server-side Connectra dedup | `deduplicateProfiles()` client-side |
| Token storage | Browser cookie / memory | `chrome.storage.local` |
---

## Email app docs pack — `contact360.io/email`

### Component highlights
- `components/email-list.tsx` — mailbox fetch orchestration, loading/error/empty state.
- `components/data-table.tsx` — tabs, checkbox selection, pagination, row action dropdown.
- `components/app-sidebar.tsx` — folder navigation and user bootstrap.
- `components/nav-user.tsx` — account menu + logout.
- `app/account/[userId]/page.tsx` — profile and IMAP account management.

### Hooks/services/contexts
- `context/imap-context.tsx` — active account context + persistence.
- `hooks/use-mobile.ts` — responsive helper.
- Service access is direct `fetch` using `BACKEND_URL` in `lib/utils.ts`.

### Design system and UX profile
- Dark-theme-first mailbox shell.
- Emphasis on compact table workflows for high-volume email triage.
- Uses shadcn/Radix primitives for consistent tabs/buttons/inputs/checkbox/dropdowns.
