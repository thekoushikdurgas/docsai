# Billing Module

## Overview

The Billing module provides billing and subscription management functionality including subscription plans, addon packages, invoices, and subscription operations.
**Location:** `app/graphql/modules/billing/`

## Queries and mutations – parameters and variable types

| Operation | Parameter(s) | Variable type (GraphQL) | Return type |
|-----------|---------------|-------------------------|-------------|
| **Queries** | | | |
| `billing` | — | — | `BillingInfo` (auth) |
| `plans` | `category`? | String | [SubscriptionPlan] (public) |
| `addons` | — | — | [AddonPackage] (public) |
| `invoices` | `limit`, `offset` | Int, Int | invoice connection |
| **Mutations** (auth) | | | |
| `subscribe` | `input` | SubscribeInput! | subscription result |
| `purchaseAddon` | `input` | PurchaseAddonInput! | result |
| `cancelSubscription` | — | — | result |
| **Admin mutations** (SuperAdmin) | | | |
| `createPlan`, `updatePlan`, `deletePlan` | `input` | plan input! | Plan / result |
| `createPlanPeriod`, `updatePlanPeriod`, `deletePlanPeriod` | `input` | period input! | result |
| `createAddon`, `updateAddon`, `deleteAddon` | `input` | addon input! | result |

Use camelCase in variables. See Input Types and Admin Input Types for field-level details. Razorpay used for payments.

## Types

### BillingInfo

Billing information for a user.

```graphql
type BillingInfo {
  credits: Int!
  creditsUsed: Int!
  creditsLimit: Int!
  subscriptionPlan: String!
  subscriptionPeriod: String
  subscriptionStatus: String!
  subscriptionStartedAt: DateTime
  subscriptionEndsAt: DateTime
  usagePercentage: Float!
}
```

### SubscriptionPlan

Subscription plan with all periods.

```graphql
type SubscriptionPlan {
  tier: String!
  name: String!
  category: String!
  periods: PlanPeriods!
}
```

**Categories:** `STARTER`, `PROFESSIONAL`, `BUSINESS`, `ENTERPRISE`

### PlanPeriods

Container for all subscription plan periods.

```graphql
type PlanPeriods {
  monthly: PlanPeriod
  quarterly: PlanPeriod
  yearly: PlanPeriod
}
```

### PlanPeriod

Subscription plan period pricing.

```graphql
type PlanPeriod {
  period: String!
  credits: Int!
  ratePerCredit: Float!
  price: Float!
  savings: Savings
}
```

**Periods:** `monthly`, `quarterly`, `yearly`

### Savings

Savings information for a plan period.

```graphql
type Savings {
  amount: Float
  percentage: Int
}
```

### AddonPackage

Addon credit package.

```graphql
type AddonPackage {
  id: String!
  name: String!
  credits: Int!
  ratePerCredit: Float!
  price: Float!
}
```

### Invoice

Invoice information.

```graphql
type Invoice {
  id: String!
  amount: Float!
  status: String!
  createdAt: DateTime!
  description: String
}
```

**Status values:** `paid`, `pending`, `failed`

### InvoiceConnection

Paginated connection of invoices.

```graphql
type InvoiceConnection {
  items: [Invoice!]!
  total: Int!
  limit: Int!
  offset: Int!
  hasNext: Boolean!
  hasPrevious: Boolean!
}
```

### SubscribeResult

Result of subscription operation.

```graphql
type SubscribeResult {
  message: String!
  subscriptionPlan: String!
  subscriptionPeriod: String!
  credits: Int!
  subscriptionEndsAt: DateTime
}
```

### PurchaseAddonResult

Result of addon purchase operation.

```graphql
type PurchaseAddonResult {
  message: String!
  package: String!
  creditsAdded: Int!
  totalCredits: Int!
}
```

### CancelSubscriptionResult

Result of subscription cancellation.

```graphql
type CancelSubscriptionResult {
  message: String!
  subscriptionStatus: String!
}
```

## Queries

### billing

Get billing information for the current user.

**Parameters:** None.

```graphql
query GetBilling {
  billing {
    billing {
      credits
      creditsUsed
      creditsLimit
      subscriptionPlan
      subscriptionPeriod
      subscriptionStatus
      subscriptionStartedAt
      subscriptionEndsAt
      usagePercentage
    }
  }
}
```

