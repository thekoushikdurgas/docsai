# Two-Factor Authentication Module

## Overview

The Two-Factor Authentication (2FA) module provides functionality for setting up, verifying, and managing two-factor authentication for user accounts. It supports TOTP (Time-based One-Time Password) authentication with backup codes for account recovery.
**Location:** `app/graphql/modules/two_factor/`

**Note:** The current implementation uses placeholder TOTP generation. In production, use `pyotp` and `qrcode` libraries for proper TOTP secret generation and QR code creation.

## Queries and mutations – parameters and variable types

| Operation | Parameter(s) | Variable type (GraphQL) | Return type |
|-----------|---------------|-------------------------|-------------|
| **Queries** | | | |
| `get2FAStatus` | — | — | `TwoFactorStatus` |
| **Mutations** | | | |
| `setup2FA` | — | — | `TwoFactorSetupResponse` |
| `verify2FA` | `code` | String! | `Verify2FAResponse` |
| `disable2FA` | — | — | result |
| `regenerateBackupCodes` | — | — | `RegenerateBackupCodesResponse` |

Use camelCase in variables. two_factor table (secret_hash, verified, enabled, backup_codes_hash). Auth required for all.

## Types

### TwoFactorStatus

Current 2FA status for a user.

```graphql
type TwoFactorStatus {
  enabled: Boolean!
  verified: Boolean!
}
```

**Fields:**
- `enabled` (Boolean!): Whether 2FA is currently enabled
- `verified` (Boolean!): Whether 2FA has been verified (setup completed)

### TwoFactorSetupResponse

Response when setting up 2FA.

```graphql
type TwoFactorSetupResponse {
  qr_code_url: String!
  qr_code_data: String!  # TOTP URI for manual entry
  secret: String!  # Backup secret (shown once)
  backup_codes: [String!]!  # Backup codes (shown once)
}
```

**Fields:**
- `qr_code_url` (String!): URL to QR code image for scanning with authenticator app
- `qr_code_data` (String!): TOTP URI string for manual entry if QR code cannot be scanned
- `secret` (String!): TOTP secret key (shown only once - store securely)
- `backup_codes` ([String!]!): List of backup codes for account recovery (shown only once - store securely)

### Verify2FAResponse

Response when verifying 2FA code.

```graphql
type Verify2FAResponse {
  verified: Boolean!
  backup_codes: [String!]  # Only returned if verification succeeds and backup codes were regenerated
}
```

**Fields:**
- `verified` (Boolean!): Whether verification was successful
- `backup_codes` ([String!]): New backup codes (only returned if codes were regenerated)

### RegenerateBackupCodesResponse

Response when regenerating backup codes.

```graphql
type RegenerateBackupCodesResponse {
  backup_codes: [String!]!
}
```

**Fields:**
- `backup_codes` ([String!]!): New list of backup codes (shown only once - store securely)

## Queries

### get2FAStatus

Get the current 2FA status for the authenticated user.

**Parameters:** None.

```graphql
query Get2FAStatus {
  twoFactor {
    get2FAStatus {
      enabled
      verified
    }
  }
}
```

**Returns:** `TwoFactorStatus`

**Authentication:** Required

**Implementation Details:**
- Uses `TwoFactorRepository.get_by_user_id` to retrieve 2FA record
- Returns `enabled: false, verified: false` if no 2FA record exists
- User isolation enforced - users can only view their own 2FA status

**Example Response:**

```json
{
  "data": {
    "twoFactor": {
      "get2FAStatus": {
        "enabled": true,
        "verified": true
      }
    }
  }
}
```

## Mutations

### setup2FA

Setup 2FA for the current user. Generates a TOTP secret, QR code, and backup codes.

**Parameters:** None.

```graphql
mutation Setup2FA {
  twoFactor {
    setup2FA {
      qr_code_url
      qr_code_data
      secret
      backup_codes
    }
  }
}
```

