---
title: "Profile"
page_id: profile_page
source_json: profile_page.json
generator: json_to_markdown.py
---

# Profile

## Overview

- **page_id:** profile_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 0.x, 1.x, 8.x, 9.x, 11.x
- **flow_id:** profile
- **_id:** profile_page-001

## Metadata

- **route:** /profile
- **file_path:** contact360.io/app/app/(dashboard)/profile/page.tsx
- **purpose:** User profile management with tabs: My Profile (edit name, title, bio, avatar), Team (admin-only), AI Settings, Appearance, Notifications, Security (sessions, 2FA), API Keys (Pro+), Billing (redirects to /billing). Data batched via profilePageApi.
- **s3_key:** data/pages/profile_page.json
- **status:** published
- **authentication:** Required (protected by useSessionGuard)
- **authorization:** Team tab visible only to admin. API Keys tab gated by hasFeatureAccess(Feature.API_KEYS). Billing tab redirects to /billing.
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
- `graphql/GetMe` — Get profile data via AuthContext. Via useAuth hook.
- `graphql/ListTeamMembers` — List company members. Via useTeam hook.
- `graphql/InviteTeamMember` — Send email invitation to new member. Via useTeam hook.
- `graphql/RemoveTeamMember` — Revoke member access. Via useTeam hook.
- `graphql/ListSessions` — List active device sessions. Via useSessions hook.
- `graphql/RevokeSession` — Force logout for a specific device. Via useSessions hook.
- `graphql/ListAPIKeys` — List developer keys. Via useAPIKeys hook.
- `graphql/CreateAPIKey` — Generate new secret key. Via useAPIKeys hook.
- `graphql/UploadAvatar` — Post base64 image data to S3/DB. Via uploadAvatar service.

### UI components (metadata)

- **ProfilePage** — `app/(dashboard)/profile/page.tsx`
- **ProfileOverview** — `components/profile/ProfileOverview.tsx`
- **ProfileTabGeneral** — `components/profile/ProfileTabGeneral.tsx`
- **ProfileTabTeam** — `components/profile/ProfileTabTeam.tsx`
- **ProfileTabSecurity** — `components/profile/ProfileTabSecurity.tsx`
- **ProfileTabAPI** — `components/profile/ProfileTabAPI.tsx`
- **ProfileTabAppearance** — `components/profile/ProfileTabAppearance.tsx`
- **Tabs** — `components/ui/Tabs.tsx`
- **Modal** — `components/ui/Modal.tsx`
- **ConfirmModal** — `components/ui/ConfirmModal.tsx`
- **TwoFactorModal** — `components/shared/TwoFactorModal.tsx`
- **ProfileTabNotifications** — `components/profile/ProfileTabNotifications.tsx`
- **ProfileTabAI** — `components/profile/ProfileTabAI.tsx`
- **Tabs** — `components/ui/Tabs.tsx`
- **Modal** — `components/ui/Modal.tsx`
- **ConfirmModal** — `components/ui/ConfirmModal.tsx`

- **versions:** []
- **endpoint_count:** 16
### api_versions

- graphql

- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Profile

### description

User profile management with tabs: My Profile (edit name, title, bio, avatar), Team (admin-only), AI Settings, Appearance, Notifications, Security (sessions, 2FA), API Keys (Pro+), Billing (redirects to /billing). Data batched via profilePageApi.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| profile-title | 1 | Profile |
| profile-overview | 2 | Account Overview |


### subheadings

| id | level | text | visibility |
| --- | --- | --- | --- |
| personal-info | 3 | Personal Information |  |
| active-sessions | 3 | Active Sessions |  |
| two-factor | 3 | Two-Factor Authentication |  |
| team-members | 3 | Team Members | admin only |


### tabs

| content_ref | id | label | visibility |
| --- | --- | --- | --- |
| profile-edit | my-profile | My Profile |  |
| profile-team | team | Team | admin only |
| profile-ai | ai-settings | AI Settings |  |
| profile-appearance | appearance | Appearance |  |
| profile-notifications | notifications | Notifications |  |
| profile-security | security | Security |  |
| profile-api-keys | api-keys | API Keys | Pro+ only |
| profile-billing | billing | Billing |  |


### buttons