**Returns:** `BillingInfo`

**Authentication:** Required

**Note:** For SuperAdmin and Admin users, `subscriptionPlan` will return `"unlimited"` since they have unlimited credits and don't require a subscription plan.

**Example Response (Regular User):**

```json
{
  "data": {
    "billing": {
      "billing": {
        "credits": 1000,
        "creditsUsed": 250,
        "creditsLimit": 1000,
        "subscriptionPlan": "pro",
        "subscriptionPeriod": "monthly",
        "subscriptionStatus": "active",
        "subscriptionStartedAt": "2024-01-01T00:00:00Z",
        "subscriptionEndsAt": "2024-02-01T00:00:00Z",
        "usagePercentage": 25.0
      }
    }
  }
}
```

**Example Response (SuperAdmin/Admin User):**

```json
{
  "data": {
    "billing": {
      "billing": {
        "credits": 999999,
        "creditsUsed": 0,
        "creditsLimit": 999999,
        "subscriptionPlan": "unlimited",
        "subscriptionPeriod": null,
        "subscriptionStatus": "active",
        "subscriptionStartedAt": null,
        "subscriptionEndsAt": null,
        "usagePercentage": 0.0
      }
    }
  }
}
```

### plans

Get all available subscription plans with all billing periods.

**Parameters:** None.

```graphql
query GetPlans {
  billing {
    plans {
      tier
      name
      category
      periods {
        monthly {
          period
          credits
          price
          savings {
            amount
            percentage
          }
        }
        yearly {
          period
          credits
          price
          savings {
            amount
            percentage
          }
        }
      }
    }
  }
}
```

**Returns:** `[SubscriptionPlan!]!`

**Authentication:** Not required (public endpoint)

**Implementation Details:**
- Uses hardcoded subscription plans from `SUBSCRIPTION_PLANS` constants for maximum performance
- Bypasses database queries entirely for sub-millisecond response times
- Plans are static data defined in `app/services/billing/constants.py`
- Available tiers: `5k`, `25k`, `100k`, `500k`, `1M`, `5M`, `10M`
- Each tier supports `monthly`, `quarterly`, and `yearly` periods

### addons

Get all available addon credit packages.

**Parameters:** None.

```graphql
query GetAddons {
  billing {
    addons {
      id
      name
      credits
      ratePerCredit
      price
    }
  }
}
```

**Returns:** `[AddonPackage!]!`

**Authentication:** Not required (public endpoint)

**Implementation Details:**
- Tries to fetch from database first (if session provided)
- **Fallback Mechanism**: If database access fails, gracefully falls back to hardcoded addon packages from `ADDON_PACKAGES` constants
- This ensures service availability even if database is temporarily unavailable
- Available packages: `small`, `basic`, `standard`, `plus`, `pro`, `advanced`, `premium`

### invoices

Get user's invoices with pagination.

**Parameters:**

| Name       | Type                     | Required | Description          |
|------------|--------------------------|----------|----------------------|
| pagination | InvoicePaginationInput   | No       | limit, offset        |

```graphql
query GetInvoices($pagination: InvoicePaginationInput) {
  billing {
    invoices(pagination: $pagination) {
      items {
        id
        amount
        status
        createdAt
        description
      }
      total
      limit
      offset
    }
  }
}
```

**Arguments:**
- `pagination` (InvoicePaginationInput): Pagination parameters

**Returns:** `InvoiceConnection`

**Authentication:** Required

**Validation:**
- Pagination is validated via `validate_pagination` utility
- `limit`: Must be between 1 and 100 (default: 10)
- `offset`: Must be non-negative (default: 0)

