"""Hardcoded Contact360 product roadmap for DocsAI (no markdown loader)."""

CONTACT360_VERSION = "1.0.0 (MVP)"
CONTACT360_PRODUCT = "Contact360"

CONTACT360_ROADMAP_STAGES = [
    {
        "id": "1.1",
        "stage": "Stage 1.1",
        "title": "User & Authentication System",
        "status": "completed",
        "features": [
            "Email Signup & Login",
            "Basic User Profile",
            "Auto credit assignment (50 credits)",
            "Session management",
        ],
    },
    {
        "id": "1.2",
        "stage": "Stage 1.2",
        "title": "Credit Management System (CORE)",
        "status": "completed",
        "features": [
            "Credit balance tracking",
            "Credit deduction per action: Finder, Verifier",
            "Free credits (50 on signup)",
            "Credit usage logs (basic)",
            "Block actions when credits = 0",
            "Credits will lapse when the premium pack is over.",
        ],
    },
    {
        "id": "1.4",
        "stage": "Stage 1.4",
        "title": "Email Finder Engine",
        "status": "completed",
        "features": [
            "Predefined pattern generation (10 formats)",
            "Generate possible valid email",
            "Historical logs should show on the same page",
        ],
    },
    {
        "id": "1.5",
        "stage": "Stage 1.5",
        "title": "Email Verification Engine",
        "status": "completed",
        "features": [
            "Integrate 1 external API (e.g., Mailvetter)",
            "Basic checks: Valid / Delivered-Catchall / Un delivered-Catchall / Invalid / Not Found — confidence score (if API provides)",
        ],
    },
    {
        "id": "1.6",
        "stage": "Stage 1.6",
        "title": "Results Engine",
        "status": "completed",
        "features": [
            "Show: Best email; Status (Valid / Delivered-Catchall / Un delivered-Catchall / Invalid / Not Found); Confidence (if API provides)",
            "Show the logs of email validation",
        ],
    },
    {
        "id": "1.8",
        "stage": "Stage 1.8",
        "title": "Bulk Processing — Validation (LIMITED MVP)",
        "status": "in_progress",
        "features": [
            "If included: CSV upload (basic)",
            "Max limit (e.g., 30 concurrency)",
        ],
    },
    {
        "id": "1.10",
        "stage": "Stage 1.10",
        "title": "Billing & Payments",
        "status": "in_progress",
        "features": [
            "Credit purchase system",
            "2–3 pricing plans only",
            "Manual Payment Integration (whatever is suitable)",
            "No subscription complexity (credit packs only)",
        ],
    },
    {
        "id": "1.11",
        "stage": "Stage 1.11",
        "title": "Analytics for the User (Minimal)",
        "status": "planned",
        "features": [
            "User Logs",
            "Credits used",
            "Package / Expiry showing",
        ],
    },
    {
        "id": "1.12",
        "stage": "Stage 1.12",
        "title": "Notifications (Minimal)",
        "status": "planned",
        "features": [
            "Low credit warning (UI only)",
            "Payment success message",
            "No email automation in v1",
        ],
    },
    {
        "id": "1.13",
        "stage": "Stage 1.13",
        "title": "Analytics Admin Panel (Basic Control)",
        "status": "planned",
        "features": [
            "View users (Package & Expiry)",
            "View credits",
            "Manually adjust credits",
            "View usage logs",
        ],
    },
    {
        "id": "1.14",
        "stage": "Stage 1.14",
        "title": "Security (Basic Layer)",
        "status": "planned",
        "features": [
            "Rate limiting (basic)",
            "Prevent spam usage",
        ],
    },
]