**Returns:** `TwoFactorSetupResponse`

**Authentication:** Required

**Implementation Details:**
- Generates a TOTP secret (currently placeholder - use `pyotp.generate_secret()` in production)
- Generates 10 backup codes
- Hashes the secret and backup codes for secure storage
- Creates or updates 2FA record with `verified: false, enabled: false`
- Generates QR code URL and TOTP URI for authenticator app setup
- **Important:** Secret and backup codes are shown only once - user must store them securely
- Database errors are handled centrally via `handle_database_exception`

**Note:** Current implementation uses placeholder TOTP generation. In production:
- Use `pyotp.generate_secret()` to generate proper TOTP secrets
- Use `pyotp` and `qrcode` libraries to generate QR codes
- Format: `otpauth://totp/AppName:user@example.com?secret=SECRET&issuer=AppName`

**Example Response:**

```json
{
  "data": {
    "twoFactor": {
      "setup2FA": {
        "qr_code_url": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=otpauth://totp/Contact360:user@example.com?secret=ABC123&issuer=Contact360",
        "qr_code_data": "otpauth://totp/Contact360:user@example.com?secret=ABC123&issuer=Contact360",
        "secret": "ABC123",
        "backup_codes": [
          "A1B2C3D4",
          "E5F6G7H8",
          "I9J0K1L2",
          "M3N4O5P6",
          "Q7R8S9T0",
          "U1V2W3X4",
          "Y5Z6A7B8",
          "C9D0E1F2",
          "G3H4I5J6",
          "K7L8M9N0"
        ]
      }
    }
  }
}
```

### verify2FA

Verify a 2FA code during setup or login. Enables 2FA if verification succeeds.

**Parameters:**

| Name | Type    | Required | Description                                  |
|------|---------|----------|----------------------------------------------|
| code | String! | Yes      | TOTP code from authenticator app or backup code |

```graphql
mutation Verify2FA($code: String!) {
  twoFactor {
    verify2FA(code: $code) {
      verified
      backup_codes
    }
  }
}
```

**Variables:**

```json
{
  "code": "123456"
}
```

**Arguments:**
- `code` (String!): TOTP code from authenticator app or backup code

**Returns:** `Verify2FAResponse`

**Authentication:** Required

**Validation:**
- `code`: Required, must be a non-empty string

**Implementation Details:**
- Retrieves 2FA record for user
- Verifies code against TOTP secret (currently placeholder - use `pyotp.TOTP(secret).verify(code)` in production)
- If verification succeeds:
  - Sets `verified: true` and `enabled: true`
  - Returns `verified: true`
- If verification fails:
  - Returns `verified: false`
- **Note:** Current implementation uses placeholder verification. In production, use `pyotp` library to verify TOTP codes
- Database errors are handled centrally via `handle_database_exception`

**Note:** Current implementation uses placeholder verification. In production:
- Use `pyotp.TOTP(secret).verify(code)` to verify TOTP codes
- Support backup code verification by checking against hashed backup codes
- Implement time window tolerance (typically ±1 time step = 30 seconds)

**Example Response (Success):**

```json
{
  "data": {
    "twoFactor": {
      "verify2FA": {
        "verified": true,
        "backup_codes": null
      }
    }
  }
}
```

**Example Response (Failure):**

```json
{
  "data": {
    "twoFactor": {
      "verify2FA": {
        "verified": false,
        "backup_codes": null
      }
    }
  }
}
```

### disable2FA

Disable 2FA for the current user.

**Parameters:**

| Name       | Type   | Required | Description                    |
|------------|--------|----------|--------------------------------|
| password   | String | No       | Optional password for verification |
| backupCode | String | No       | Optional backup code for verification |

```graphql
mutation Disable2FA($password: String, $backupCode: String) {
  twoFactor {
    disable2FA(password: $password, backupCode: $backupCode)
  }
}
```

**Variables:**