**Implementation Details:**
- **Mock Implementation**: Currently uses a mock implementation to generate invoice data
- In production, this would integrate with a payment processor (Stripe, PayPal, etc.)
- Generates invoices based on subscription history (up to 12 invoices)
- Activity logging is non-blocking (errors are logged but don't affect the operation)

## Mutations

### subscribe

Subscribe to a subscription plan.

**Parameters:**

| Name  | Type             | Required | Description        |
|-------|------------------|----------|--------------------|
| input | SubscribeInput!  | Yes      | tier, period       |

```graphql
mutation Subscribe($input: SubscribeInput!) {
  billing {
    subscribe(input: $input) {
      message
      subscriptionPlan
      subscriptionPeriod
      credits
      subscriptionEndsAt
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "tier": "pro",
    "period": "monthly"
  }
}
```

**Input:** `SubscribeInput!`

**Returns:** `SubscribeResult`

**Authentication:** Required

**Validation:**
- `tier`: Required, non-empty string, max 50 characters, must be a valid tier (5k, 25k, 100k, 500k, 1M, 5M, 10M)
- `period`: Required, non-empty string, max 50 characters, must be one of: `monthly`, `quarterly`, `yearly`
- SuperAdmin/Admin users cannot subscribe (they have unlimited credits)

**Implementation Details:**
- Uses Connectra subscription logic via `BillingService.subscribe_to_plan`
- Tries to get plan from database first, falls back to hardcoded `SUBSCRIPTION_PLANS` if database fails
- Updates user profile with subscription details and credits
- Calculates subscription end date based on period
- Activity logging is non-blocking (errors are logged but don't affect the operation)

### purchaseAddon

Purchase an addon credit package.

**Parameters:**

| Name  | Type                   | Required | Description  |
|-------|------------------------|----------|--------------|
| input | PurchaseAddonInput!    | Yes      | packageId    |

```graphql
mutation PurchaseAddon($input: PurchaseAddonInput!) {
  billing {
    purchaseAddon(input: $input) {
      message
      package
      creditsAdded
      totalCredits
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "packageId": "addon_1000_credits"
  }
}
```

**Input:** `PurchaseAddonInput!`

**Returns:** `PurchaseAddonResult`

**Authentication:** Required

**Validation:**
- `packageId`: Required, non-empty string, max 100 characters, must be a valid package ID (small, basic, standard, plus, pro, advanced, premium)
- SuperAdmin/Admin users cannot purchase addons (they have unlimited credits)

**Implementation Details:**
- Uses `BillingService.purchase_addon_credits`
- Tries to get package from database first, falls back to hardcoded `ADDON_PACKAGES` if database fails
- Adds credits to user's existing credit balance
- Activity logging is non-blocking (errors are logged but don't affect the operation)

### cancelSubscription

Cancel current subscription.

**Parameters:** None.

```graphql
mutation CancelSubscription {
  billing {
    cancelSubscription {
      message
      subscriptionStatus
    }
  }
}
```

**Returns:** `CancelSubscriptionResult`

**Authentication:** Required

## Admin Mutations (SuperAdmin only)

### createPlan

Create a new subscription plan.

**Parameters:**

| Name  | Type                 | Required | Description        |
|-------|----------------------|----------|--------------------|
| input | CreatePlanInput!     | Yes      | tier, name, category, periods |

```graphql
mutation CreatePlan($input: CreatePlanInput!) {
  billing {
    createPlan(input: $input) {
      message
      tier
    }
  }
}
```

### updatePlan

Update an existing subscription plan.

**Parameters:**

| Name  | Type               | Required | Description  |
|-------|--------------------|----------|--------------|
| tier  | String!            | Yes      | Plan tier    |
| input | UpdatePlanInput!   | Yes      | name, category, isActive |

```graphql
mutation UpdatePlan($tier: String!, $input: UpdatePlanInput!) {
  billing {
    updatePlan(tier: $tier, input: $input) {
      message
      tier
    }
  }
}
```

**Variables:**

```json
{
  "tier": "5k",
  "input": {
    "name": "Updated Plan Name",
    "category": "PROFESSIONAL",
    "isActive": true
  }
}
```

### deletePlan

Delete a subscription plan.

**Parameters:**

| Name | Type    | Required | Description  |
|------|---------|----------|--------------|
| tier | String! | Yes      | Plan tier    |

```graphql
mutation DeletePlan($tier: String!) {
  billing {
    deletePlan(tier: $tier) {
      message
      tier
    }
  }
}
```

**Variables:**

```json
{
  "tier": "5k"
}
```

### createPlanPeriod

Create or update a subscription plan period.

**Parameters:**

| Name  | Type                     | Required | Description  |
|-------|--------------------------|----------|--------------|
| tier  | String!                  | Yes      | Plan tier    |
| input | CreatePlanPeriodInput!   | Yes      | period, credits, price, etc. |

```graphql
mutation CreatePlanPeriod($tier: String!, $input: CreatePlanPeriodInput!) {
  billing {
    createPlanPeriod(tier: $tier, input: $input) {
      message
      tier
      period
    }
  }
}
```

**Variables:**

```json
{
  "tier": "5k",
  "input": {
    "period": "monthly",
    "credits": 5000,
    "ratePerCredit": 0.002,
    "price": 10.00,
    "savingsAmount": null,
    "savingsPercentage": null
  }
}
```

### updatePlanPeriod

Update an existing subscription plan period.

**Parameters:**

| Name   | Type                     | Required | Description  |
|--------|--------------------------|----------|--------------|
| tier   | String!                  | Yes      | Plan tier    |
| period | String!                  | Yes      | Period (e.g. monthly) |
| input  | UpdatePlanPeriodInput!   | Yes      | credits, price, etc. (all optional) |

```graphql
mutation UpdatePlanPeriod($tier: String!, $period: String!, $input: UpdatePlanPeriodInput!) {
  billing {
    updatePlanPeriod(tier: $tier, period: $period, input: $input) {
      message
      tier
      period
    }
  }
}
```

**Variables:**

```json
{
  "tier": "5k",
  "period": "monthly",
  "input": {
    "credits": 6000,
    "price": 12.00
  }
}
```

**Note:** Only provide the fields you want to update. All fields in `UpdatePlanPeriodInput` are optional.

### deletePlanPeriod

Delete a subscription plan period.

**Parameters:**

| Name   | Type   | Required | Description  |
|--------|--------|----------|--------------|
| tier   | String!| Yes      | Plan tier    |
| period | String!| Yes      | Period (e.g. monthly) |

```graphql
mutation DeletePlanPeriod($tier: String!, $period: String!) {
  billing {
    deletePlanPeriod(tier: $tier, period: $period) {
      message
      tier
      period
    }
  }
}
```

**Variables:**

```json
{
  "tier": "5k",
  "period": "monthly"
}
```

### createAddon

Create an addon package.

**Parameters:**

| Name  | Type                 | Required | Description        |
|-------|----------------------|----------|--------------------|
| input | CreateAddonInput!    | Yes      | id, name, credits, price, etc. |

```graphql
mutation CreateAddon($input: CreateAddonInput!) {
  billing {
    createAddon(input: $input) {
      message
      id
    }
  }
}
```

### updateAddon

Update an addon package.

**Parameters:**

| Name      | Type               | Required | Description  |
|-----------|--------------------|----------|--------------|
| packageId | String!            | Yes      | Addon package ID |
| input     | UpdateAddonInput!  | Yes      | name, credits, price, etc. |

```graphql
mutation UpdateAddon($packageId: String!, $input: UpdateAddonInput!) {
  billing {
    updateAddon(packageId: $packageId, input: $input) {
      message
      id
    }
  }
}
```

**Variables:**

```json
{
  "packageId": "small",
  "input": {
    "name": "Updated Package Name",
    "credits": 6000,
    "price": 12.00
  }
}
```

### deleteAddon

Delete an addon package.

**Parameters:**

| Name      | Type   | Required | Description      |
|-----------|--------|----------|------------------|
| packageId | String!| Yes      | Addon package ID |

```graphql
mutation DeleteAddon($packageId: String!) {
  billing {
    deleteAddon(packageId: $packageId) {
      message
      id
    }
  }
}
```

**Variables:**

```json
{
  "packageId": "small"
}
```

## Input Types

### SubscribeInput

Input for subscribing to a plan.

```graphql
input SubscribeInput {
  tier: String!
  period: String!
}
```

**Fields:**

- `tier` (String!): Subscription tier (5k, 25k, 100k, 500k, 1M, 5M, 10M) - max 50 characters
- `period` (String!): Billing period (monthly, quarterly, yearly) - max 50 characters

**Validation:**

- `tier`: Required, non-empty, max 50 characters, must be a valid tier
- `period`: Required, non-empty, max 50 characters, must be one of: `monthly`, `quarterly`, `yearly`
- Input validation is performed via `input.validate()` method

### PurchaseAddonInput

Input for purchasing an addon.

```graphql
input PurchaseAddonInput {
  packageId: String!
}
```

**Fields:**

- `packageId` (String!): Addon package ID (small, basic, standard, plus, pro, advanced, premium) - max 100 characters

**Validation:**

- `packageId`: Required, non-empty, max 100 characters, must be a valid package ID
- Input validation is performed via `input.validate()` method

### InvoicePaginationInput

Input for paginating invoices.

```graphql
input InvoicePaginationInput {
  limit: Int
  offset: Int
}
```

**Fields:**

- `limit` (Int): Maximum number of invoices to return (1-100, default: 10)
- `offset` (Int): Number of invoices to skip (non-negative, default: 0)

**Validation:**

- `limit`: Must be between 1 and 100
- `offset`: Must be non-negative
- Input validation is performed via `input.validate()` method

## Admin Input Types (SuperAdmin only)

### CreatePlanInput

Input for creating a subscription plan.

```graphql
input CreatePlanInput {
  tier: String!
  name: String!
  category: String!
  periods: [PlanPeriodInput!]!
  isActive: Boolean
}
```

**Categories:** `STARTER`, `PROFESSIONAL`, `BUSINESS`, `ENTERPRISE`

### UpdatePlanInput

Input for updating a subscription plan.

```graphql
input UpdatePlanInput {
  name: String
  category: String
  isActive: Boolean
}
```

### PlanPeriodInput

Input for a subscription plan period (used in CreatePlanInput).

```graphql
input PlanPeriodInput {
  period: String!
  credits: Int!
  ratePerCredit: Float!
  price: Float!
  savingsAmount: Float
  savingsPercentage: Int
}
```

### CreatePlanPeriodInput

Input for creating a subscription plan period.

```graphql
input CreatePlanPeriodInput {
  period: String!
  credits: Int!
  ratePerCredit: Float!
  price: Float!
  savingsAmount: Float
  savingsPercentage: Int
}
```

### UpdatePlanPeriodInput

Input for updating a subscription plan period.

```graphql
input UpdatePlanPeriodInput {
  credits: Int
  ratePerCredit: Float
  price: Float
  savingsAmount: Float
  savingsPercentage: Int
}
```

**Note:** All fields are optional. Only provide the fields you want to update.

### CreateAddonInput

Input for creating an addon package.

```graphql
input CreateAddonInput {
  id: String!
  name: String!
  credits: Int!
  ratePerCredit: Float!
  price: Float!
  isActive: Boolean
}
```

### UpdateAddonInput

Input for updating an addon package.

```graphql
input UpdateAddonInput {
  name: String
  credits: Int
  ratePerCredit: Float
  price: Float
  isActive: Boolean
}
```

## Error Handling

The Billing module implements comprehensive error handling with input validation, database error handling, external service error handling, and role-based access control.

### Error Types

The Billing module may raise the following errors:

- **NotFoundError** (404): Plan, addon, or invoice not found
  - Code: `NOT_FOUND`
  - Extensions: `resourceType: "SubscriptionPlan"`, `"AddonPackage"`, or `"Invoice"`, `identifier: <id>`
  - Occurs when: Requested plan, addon, or invoice does not exist
- **ValidationError** (422): Input validation failed
  - Code: `VALIDATION_ERROR`
  - Extensions: `fieldErrors` (field-specific errors)
  - Occurs when: Invalid tier/period combination, invalid package ID, invalid pagination values, or missing required fields
- **BadRequestError** (400): Invalid subscription operation
  - Code: `BAD_REQUEST`
  - Occurs when: Invalid subscription state transition, subscription already exists, invalid operation for current subscription status, or SuperAdmin/Admin users attempting to subscribe/purchase addons (they have unlimited credits)
- **ForbiddenError** (403): Insufficient permissions
  - Code: `FORBIDDEN`
  - Extensions: `requiredRole: "SuperAdmin"` (for admin operations)
  - Occurs when: User lacks SuperAdmin role required for plan/addon management operations
- **ServiceUnavailableError** (503): Database or payment service unavailable
  - Code: `SERVICE_UNAVAILABLE`
  - Extensions: `serviceName: "database"` or `serviceName: "razorpay"`
  - Occurs when: Database connection fails or Razorpay payment service is unavailable

### Error Response Examples

**Example: Plan Not Found**

```json
{
  "errors": [
    {
      "message": "SubscriptionPlan with identifier 'invalid_tier' not found",
      "extensions": {
        "code": "NOT_FOUND",
        "statusCode": 404,
        "resourceType": "SubscriptionPlan",
        "identifier": "invalid_tier"
      }
    }
  ]
}
```

**Example: Validation Error**

```json
{
  "errors": [
    {
      "message": "Invalid subscription period",
      "extensions": {
        "code": "VALIDATION_ERROR",
        "statusCode": 422,
        "fieldErrors": {
          "period": ["Period must be one of: monthly, quarterly, yearly"],
          "tier": ["Tier is required"]
        }
      }
    }
  ]
}
```

**Example: Bad Request Error**

```json
{
  "errors": [
    {
      "message": "Subscription already exists for this user",
      "extensions": {
        "code": "BAD_REQUEST",
        "statusCode": 400
      }
    }
  ]
}
```

**Example: Forbidden Error**

```json
{
  "errors": [
    {
      "message": "You do not have permission to perform this action",
      "extensions": {
        "code": "FORBIDDEN",
        "statusCode": 403,
        "requiredRole": "SuperAdmin"
      }
    }
  ]
}
```

### Error Handling Patterns

- **Input Validation**: Tiers, periods, package IDs, and pagination parameters are validated before processing
- **Database Errors**: All database operations include transaction rollback on failure
- **External Service Errors**: Razorpay API errors are caught and converted to appropriate GraphQL errors
- **Role-Based Access**: Plan and addon management operations require SuperAdmin role
- **Subscription State Validation**: Subscription state transitions are validated before processing
- **Error Logging**: Comprehensive error logging with context for debugging

## Usage Examples

### Subscription Management

```graphql
# Get billing info
query GetBilling {
  billing {
    billing {
      credits
      creditsUsed
      subscriptionPlan
      subscriptionStatus
    }
  }
}

# Get available plans
query GetPlans {
  billing {
    plans {
      tier
      name
      category
      periods {
        monthly {
          price
          credits
        }
        yearly {
          price
          credits
          savings {
            percentage
          }
        }
      }
    }
  }
}

# Subscribe to a plan
mutation Subscribe {
  billing {
    subscribe(input: {
      tier: "pro"
      period: "monthly"
    }) {
      message
      subscriptionPlan
      credits
    }
  }
}

# Purchase addon
mutation PurchaseAddon {
  billing {
    purchaseAddon(input: {
      packageId: "addon_1000_credits"
    }) {
      message
      creditsAdded
      totalCredits
    }
  }
}

# Cancel subscription
mutation Cancel {
  billing {
    cancelSubscription {
      message
      subscriptionStatus
    }
  }
}
```

## Implementation Details

### Billing Service

- **BillingService**: Billing operations are handled by `BillingService`
  - All billing operations go through the service layer
  - Service handles database operations, validation, and business logic

### Subscription Plans

- **Hardcoded Data**: Subscription plans are loaded from hardcoded `SUBSCRIPTION_PLANS` constants
  - Used directly for maximum performance (sub-millisecond response times)
  - Bypasses database queries entirely for `get_subscription_plans`
  - Plans are static data defined in `app/services/billing/constants.py`
  - Available tiers: `5k`, `25k`, `100k`, `500k`, `1M`, `5M`, `10M`
  - Each tier supports `monthly`, `quarterly`, and `yearly` periods

### Addon Packages

- **Database with Fallback**: Addon packages try database first, then fall back to hardcoded data
  - Tries to fetch from database if session is provided
  - **Fallback Mechanism**: If database access fails, gracefully falls back to hardcoded `ADDON_PACKAGES` constants
  - This ensures service availability even if database is temporarily unavailable
  - Available packages: `small`, `basic`, `standard`, `plus`, `pro`, `advanced`, `premium`

### Credit Management

- **Credit Calculation**: Credits are calculated based on subscription plan and period
  - Free tier: 50 credits (initial free credits)
  - Subscription tiers: Credits from plan period (database or hardcoded fallback)
  - **Unlimited Credits**: SuperAdmin/Admin roles have unlimited credits (999999)
    - Represented as 999999 in the system
    - No subscription required for unlimited users
- **Credit Updates**: Credits are updated when subscribing or purchasing addons
  - Subscription sets credits to plan amount
  - Addon purchase adds credits to existing balance

### Subscription Management

- **Subscription Tracking**: Subscription status and dates are tracked in user profiles
  - `subscription_plan`: Tier name (5k, 25k, etc.)
  - `subscription_period`: Billing period (monthly, quarterly, yearly)
  - `subscription_status`: Status (active, cancelled, expired)
  - `subscription_started_at`: Start date
  - `subscription_ends_at`: End date (calculated based on period)
- **Subscription End Date**: Calculated via `calculate_subscription_end_date` helper
  - Monthly: +30 days
  - Quarterly: +90 days
  - Yearly: +365 days

### Invoice Management

- **Mock Implementation**: `get_invoices` uses a mock implementation
  - Generates invoice data based on subscription history
  - In production, this would integrate with a payment processor (Stripe, PayPal, etc.)
  - Generates up to 12 invoices based on subscription period
  - Invoice status: `paid`, `pending`, `failed`

### Pagination

- **Pagination Validation**: Invoice pagination is validated via `validate_pagination` utility
  - `limit`: Must be between 1 and 100 (default: 10)
  - `offset`: Must be non-negative (default: 0)

### Access Control

- **Public Endpoints**: Plans and addons queries are public (no auth required)
- **User Endpoints**: Billing info, invoices, subscribe, purchase addon, cancel subscription require authentication
- **Admin Operations**: Plan and addon management requires SuperAdmin role
  - `createPlan`, `updatePlan`, `deletePlan`
  - `createPlanPeriod`, `updatePlanPeriod`, `deletePlanPeriod`
  - `createAddon`, `updateAddon`, `deleteAddon`

### Activity Logging

- **Non-Blocking**: Activity logging is non-blocking - if logging fails, the operation still succeeds
  - Activity logging errors are caught and logged but don't affect the primary operation
  - Logs include: operation type, user UUID, subscription details, package details

### Error Handling

- **Input Validation**: All inputs are validated before processing
  - Tier validation: max 50 characters, must be valid tier
  - Period validation: max 50 characters, must be valid period
  - Package ID validation: max 100 characters, must be valid package
  - UUID validation for user IDs
- **Database Error Handling**: Database operations use centralized error handlers
  - Transaction rollback on failure
  - Integrity errors are caught and converted to user-friendly errors
  - Database connection errors trigger fallback to hardcoded data (for addons)
- **Business Logic Validation**:
  - SuperAdmin/Admin cannot subscribe or purchase addons (unlimited credits)
  - Invalid tier/period combinations are rejected
  - Invalid package IDs are rejected

## Task breakdown (for maintainers)

1. **billing query:** BillingService/UserProfileRepository; credits, subscription fields from user_profiles; subscription_plans / subscription_plan_periods for plan details; usagePercentage computed.
2. **plans/addons:** Public queries; subscription_plans and addon_packages tables; optional category filter for plans; document period structure (monthly/yearly, price, credits).
3. **subscribe/purchaseAddon/cancelSubscription:** Razorpay integration; validate plan/addon IDs; update user_profiles (subscription_*, razorpay_*); confirm webhook or callback handling if used.
4. **Admin plan/addon CRUD:** SuperAdmin only; createPlan, updatePlan, deletePlan and period/addon equivalents; validate tier, name, price, credits; document which fields are required in each input.
5. **invoices:** If implemented, verify repository and pagination; link to Razorpay or local invoice records.

## Related Modules

- **Users Module**: User profiles contain subscription and credit information
- **Usage Module**: Tracks feature usage against credit limits
- **Admin Module**: Provides admin operations for billing management
- **AI Chats Module** ([17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md)): `AI_CHAT` (and related) usage limits are enforced via Usage/billing rules, not by Contact AI directly

## Documentation metadata

- Era: `1.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

