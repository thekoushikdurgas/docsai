# Contact360 — User Guide

> **Your complete guide to uploading contacts, enriching data, running campaigns, and using the AI assistant.**
> Version 1.0 · April 2026

---

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Step 1 — Upload Data (CSV)](#2-step-1--upload-data-csv)
3. [Step 2 — Enrich Data](#3-step-2--enrich-data)
4. [Step 3 — Create a Campaign](#4-step-3--create-a-campaign)
5. [Step 4 — Schedule Campaign](#5-step-4--schedule-campaign)
6. [Step 5 — Track Results](#6-step-5--track-results)
7. [Step 6 — AI Assistant](#7-step-6--ai-assistant)
8. [Tips & Best Practices](#8-tips--best-practices)
9. [Troubleshooting](#9-troubleshooting)
10. [Keyboard Shortcuts](#10-keyboard-shortcuts)

---

# 1. Getting Started

## What is Contact360?

Contact360 is an AI-powered CRM platform that helps you:
- **Manage contacts** — import, organise, and enrich your contact list
- **Run campaigns** — send emails, SMS, and LinkedIn messages at scale
- **Track performance** — real-time open rate, click rate, and reply tracking
- **Work with AI** — ask your AI assistant to find leads, draft messages, and automate follow-ups

---

## Your Dashboard at a Glance

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Contact360                          [🔔 Notifications]  [👤 Your Name]  │
├───────────────┬──────────────────────────────────────────────────────────┤
│               │                                                          │
│  📁 Contacts  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  ✉ Campaigns  │   │  👥 Contacts │  │  📧 Emails   │  │  📊 Open    │    │
│  📊 Analytics │   │    12,450   │  │  Sent: 4,200 │  │  Rate: 32%  │    │
│  🤖 AI Agent  │   └─────────────┘  └─────────────┘  └─────────────┘    │
│  ⚙ Settings  │                                                          │
│               │   Recent Activity                  Quick Actions        │
│               │   ─────────────────────────        ──────────────────   │
│               │   ✅ CSV imported (2 min ago)       [+ Upload CSV]       │
│               │   📧 Campaign "Q2 Outreach" sent    [+ New Campaign]     │
│               │   🤖 AI found 45 new leads          [Ask AI]             │
└───────────────┴──────────────────────────────────────────────────────────┘
```

---

## Account Setup Checklist

Before your first campaign, complete these steps:

- [ ] **Connect your email sender** — Settings → Email → Connect Gmail / Outlook / SMTP
- [ ] **Verify your sending domain** — add SPF, DKIM, DMARC DNS records (provided in settings)
- [ ] **Set your timezone** — Settings → Preferences → Timezone (used for AI scheduling)
- [ ] **Invite your team** — Settings → Users → Invite (assign roles: Admin / Manager / User)
- [ ] **Configure unsubscribe link** — Settings → Compliance → Unsubscribe Footer (mandatory)

---

# 2. Step 1 — Upload Data (CSV)

## Supported Import Formats

| Format | Max File Size | Max Rows | Notes |
|--------|--------------|----------|-------|
| CSV (.csv) | 50 MB | 100,000 rows | UTF-8 encoded |
| Excel (.xlsx) | 50 MB | 100,000 rows | First sheet only |
| Google Sheets | — | 100,000 rows | Share link or sync |
| Manual entry | — | 1 at a time | Via Contacts → Add Contact |

---

## How to Upload a CSV

### Step 1.1 — Prepare Your CSV

Your CSV should have a header row. Recommended columns:

```csv
first_name,last_name,email,phone,company,job_title,linkedin_url,source
John,Smith,john@acme.com,+919876543210,Acme Corp,VP Sales,https://linkedin.com/in/johnsmith,linkedin
Priya,Mehta,,+918765432109,TechStart,Founder,,manual
```

**Required:** At least one of `email` or `phone`
**Optional but recommended:** `first_name`, `last_name`, `company`, `job_title`, `linkedin_url`

> 💡 **Tip:** The more data you provide, the higher your enrichment match rate.
> Contacts with email + company name enrich at ~85% accuracy vs ~40% with phone only.

---

### Step 1.2 — Upload the File

1. Click **Contacts** in the left sidebar
2. Click **Import CSV** (top-right button)
3. Drag and drop your `.csv` file, or click **Browse Files**
4. Contact360 auto-detects your column headers

```
┌─────────────────────────────────────────────────────────────┐
│  Import Contacts                                            │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│         ┌───────────────────────────────────┐              │
│         │                                   │              │
│         │   📂  Drop your CSV here          │              │
│         │       or click to browse          │              │
│         │                                   │              │
│         └───────────────────────────────────┘              │
│                                                             │
│  ✅ Accepts: .csv, .xlsx, .xls (max 50MB, 100k rows)       │
└─────────────────────────────────────────────────────────────┘
```

---

### Step 1.3 — Map Your Columns

Contact360 will show a mapping screen. Review and adjust:

```
Your CSV Column          →    Contact360 Field
─────────────────────────────────────────────────
"first_name"             →    First Name       ✅ (auto-matched)
"last_name"              →    Last Name        ✅ (auto-matched)
"email"                  →    Email            ✅ (auto-matched)
"mobile"                 →    Phone            ✅ (auto-matched)
"org"                    →    Company          ⚠ Please confirm
"title"                  →    Job Title        ⚠ Please confirm
"notes"                  →    [Skip]  ▼        ← drop-down to map
```

- **Green ✅** = auto-matched with high confidence
- **Orange ⚠** = review needed — click the dropdown to correct
- **[Skip]** = this column will not be imported

---

### Step 1.4 — Import Settings

Before confirming, configure:

| Option | Description | Recommendation |
|--------|-------------|----------------|
| **Duplicate handling** | Skip / Update / Create new | Use **Update existing** |
| **Assign to list** | Tag contacts with a list name | e.g. "Q2 Leads" |
| **Assign owner** | Default owner for new contacts | Your name or team |
| **Notify on complete** | Email when import finishes | ✅ Enable for large files |

---

### Step 1.5 — Review Import Results

After upload, you'll see a summary:

```
Import Complete ✅
─────────────────────────────────────────
  📥 Total rows in file:        5,000
  ✅ Successfully imported:     4,832
  ♻️  Duplicates updated:          98
  ⚠️  Skipped (invalid email):     70
  ──────────────────────────────────
  📋 Download error report →   [errors.csv]
```

Click **Download error report** to see which rows were skipped and why (e.g., invalid email format, missing required fields).

---

## CSV Field Reference

| Field Name | Type | Example | Notes |
|-----------|------|---------|-------|
| `first_name` | Text | `Priya` | — |
| `last_name` | Text | `Mehta` | — |
| `email` | Email | `priya@startup.io` | Must be valid format |
| `phone` | E.164 | `+919876543210` | Include country code |
| `company` | Text | `TechStart` | Used for enrichment matching |
| `job_title` | Text | `Founder` | — |
| `linkedin_url` | URL | `https://linkedin.com/in/...` | Must start with https:// |
| `source` | Text | `linkedin`, `event`, `referral` | Custom value |
| `tags` | Text | `hot-lead,q2` | Comma-separated, no spaces |
| `owner_email` | Email | `you@company.com` | Must match a team member |
| `custom_field_1` | Any | `Enterprise` | Up to 20 custom fields |

---

# 3. Step 2 — Enrich Data

Enrichment fills in missing contact details — emails, phone numbers, job titles, and company info — automatically using Contact360's data providers.

## Enrichment Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│  Your Contact (before enrichment)      After Enrichment              │
│  ──────────────────────────────────    ─────────────────────────────  │
│  Name:      Rahul Sharma               Name:      Rahul Sharma       │
│  Company:   Flipkart                   Company:   Flipkart           │
│  Email:     ❌ missing                 Email:     ✅ rahul@flipkart.com│
│  Phone:     ❌ missing                 Phone:     ✅ +91 98765 43210   │
│  Title:     ❌ missing                 Title:     ✅ Head of Growth    │
│  LinkedIn:  ❌ missing                 LinkedIn:  ✅ /in/rahulsharma  │
│  Confidence: —                         Confidence: 🟢 High (91%)     │
└──────────────────────────────────────────────────────────────────────┘
```

---

## A — Generate / Find Emails

### Single contact
1. Open a contact profile
2. Click **Find Email** (magic wand icon next to the email field)
3. Contact360 queries Hunter.io + Apollo + internal pattern matching
4. Results show with a **confidence score** (High / Medium / Low)

### Bulk email generation
1. Go to **Contacts** → select contacts using checkboxes
2. Click **Bulk Actions** → **Find Emails**
3. Choose how many to enrich (credits are deducted per result found)
4. Results are populated automatically when found

> 💡 **How it works:** Contact360 uses the contact's name + company domain to
> pattern-match email formats (e.g., `{first}.{last}@company.com`), then
> validates deliverability before storing.

---

## B — Validate Emails

Email validation checks whether an email address is actually deliverable before you send.

### Validation statuses explained

| Status | Meaning | Action |
|--------|---------|--------|
| 🟢 **Valid** | Inbox confirmed deliverable | Safe to send |
| 🟡 **Risky** | Exists but may bounce (catch-all domain) | Send with caution |
| 🔴 **Invalid** | Does not exist / will hard bounce | Do not send |
| ⬜ **Unknown** | Cannot verify (server timeout) | Retry later |

### How to validate emails

1. Go to **Contacts** → filter by "Email not validated"
2. Select all → **Bulk Actions** → **Validate Emails**
3. Watch the status column update in real time
4. Invalid emails are automatically excluded from campaigns

> ⚠️ **Important:** Contact360 automatically blocks sending to **Invalid** emails.
> Sending to unvalidated emails increases your bounce rate and damages your
> sender reputation. Always validate before campaigns.

---

## C — Find Phone Numbers

1. Open a contact (or select in bulk)
2. Click **Find Phone** or **Bulk Actions → Find Phones**
3. Contact360 searches for mobile and direct dial numbers
4. Phone numbers are stored in E.164 format (`+91XXXXXXXXXX`)
5. Indian numbers are automatically DND-checked (TRAI compliance)

### Phone number types

| Type | Example | Best for |
|------|---------|---------|
| Mobile | `+91 98765 43210` | WhatsApp, SMS, calls |
| Direct dial | `+91 22 6789 1234` | Calls only |
| Company HQ | `+91 80 4567 8900` | Fallback only |

---

## Enrichment Credits

Enrichment uses credits from your plan:

| Action | Credits Used |
|--------|-------------|
| Find email (successful) | 1 credit |
| Find email (not found) | 0 credits |
| Validate email | 0.1 credits |
| Find phone (successful) | 2 credits |
| Enrich full profile | 3 credits |

Check your remaining credits: **Settings → Plan → Credits**

---

# 4. Step 3 — Create a Campaign

## Campaign Types

| Type | Channel | Best For |
|------|---------|---------|
| **Email Campaign** | Email | Cold outreach, newsletters, follow-ups |
| **SMS Campaign** | SMS (Twilio) | Reminders, alerts, short messages |
| **LinkedIn Campaign** | LinkedIn DM | B2B prospecting, warm outreach |
| **WhatsApp Campaign** | WhatsApp API | Customer support, confirmations |
| **Multi-channel** | Email + SMS | High-priority prospects |

---

## Creating an Email Campaign — Step by Step

### Step 3.1 — Name and Goal

1. Click **Campaigns** → **New Campaign**
2. Fill in:
   - **Campaign name:** e.g. "Q2 SaaS Founders Outreach"
   - **Goal:** Awareness / Lead Generation / Nurture / Re-engagement
   - **Campaign type:** Email
3. Click **Next →**

---

### Step 3.2 — Select Audience

```
┌──────────────────────────────────────────────────────────────────────┐
│  Who should receive this campaign?                                   │
│  ─────────────────────────────────────────────────────────────────── │
│                                                                      │
│  From list:        [Q2 Leads ▼]           2,450 contacts            │
│                                                                      │
│  Filter by:                                                          │
│    Job Title       contains     [Founder, CEO, CTO]         ✅       │
│    Email Status    is           [Valid]                     ✅       │
│    Company Size    is           [11–200, 201–1000]          ✅       │
│    Last contacted  more than    [30 days ago]               ✅       │
│                                                                      │
│  ──────────────────────────────────────────────────────────────────  │
│  Estimated audience:  847 contacts                                   │
│  Excluded (DND/Unsubscribed): 12                                     │
│                                                                      │
│  [← Back]                                    [Next: Template →]     │
└──────────────────────────────────────────────────────────────────────┘
```

> 💡 **AI Audience Suggestion:** Click **"Let AI build this audience"** and describe
> in plain English: *"SaaS founders in India with 10–500 employees who haven't
> been contacted in 30 days"* — the AI will set all filters automatically.

---

### Step 3.3 — Choose Template / Write Email

#### Using a template

1. Click **Browse Templates**
2. Filter by: Industry / Goal / Tone
3. Preview and select
4. Template loads into the editor — customise as needed

#### Writing from scratch

Use the drag-and-drop email editor:

```
┌──────────────────────────────────────────────────────────────────────┐
│  Subject:  [{{first_name}}, quick question about {{company}}   ]    │
│  Preview:  [Hope this finds you well...                        ]    │
│  ───────────────────────────────────────────────────────────────── │
│                                                                      │
│  [Logo]                                                              │
│                                                                      │
│  Hi {{first_name}},                                                  │
│                                                                      │
│  I noticed {{company}} is in the {{industry}} space — we've helped  │
│  similar companies grow pipeline by 3x with automated outreach.     │
│                                                                      │
│  Would you be open to a 15-min call this week?                       │
│                                                                      │
│  Best,                                                               │
│  {{sender_name}}                                                     │
│                                                                      │
│  [Unsubscribe] · [View in browser]                                  │
└──────────────────────────────────────────────────────────────────────┘
```

#### Available personalisation variables

| Variable | Replaced with | Example output |
|----------|--------------|----------------|
| `{{first_name}}` | Contact's first name | `Priya` |
| `{{last_name}}` | Contact's last name | `Mehta` |
| `{{company}}` | Contact's company | `TechStart` |
| `{{job_title}}` | Contact's job title | `Founder` |
| `{{sender_name}}` | Your name | `Koushik` |
| `{{sender_company}}` | Your company | `Contact360` |
| `{{custom_intro}}` | AI-generated opening line | `I saw TechStart just raised...` |
| `{{unsubscribe_link}}` | Auto-inserted unsubscribe URL | *(required by law)* |

> 💡 **AI Personalisation:** Enable **"AI intro lines"** to auto-generate a unique
> first sentence per contact based on their LinkedIn activity, company news, or
> recent funding — dramatically improves reply rates.

---

### Step 3.4 — Add Follow-up Sequence (Optional)

Create an automated multi-touch sequence:

```
Day 0  →  Email 1: Initial outreach
Day 3  →  Email 2: Quick follow-up (if no reply)
Day 7  →  Email 3: Value-add (share a resource)
Day 14 →  Email 4: Break-up email ("Should I stop reaching out?")
Day 21 →  SMS: Short nudge (if phone available)
         ↓
         [Stop if replied at any step]
```

To add a follow-up:
1. Click **+ Add Step** in the sequence builder
2. Choose: Email / SMS / Wait / AI Action
3. Set the delay (e.g., "3 days after previous step")
4. Condition: **"Only if not replied"** ← important!

---

# 5. Step 4 — Schedule Campaign

## Manual Scheduling

```
┌──────────────────────────────────────────────────────────────────────┐
│  Schedule Your Campaign                                              │
│  ───────────────────────────────────────────────────────────────── │
│                                                                      │
│  Send:     ○ Now   ● Scheduled   ○ Recurring                       │
│                                                                      │
│  Date:     [15 April 2026  ▼]                                       │
│  Time:     [09:30 AM       ▼]                                       │
│  Timezone: [Asia/Kolkata (IST) ▼]                                   │
│                                                                      │
│  Send rate: [50 emails/hour ▼]    ← lower = safer for deliverability│
│                                                                      │
│  [← Back]                              [Review & Confirm →]        │
└──────────────────────────────────────────────────────────────────────┘
```

---

## AI-Suggested Best Time ✨

Contact360's AI analyses your past campaign data and the contact's engagement history to recommend the optimal send time.

### How to use it

1. On the Schedule screen, click **"Ask AI for best time"**
2. The AI returns a recommendation like:

```
┌─────────────────────────────────────────────────────────────────────┐
│  🤖 AI Scheduling Recommendation                                    │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                      │
│  Best send time:   Tuesday, 15 Apr · 9:15 AM IST                   │
│                                                                      │
│  Why:                                                                │
│  • Your audience (SaaS founders, India) shows highest open rates   │
│    on Tue–Thu between 9 AM–11 AM IST                               │
│  • Your last 3 campaigns had 31% open rate on Tuesdays vs          │
│    18% on Fridays                                                   │
│  • Avoiding: Monday (inbox flood), Friday (low engagement)         │
│                                                                      │
│  Predicted open rate:  ~34%  (vs your average 28%)                 │
│                                                                      │
│  [Use AI Suggestion ✓]              [Choose my own time]           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Scheduling Options

| Option | Description | Best For |
|--------|-------------|---------|
| **Send now** | Sends immediately on confirm | Urgent, time-sensitive |
| **Scheduled** | Fixed date + time | Planned campaigns |
| **Recurring** | Daily / Weekly / Monthly | Newsletters, digests |
| **AI optimised** | AI picks best time per recipient | Max engagement |
| **Send in batches** | Spread sends over X hours | Warming new domains |

> ⚠️ **Deliverability tip:** If your domain is new (< 60 days old), use
> **Send in batches** and keep your daily volume under 200 emails/day for the
> first 2 weeks. Contact360 warns you automatically if your volume exceeds
> safe warm-up limits.

---

## Pre-Send Checklist

Contact360 runs this automatically before confirming your schedule:

```
✅ Subject line: 47 characters (good)
✅ Preview text: set
✅ Unsubscribe link: present
✅ Sender name + reply-to: configured
✅ Email validated: 100% of audience
⚠️ Spam words detected: "FREE" in subject — consider rewording
✅ SPF / DKIM: verified
✅ Links tested: 3/3 links working
✅ Plain text version: auto-generated
```

Resolve all ⚠️ warnings before sending for best deliverability.

---

# 6. Step 5 — Track Results

## Campaign Analytics Dashboard

```
┌──────────────────────────────────────────────────────────────────────┐
│  Campaign: "Q2 SaaS Founders Outreach"           Apr 15 · 9:15 AM   │
│  ───────────────────────────────────────────────────────────────── │
│                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ Sent     │  │ Opened   │  │ Clicked  │  │ Replied  │           │
│  │  847     │  │  271     │  │  89      │  │  34      │           │
│  │  100%    │  │  32.0%   │  │  10.5%   │  │  4.0%   │           │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │
│                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ Bounced  │  │ Unsubscr │  │ Spam     │  │ Pending  │           │
│  │   8      │  │   3      │  │   1      │  │   0      │           │
│  │  0.9%    │  │  0.4%    │  │  0.1%   │  │  0%      │           │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │
│                                                                      │
│  [View Opens Timeline]  [View Click Map]  [Export Report]          │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Metrics Explained

### Open Rate
The percentage of recipients who opened the email.

```
Open Rate = (Unique Opens ÷ Emails Delivered) × 100

Good:        > 25%
Average:     15–25%
Needs work:  < 15%
```

> 💡 Note: Apple Mail Privacy Protection (iOS 15+) inflates open rates.
> Contact360 shows both "raw" and "privacy-adjusted" open rates.

---

### Click Rate (CTR)
The percentage of recipients who clicked at least one link.

```
Click Rate = (Unique Clicks ÷ Emails Delivered) × 100

Good:        > 5%
Average:     2–5%
Needs work:  < 2%
```

---

### Reply Rate
The percentage of recipients who replied to the email. This is the most important metric for outbound sales campaigns.

```
Reply Rate = (Total Replies ÷ Emails Delivered) × 100

Good:        > 5%
Average:     2–5%
Needs work:  < 2%
```

---

### Bounce Rate

| Bounce Type | Meaning | Action |
|-------------|---------|--------|
| **Hard bounce** | Email address doesn't exist | Remove immediately |
| **Soft bounce** | Inbox full / server timeout | Retry after 3 days |
| **Spam complaint** | Marked as spam by recipient | Remove + investigate |

> ⚠️ Keep your hard bounce rate under **2%** and spam rate under **0.1%**.
> Exceeding these thresholds triggers automatic campaign pause.

---

## Opens Timeline Chart

Track when your contacts opened the email throughout the day:

```
Opens
 80 │
    │      ████
 60 │      ████ ████
    │      ████ ████
 40 │ ████ ████ ████      ████
    │ ████ ████ ████      ████ ████
 20 │ ████ ████ ████      ████ ████
    │ ████ ████ ████ ████ ████ ████ ████
  0 └────────────────────────────────────────
     6AM  8AM  10AM  12PM  2PM  4PM  6PM  8PM
```

Use this to choose the best send time for your next campaign.

---

## Contact-Level Tracking

Click on any contact to see their individual journey:

```
Rahul Sharma — rahul@flipkart.com
─────────────────────────────────────────────────────
  Apr 15 · 9:17 AM    ✅ Email delivered
  Apr 15 · 10:42 AM   👁 Opened (Bangalore, Chrome)
  Apr 15 · 10:43 AM   🔗 Clicked: "Book a call" link
  Apr 15 · 11:05 AM   💬 Replied: "Yes, let's connect"
  Apr 15 · 11:10 AM   🤖 AI flagged as: HOT LEAD 🔥
```

---

## Exporting Reports

1. Go to **Campaigns** → open your campaign
2. Click **Export Report** (top right)
3. Choose format: CSV / PDF / Google Sheets

Report includes: per-contact open/click/reply data, timestamps, device info, and link breakdown.

---

# 7. Step 6 — AI Assistant

The Contact360 AI Assistant understands your CRM data and can take actions on your behalf — from finding leads to sending follow-up emails.

## Opening the AI Assistant

- Click **🤖 AI Assistant** in the left sidebar
- Or press `Cmd+K` / `Ctrl+K` from anywhere
- Or click the floating **Ask AI** button (bottom right)

---

## Example Queries

### Finding Leads

```
You:  "Find top leads from my Q2 list"

AI:   I found 23 high-potential leads in your Q2 list based on:
      • Opened your last email within 24 hours
      • Job title matches: Founder, CEO, Head of Growth
      • Company raised funding in the last 6 months

      Top 5:
      1. 🔥 Rahul Sharma, Flipkart — opened 3 emails, clicked 2 links
      2. 🔥 Priya Mehta, TechStart — replied to email 2
      3. 🟡 Amit Joshi, Razorpay — opened but not clicked
      4. 🟡 Sneha Rao, CRED — new contact, high enrichment score
      5. 🟡 Karan Singh, Zepto — viewed profile via extension

      [View all 23 leads →]   [Create audience from these →]
```

---

### Sending Follow-up Emails

```
You:  "Send a follow-up email to everyone who opened but didn't reply"

AI:   I found 182 contacts who opened your "Q2 SaaS Founders Outreach"
      campaign but haven't replied.

      Suggested follow-up email:

      Subject: "Still interested, {{first_name}}?"

      Hi {{first_name}},

      I noticed you opened my last email about [your product] —
      wanted to quickly follow up in case it got lost.

      Would 15 minutes this week work for a quick call?

      [Book time here → calendly.com/...]

      Best, Koushik

      ──────────────────────────────────────────
      Send to: 182 contacts
      Schedule: Tomorrow, 9:30 AM IST (AI recommended)

      [Edit email]   [Approve & Schedule ✓]   [Cancel]
```

---

### Other Things You Can Ask

| Ask the AI | What it does |
|-----------|-------------|
| *"Who hasn't been contacted in 30 days?"* | Filters contacts + shows list |
| *"Which campaign had the best reply rate?"* | Analytics summary |
| *"Enrich all contacts missing a phone number"* | Starts bulk enrichment |
| *"Draft a re-engagement email for cold leads"* | Writes email template |
| *"Add everyone who replied to a new list called Hot Leads"* | Creates list + moves contacts |
| *"Show me contacts at companies with 50–200 employees"* | Filtered contact view |
| *"What's my best sending day this week?"* | Scheduling recommendation |
| *"Generate a personalised intro line for Rahul at Flipkart"* | AI copywriting |
| *"Summarise replies from the Q2 campaign"* | Reply analysis + sentiment |
| *"Unsubscribe everyone who marked as spam"* | Compliance action |

---

## AI Action Approval

For actions that modify data (sending emails, updating contacts, deleting records), the AI always asks for your approval first:

```
┌─────────────────────────────────────────────────────────────────────┐
│  🤖 AI wants to take an action — please review                      │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                      │
│  Action:    Send follow-up email                                    │
│  To:        182 contacts (filtered: opened, not replied)            │
│  Template:  "Still interested?" (shown above)                       │
│  Schedule:  Apr 16 · 9:30 AM IST                                   │
│                                                                      │
│  ⚠️  This will send 182 emails and cannot be undone.                │
│                                                                      │
│  [✅ Approve]          [✏️ Edit first]          [❌ Cancel]          │
└─────────────────────────────────────────────────────────────────────┘
```

> The AI **never sends emails or deletes data without your explicit approval.**
> You are always in control.

---

## AI Memory

The AI remembers context within your session and across sessions:

- Your previous campaigns and results
- Contacts you've asked about
- Preferences (e.g., "I prefer sending on Tuesdays")
- Instructions (e.g., "Always exclude contacts at companies > 5000 employees")

To add a persistent instruction: **Settings → AI Assistant → Custom Instructions**

---

# 8. Tips & Best Practices

## CSV Upload
- Always include `company` + `first_name` for best enrichment match rates
- Clean your data before upload — remove rows with no email AND no phone
- Use the tag column to segment contacts at import (saves time later)
- Max 100,000 rows per file — split larger lists into multiple uploads

## Enrichment
- Run email validation BEFORE every campaign, not after
- Re-enrich contacts every 6 months — people change jobs frequently
- High-confidence emails (🟢 Valid) bounce < 2% — always prioritise these

## Campaigns
- Keep subject lines under 50 characters for mobile display
- Personalise the first line — even `"Hi {{first_name}},"` improves open rates by ~10%
- Always preview on mobile before sending (70%+ of emails are read on mobile)
- Include ONE clear CTA per email — not three competing buttons
- A/B test your subject line on 20% of the list before the full send

## Scheduling
- Best days (general): Tuesday, Wednesday, Thursday
- Best times (India): 9–11 AM, 2–4 PM IST
- Avoid: Monday morning, Friday afternoon, holidays
- Use AI scheduling for personalised per-recipient timing

## Deliverability
- Warm up new domains: start at 50/day, double weekly up to 500+
- Keep hard bounce rate < 2%
- Keep spam complaint rate < 0.1%
- Always include a plain-text version (Contact360 generates this automatically)
- Authenticate your domain: SPF + DKIM + DMARC (Settings → Email → Domain)

---

# 9. Troubleshooting

## Import Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| "Encoding error" on upload | File is not UTF-8 | Re-save CSV as UTF-8 in Excel (Save As → CSV UTF-8) |
| Columns not auto-detected | No header row | Add a header row as the first line |
| "Duplicate contact" warning | Email already exists | Choose "Update existing" in import settings |
| Phone numbers import as wrong format | Missing country code | Add `+91` prefix to all Indian numbers |
| Import stuck at 0% | File > 50 MB | Split file into multiple CSVs and upload separately |

## Enrichment Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| Low email find rate | Insufficient contact data | Add company name + full name |
| Email found but "Risky" | Catch-all domain | Send a small test batch; monitor bounces |
| Phone marked "DND" | TRAI DND registration | Cannot send SMS — use email instead |
| Credits running out fast | Bulk enrichment | Prioritise contacts by enrichment score first |

## Campaign Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| Campaign stuck in "Sending" | Rate limit or provider issue | Wait 10 min; if stuck, contact support |
| High bounce rate | Unvalidated emails | Always validate before sending |
| Low open rate | Bad subject line or wrong send time | A/B test subjects; use AI scheduling |
| Spam complaints | Too frequent / irrelevant emails | Review targeting; reduce frequency |
| "Domain not verified" error | DNS records missing | Settings → Email → Domain → copy DNS records |

---

# 10. Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd/Ctrl + K` | Open AI Assistant |
| `Cmd/Ctrl + N` | New contact |
| `Cmd/Ctrl + I` | Import CSV |
| `Cmd/Ctrl + F` | Search contacts |
| `Cmd/Ctrl + E` | Enrich selected contacts |
| `Cmd/Ctrl + Shift + C` | New campaign |
| `Cmd/Ctrl + Shift + A` | View analytics |
| `Escape` | Close modal / dismiss panel |
| `?` | Show all keyboard shortcuts |

---

*Contact360 User Guide · Version 1.0 · April 2026*
*For support: support@contact360.io · Docs: docs.contact360.io*