```json
{
  "password": "userpassword123",
  "backupCode": "A1B2C3D4"
}
```

**Arguments:**
- `password` (String): Optional password for verification
- `backupCode` (String): Optional backup code for verification

**Returns:** `Boolean` (true if successful)

**Authentication:** Required

**Implementation Details:**
- Retrieves 2FA record for user
- Raises NotFoundError if 2FA is not enabled
- **Note:** Password and backup code verification are placeholders - implement proper verification in production
- Sets `enabled: false` and `verified: false`
- Does not delete the 2FA record (allows re-enabling without new setup)
- Database errors are handled centrally via `handle_database_exception`

**Note:** Current implementation uses placeholder verification. In production:
- Verify password using user's hashed password
- Verify backup code against hashed backup codes
- Require either password OR backup code (not both)
- Log security event for 2FA disable action

**Example Response:**

```json
{
  "data": {
    "twoFactor": {
      "disable2FA": true
    }
  }
}
```

### regenerateBackupCodes

Regenerate backup codes for the current user. Invalidates all previous backup codes.

**Parameters:** None.

```graphql
mutation RegenerateBackupCodes {
  twoFactor {
    regenerateBackupCodes {
      backup_codes
    }
  }
}
```

**Returns:** `RegenerateBackupCodesResponse`

**Authentication:** Required

**Implementation Details:**
- Retrieves 2FA record for user
- Raises NotFoundError if 2FA is not enabled
- Generates 10 new backup codes
- Hashes and stores new backup codes (invalidates old ones)
- **Important:** New backup codes are shown only once - user must store them securely
- Database errors are handled centrally via `handle_database_exception`

**Example Response:**

```json
{
  "data": {
    "twoFactor": {
      "regenerateBackupCodes": {
        "backup_codes": [
          "X1Y2Z3A4",
          "B5C6D7E8",
          "F9G0H1I2",
          "J3K4L5M6",
          "N7O8P9Q0",
          "R1S2T3U4",
          "V5W6X7Y8",
          "Z9A0B1C2",
          "D3E4F5G6",
          "H7I8J9K0"
        ]
      }
    }
  }
}
```

## Error Handling

### Error Types

- **UnauthorizedError** (401): Authentication required
- **NotFoundError** (404): 2FA not enabled or record not found
- **BadRequestError** (400): Invalid input data (e.g., empty code)
- **InternalServerError** (500): Internal server error

### Error Response Examples

**Not Found (2FA not enabled):**

```json
{
  "errors": [{
    "message": "Resource with identifier 'user-uuid' not found",
    "extensions": {
      "code": "NOT_FOUND",
      "statusCode": 404,
      "resourceType": "TwoFactor",
      "identifier": "user-uuid"
    }
  }]
}
```

**Invalid Code:**

```json
{
  "errors": [{
    "message": "Invalid code: code must be a non-empty string",
    "extensions": {
      "code": "BAD_REQUEST",
      "statusCode": 400
    }
  }]
}
```

## Usage Examples

### Complete Flow: Setup and Enable 2FA

```graphql
# 1. Get current 2FA status
query GetStatus {
  twoFactor {
    get2FAStatus {
      enabled
      verified
    }
  }
}

# 2. Setup 2FA (get QR code and backup codes)
mutation Setup {
  twoFactor {
    setup2FA {
      qr_code_url
      qr_code_data
      secret
      backup_codes
    }
  }
}

# 3. Scan QR code with authenticator app (e.g., Google Authenticator, Authy)
# 4. Verify code from authenticator app
mutation Verify {
  twoFactor {
    verify2FA(code: "123456") {
      verified
    }
  }
}

# 5. Verify 2FA is enabled
query CheckEnabled {
  twoFactor {
    get2FAStatus {
      enabled
      verified
    }
  }
}
```

### Regenerate Backup Codes

