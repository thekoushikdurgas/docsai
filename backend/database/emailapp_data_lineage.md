# Email App Data Lineage — `contact360.io/email`

## Ownership model
`contact360.io/email` is a frontend consumer and does not own persistence tables. Data lineage flows through backend APIs.

## Lineage map

| UI source | API | Backend entity (logical) |
| --- | --- | --- |
| Login form | `POST /auth/login` | Session/auth state |
| Signup form | `POST /auth/signup` | User identity |
| Account profile form | `PUT /api/user/update/{id}` | User profile |
| IMAP connect form | `POST /api/user/imap/{id}` | IMAP account configuration |
| Folder table | `GET /api/emails/{folder}` | Email metadata rows |
| Email detail page | `GET /api/emails/{mailId}` | Email body HTML/text |

## Browser-side transient stores
- `localStorage.userId`
- `localStorage.mailhub_active_account`

## Risk note
Persisting IMAP password in localStorage and forwarding via request headers is a compliance risk and should be replaced by backend tokenized mailbox sessions.