| action | component | id | label | type | era |
| --- | --- | --- | --- | --- | --- |
| uploadAvatar | ProfileOverview | avatar-input | Change Avatar | file | 0.x |
| setActiveTab | Tabs | profile-tab | [Tab] | ghost | 0.x |
| inviteTeamMember | ProfileTabTeam | invite-btn | Invite Member | primary | 1.x |
| removeTeamMember | ProfileTabTeam | remove-btn | Remove | ghost | 1.x |
| createKey | ProfileTabAPI | create-key-btn | Create API Key | primary | 8.x |
| revokeKey | ProfileTabAPI | revoke-key-btn | Revoke | danger | 8.x |
| revokeSession | ProfileTabSecurity | revoke-session-btn | Revoke | ghost | 1.x |
| revokeAllOthers | ProfileTabSecurity | revoke-all-btn | Revoke All Other Sessions | danger | 9.x |
| toggleTheme | ProfileTabAppearance | theme-toggle | [Icons] | ghost | 0.x |


### input_boxes

- **[0]**
  - **id:** first-name
  - **label:** First name
  - **type:** text
  - **placeholder:** John
  - **required:** True
  - **component:** ProfileEditForm
  - **tab:** my-profile

- **[1]**
  - **id:** last-name
  - **label:** Last name
  - **type:** text
  - **placeholder:** Doe
  - **required:** False
  - **component:** ProfileEditForm
  - **tab:** my-profile

- **[2]**
  - **id:** job-title
  - **label:** Job title
  - **type:** text
  - **placeholder:** e.g. Sales Manager
  - **required:** False
  - **component:** ProfileEditForm
  - **tab:** my-profile

- **[3]**
  - **id:** bio
  - **label:** Bio
  - **type:** textarea
  - **placeholder:** Tell us about yourself
  - **required:** False
  - **rows:** 3
  - **component:** ProfileEditForm
  - **tab:** my-profile

- **[4]**
  - **id:** current-password
  - **label:** Current password
  - **type:** password
  - **required:** True
  - **has_toggle:** True
  - **component:** ProfileEditForm
  - **tab:** my-profile

- **[5]**
  - **id:** new-password
  - **label:** New password
  - **type:** password
  - **required:** False
  - **has_toggle:** True
  - **component:** ProfileEditForm
  - **tab:** my-profile

- **[6]**
  - **id:** invite-email
  - **label:** Email address to invite
  - **type:** email
  - **placeholder:** colleague@company.com
  - **required:** True
  - **component:** ProfileTeamManagement
  - **tab:** team

- **[7]**
  - **id:** api-key-name
  - **label:** Key name
  - **type:** text
  - **placeholder:** e.g. Production API Key
  - **required:** True
  - **component:** ProfileAPIKeys
  - **tab:** api-keys

- **[8]**
  - **id:** otp-input
  - **label:** 6-digit OTP
  - **type:** text
  - **placeholder:** 000000
  - **maxlength:** 6
  - **pattern:** [0-9]{6}
  - **component:** TwoFactorModal
  - **tab:** security



### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| ProfileOverviewCard | Account email: {email} (cannot be changed) | account-email-display | read-only |
| ProfileOverviewCard | {planName} | plan-badge | badge |
| ProfileOverviewCard | Member since {joinDate} | member-since | caption |
| ProfileSecurity | Two-factor authentication is {enabled/disabled} | 2fa-status | status |
| ProfileAPIKeys | Created {date} · Last used {lastUsed} | api-key-created | caption |


### checkboxes



### radio_buttons

| component | id | label | options | purpose | tab |
| --- | --- | --- | --- | --- | --- |
| ProfileAppearance | theme-select | Appearance theme | ['Light', 'Dark', 'System'] | Set dashboard color theme | appearance |
| ProfileTeamManagement | team-role | Member role | ['Viewer', 'Editor', 'Admin'] | Set team member role | team |


### progress_bars



### graphs



### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| ProfileHeader | avatar-upload-flow | Avatar upload | ["Click 'Change Avatar'", 'File input (max 5MB, JPEG/PNG/GIF/WebP)', 'Preview shown', 'Submit → usersService.UploadAvatar', 'ProfileHeader updates with new avatar URL'] |
| TwoFactorModal | 2fa-setup-flow | 2FA setup flow | ["Click 'Enable 2FA'", 'twoFactorService.Setup2FA → returns QR code + secret', 'User scans QR in authenticator app', 'Enter 6-digit OTP to verify', 'twoFactorService.Verify2FA', 'On success: 2FA enabl |


### components

| file_path | name | purpose |
| --- | --- | --- |
| components/features/profile/ProfileTabNavigation.tsx | ProfileTabNavigation | Vertical tab nav (My Profile, Team, AI Settings, etc.) |
| components/features/profile/ProfileHeader.tsx | ProfileHeader | Avatar, name, plan badge, member-since |
| components/features/profile/ProfileOverviewCard.tsx | ProfileOverviewCard | Read-only account summary card |
| components/features/profile/ProfileEditForm.tsx | ProfileEditForm | Editable name, title, bio, password fields |
| components/features/profile/ProfileTeamManagement.tsx | ProfileTeamManagement | Team member list with invite/remove/role |
| components/features/profile/ProfileAISettings.tsx | ProfileAISettings | AI model preferences and behavior settings |
| components/features/profile/ProfileAppearance.tsx | ProfileAppearance | Theme toggle (light/dark/system) |
| components/features/profile/ProfileNotifications.tsx | ProfileNotifications | Notification preference toggles |
| components/features/profile/ProfileSecurity.tsx | ProfileSecurity | Sessions list + 2FA management |
| components/features/profile/ProfileAPIKeys.tsx | ProfileAPIKeys | API key list, create, revoke, copy |
| components/features/profile/TwoFactorModal.tsx | TwoFactorModal | QR code + OTP verification for 2FA setup/disable |


### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| context/AuthContext.ts | useAuth | Global user identity and session management | 0.x |
| context/ThemeContext.ts | useTheme | Light/Dark mode state and toggle | 0.x |
| hooks/index.ts | useTeam | Team membership and invitation logic | 1.x |
| hooks/index.ts | useSessions | Active device session tracking and revocation | 0.x |
| hooks/index.ts | useAPIKeys | High-privilege API credential management | 8.x |
| hooks/useAPIKeys.ts | useAPIKeys | API key lifecycle management | 9.x |
| hooks/useProfilePage.ts | use2FA | Setup2FA, Verify2FA, Disable2FA mutations |


### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/authService.ts | authService | ['GetMe'] |
| services/graphql/profileService.ts | profileService | ['ListAPIKeys', 'ListSessions', 'ListTeamMembers', 'CreateAPIKey', 'DeleteAPIKey', 'RevokeSession', 'InviteTeamMember', 'UpdateTeamMemberRole', 'RemoveTeamMember'] |
| services/graphql/usersService.ts | usersService | ['UpdateProfile', 'UploadAvatar'] |
| services/graphql/twoFactorService.ts | twoFactorService | ['Get2FAStatus', 'Setup2FA', 'Verify2FA', 'Disable2FA'] |


### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/AuthContext.tsx | AuthContext | Current user data display |
| context/RoleContext.tsx | RoleContext | Team tab (admin), API Keys tab (Pro+) visibility |
| context/ThemeContext.tsx | ThemeContext | Appearance tab reads/writes theme |


### utilities

| file_path | name | purpose |
| --- | --- | --- |
| lib/clipboard.ts | clipboard | Copy API key to clipboard with success toast |
| lib/profile/sessionUtils.ts | sessionUtils | Format device name and last-active timestamp |


### ui_components



### endpoints

| hook | method | operation | service |
| --- | --- | --- | --- |
| useProfilePage | QUERY | GetMe | authService |
| useProfilePage | QUERY | ListAPIKeys | profileService |
| useProfilePage | QUERY | ListSessions | profileService |
| useUserProfile | MUTATION | UpdateProfile | usersService |
| use2FA | MUTATION | Setup2FA | twoFactorService |


## UI elements (top-level)

### buttons

| id | label | type | action | loading_state | component | tab |
| --- | --- | --- | --- | --- | --- | --- |
| save-profile | Save Changes | primary | usersService.UpdateProfile | Saving... | ProfileEditForm | my-profile |
| upload-avatar | Change Avatar | secondary | file input → usersService.UploadAvatar |  | ProfileHeader | my-profile |
| invite-member | Invite Member | primary | profileService.InviteTeamMember → email input modal |  | ProfileTeamManagement | team |
| remove-member | Remove | danger | profileService.RemoveTeamMember → ConfirmModal |  | ProfileTeamManagement | team |
| create-api-key | Create API Key | primary | profileService.CreateAPIKey → name input modal |  | ProfileAPIKeys | api-keys |
| revoke-api-key | Revoke | danger | profileService.DeleteAPIKey → ConfirmModal |  | ProfileAPIKeys | api-keys |
| copy-api-key | Copy | icon | clipboard.copyToClipboard(key) |  | ProfileAPIKeys | api-keys |
| setup-2fa | Enable 2FA | primary | twoFactorService.Setup2FA → TwoFactorModal |  | ProfileSecurity | security |
| disable-2fa | Disable 2FA | danger | twoFactorService.Disable2FA → OTP confirm |  | ProfileSecurity | security |
| revoke-session | Revoke | danger | profileService.RevokeSession |  | ProfileSecurity | security |
| revoke-all-sessions | Revoke All Other Sessions | danger | revoke all except current |  | ProfileSecurity | security |
| go-to-billing | Manage Billing | primary | navigate to /billing |  | ProfilePage | billing |


### inputs

| id | label | type | placeholder | required | component | tab |
| --- | --- | --- | --- | --- | --- | --- |
| first-name | First name | text | John | True | ProfileEditForm | my-profile |
| last-name | Last name | text | Doe | False | ProfileEditForm | my-profile |
| job-title | Job title | text | e.g. Sales Manager | False | ProfileEditForm | my-profile |
| bio | Bio | textarea | Tell us about yourself | False | ProfileEditForm | my-profile |
| current-password | Current password | password |  | True | ProfileEditForm | my-profile |
| new-password | New password | password |  | False | ProfileEditForm | my-profile |
| invite-email | Email address to invite | email | colleague@company.com | True | ProfileTeamManagement | team |
| api-key-name | Key name | text | e.g. Production API Key | True | ProfileAPIKeys | api-keys |
| otp-input | 6-digit OTP | text | 000000 |  | TwoFactorModal | security |


### checkboxes

[]

### radio_buttons

| id | label | options | purpose | component | tab |
| --- | --- | --- | --- | --- | --- |
| theme-select | Appearance theme | ['Light', 'Dark', 'System'] | Set dashboard color theme | ProfileAppearance | appearance |
| team-role | Member role | ['Viewer', 'Editor', 'Admin'] | Set team member role | ProfileTeamManagement | team |


### progress_bars

[]

### toasts

[]

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useProfilePage.ts | useProfilePage | Batched: GetMe + ListAPIKeys + ListSessions + ListTeamMembers + Get2FAStatus |
| hooks/useProfilePage.ts | useUserProfile | UpdateProfile and UploadAvatar mutations |
| hooks/useAPIKeys.ts | useAPIKeys | API key CRUD |
| hooks/useSessions.ts | useSessions | Session list and revoke |
| hooks/useTeam.ts | useTeam | Invite, remove, update role for team members |
| hooks/useProfilePage.ts | use2FA | Setup2FA, Verify2FA, Disable2FA mutations |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/authService.ts | authService | ['GetMe'] |
| services/graphql/profileService.ts | profileService | ['ListAPIKeys', 'ListSessions', 'ListTeamMembers', 'CreateAPIKey', 'DeleteAPIKey', 'RevokeSession', 'InviteTeamMember', 'UpdateTeamMemberRole', 'RemoveTeamMember'] |
| services/graphql/usersService.ts | usersService | ['UpdateProfile', 'UploadAvatar'] |
| services/graphql/twoFactorService.ts | twoFactorService | ['Get2FAStatus', 'Setup2FA', 'Verify2FA', 'Disable2FA'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql/GetMe, graphql/ListAPIKeys, graphql/ListSessions, graphql/ListTeamMembers, graphql/Get2FAStatus, graphql/CreateAPIKey | dashboard data and mutations via services/hooks |


## Data Sources

- Appointment360 GraphQL gateway
- Service modules: authService, profileService, usersService, twoFactorService
- Backend-owned data stores (via GraphQL modules)


## Flow summary

app page UI -> useProfilePage, useUserProfile, useAPIKeys, useSessions -> authService, profileService, usersService, twoFactorService -> GraphQL gateway -> backend modules -> rendered states


<!-- AUTO:design-nav:start -->

- **0.x** — Foundation — app layouts, vertical tabs, confirm modals, file upload patterns.
- **1.x** — User / billing / credit — profile edits, team invitations, plan visibility.
- **8.x** — Public/Private APIs — API key management, secret mask/copy patterns.
- **9.x** — Security / Scaling — session audit trails, 2FA workflows, global logout.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L:Dashboard] > [H:Header] + [P:ProfileHero] + [S:StatsGrid] + [A:Actions] -> {useAuth}

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/profile`

**Codebase:** `contact360.io/app` (Next.js dashboard, GraphQL).

**Typical inbound:** `Sidebar` / `MainLayout`, [dashboard_page.md](dashboard_page.md) quick actions.

**Typical outbound:** Sidebar peers; [billing_page.md](billing_page.md) redirect via tab.

**Cross-host:** Hand-off from **root** (Marketing) auth links.
**Backend:** Appointment360 GraphQL gateway; aggregates user identity, team, keys, and security services.

- **Page → GraphQL endpoint specs:** run `python docs/frontend/pages/link_endpoint_specs.py` to refresh the `AUTO:endpoint-links` table in this file.
- **Endpoint ↔ database naming & Connectra scope:** [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).
- **Service topology:** [SERVICE_TOPOLOGY.md](../../backend/endpoints/SERVICE_TOPOLOGY.md).

### Peer pages (same codebase)

- [activities_page](activities_page.md)
- [admin_page](admin_page.md)
- [ai_chat_page](ai_chat_page.md)
- [analytics_page](analytics_page.md)
- [billing_page](billing_page.md)
- [campaign_builder_page](campaign_builder_page.md)
- [campaign_templates_page](campaign_templates_page.md)
- [campaigns_page](campaigns_page.md)
- [companies_page](companies_page.md)
- [contacts_page](contacts_page.md)
- [dashboard_page](dashboard_page.md)
- [dashboard_pageid_page](dashboard_pageid_page.md)
- [deployment_page](deployment_page.md)
- [email_page](email_page.md)
- [export_page](export_page.md)
- [files_page](files_page.md)
- [finder_page](finder_page.md)
- [jobs_page](jobs_page.md)
- [linkedin_page](linkedin_page.md)
- [live_voice_page](live_voice_page.md)
- [login_page](login_page.md)
- [register_page](register_page.md)
- [root_page](root_page.md)
- [sequences_page](sequences_page.md)
- [settings_page](settings_page.md)
- [status_page](status_page.md)
- [usage_page](usage_page.md)
- [verifier_page](verifier_page.md)

<!-- AUTO:design-nav:end -->

<!-- AUTO:endpoint-links:start -->

## Backend endpoint specs (GraphQL)

| GraphQL operation | Endpoint spec | Method | Era |
| --- | --- | --- | --- |
| `GetMe` | [query_get_me_graphql.md](../../backend/endpoints/query_get_me_graphql.md) | QUERY | 0.x |
| `ListTeamMembers` | [query_list_team_members_graphql.md](../../backend/endpoints/query_list_team_members_graphql.md) | QUERY | 0.x |
| `InviteTeamMember` | *unresolved — add to endpoint index* | — | — |
| `RemoveTeamMember` | *unresolved — add to endpoint index* | — | — |
| `ListSessions` | [query_list_sessions_graphql.md](../../backend/endpoints/query_list_sessions_graphql.md) | QUERY | 0.x |
| `RevokeSession` | [mutation_revoke_session_graphql.md](../../backend/endpoints/mutation_revoke_session_graphql.md) | MUTATION | 0.x |
| `ListAPIKeys` | [query_list_api_keys_graphql.md](../../backend/endpoints/query_list_api_keys_graphql.md) | QUERY | 5.x |
| `CreateAPIKey` | [mutation_create_api_key_graphql.md](../../backend/endpoints/mutation_create_api_key_graphql.md) | MUTATION | 5.x |
| `UploadAvatar` | [mutation_upload_avatar_graphql.md](../../backend/endpoints/mutation_upload_avatar_graphql.md) | MUTATION | 2.x |
| `Get2FAStatus` | [query_get_2fa_status_graphql.md](../../backend/endpoints/query_get_2fa_status_graphql.md) | QUERY | 0.x |

**Unresolved operations** (not found in `index.md` / `endpoints_index.md`):
`graphql/InviteTeamMember`, `graphql/RemoveTeamMember`

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