```graphql
# Regenerate backup codes (invalidates old ones)
mutation Regenerate {
  twoFactor {
    regenerateBackupCodes {
      backup_codes
    }
  }
}
```

### Disable 2FA

```graphql
# Disable 2FA (requires password or backup code)
mutation Disable {
  twoFactor {
    disable2FA(password: "userpassword123")
  }
}
```

## Implementation Details

### Repository Integration

- **TwoFactorRepository**: Provides data access layer
  - `create`: Create new 2FA record
  - `get_by_user_id`: Get 2FA record by user ID
  - `update`: Update 2FA record (secret, verified, enabled, backup codes)

### Database Schema

- **Table**: `two_factor`
- **Key Fields**: `id`, `user_id`, `secret_hash`, `verified`, `enabled`, `backup_codes_hash`, `created_at`, `updated_at`
- **Indexes**: `user_id` (unique)
- **Foreign Keys**: `user_id` references `users.uuid`

### Security Considerations

1. **Secret Storage**: TOTP secrets are hashed using SHA-256 before storage
2. **Backup Codes**: Backup codes are hashed before storage (cannot be retrieved)
3. **One-Time Display**: Secrets and backup codes are shown only once during setup/regeneration
4. **Verification**: TOTP codes are verified against the stored secret hash
5. **Time Windows**: TOTP verification should support time window tolerance (typically ±1 time step = 30 seconds)

### Placeholder Implementation Notes

The current implementation uses placeholders for:
- **TOTP Secret Generation**: Use `pyotp.generate_secret()` in production
- **QR Code Generation**: Use `pyotp` and `qrcode` libraries in production
- **TOTP Verification**: Use `pyotp.TOTP(secret).verify(code)` in production
- **Password Verification**: Implement proper password verification in production
- **Backup Code Verification**: Implement proper backup code verification in production

### Production Implementation Checklist

- 📌 Planned: Install `pyotp` and `qrcode` libraries
- 📌 Planned: Replace placeholder secret generation with `pyotp.generate_secret()`
- 📌 Planned: Replace placeholder QR code generation with proper QR code creation
- 📌 Planned: Replace placeholder TOTP verification with `pyotp.TOTP(secret).verify(code)`
- 📌 Planned: Implement time window tolerance for TOTP verification (±1 time step)
- 📌 Planned: Implement password verification for disable2FA
- 📌 Planned: Implement backup code verification for disable2FA and verify2FA
- 📌 Planned: Add security event logging for 2FA operations
- 📌 Planned: Add rate limiting for verification attempts
- 📌 Planned: Add email notifications for 2FA enable/disable events

### User Isolation

All operations enforce user isolation:
- Queries filter by `user_id` at repository level
- Mutations verify user context before processing
- Users can only manage their own 2FA settings

### Timezone Handling

All timestamps use UTC timezone:
- `created_at`, `updated_at` are stored as timezone-aware datetimes

## Task breakdown (for maintainers)

1. **get2FAStatus:** TwoFactorRepository.get_by_user_id; return TwoFactorStatus (enabled, verified); auth required.
2. **setup2FA:** Generate TOTP secret (pyotp); create QR and backup codes; store secret_hash and backup_codes_hash in two_factor; return qr_code_url, qr_code_data, secret, backup_codes (once); do not re-show secret/codes.
3. **verify2FA:** Validate code against TOTP; set verified=true; optionally regenerate backup codes and return them; auth required.
4. **disable2FA:** Require password or 2FA code; set enabled=false, clear secret/backup hashes; auth required.
5. **regenerateBackupCodes:** New backup codes; hash and store; return new codes once; auth required. Confirm login flow checks 2FA when enabled (Auth module).

## Related Modules

- **Auth Module**: 2FA verification during login
- **Users Module**: User profile and authentication
- **Profile Module**: User account management
- **AI Chats Module** ([17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md)): after login, AI chat uses the same authenticated session; Contact AI is still called server-side with service credentials

## Documentation metadata

- Era: `9.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

