"""
Roadmap constants — mirrors docs/docs/roadmap.md.
Update this file whenever roadmap.md changes (docsai-sync protocol).
"""

ERAS = [
    {
        "number": "0",
        "name": "Foundation and pre-product stabilization",
        "status": "completed",
        "era_pct": 100,
    },
    {
        "number": "1",
        "name": "Contact360 user and billing and credit system",
        "status": "in_progress",
        "era_pct": 60,
    },
    {
        "number": "2",
        "name": "Contact360 email system",
        "status": "planned",
        "era_pct": 10,
    },
    {
        "number": "3",
        "name": "Contact360 contact and company data system",
        "status": "planned",
        "era_pct": 0,
    },
    {
        "number": "4",
        "name": "Contact360 Extension and Sales Navigator maturity",
        "status": "planned",
        "era_pct": 0,
    },
    {
        "number": "5",
        "name": "Contact360 AI workflows",
        "status": "planned",
        "era_pct": 0,
    },
    {
        "number": "6",
        "name": "Contact360 Reliability and Scaling",
        "status": "planned",
        "era_pct": 0,
    },
    {"number": "7", "name": "Contact360 deployment", "status": "planned", "era_pct": 0},
    {
        "number": "8",
        "name": "Contact360 public and private APIs and endpoints",
        "status": "planned",
        "era_pct": 0,
    },
    {
        "number": "9",
        "name": "Contact360 Ecosystem integrations and Platform productization",
        "status": "planned",
        "era_pct": 0,
    },
    {
        "number": "10",
        "name": "Contact360 email campaign",
        "status": "planned",
        "era_pct": 0,
    },
]

STATUS_COLOR = {
    "completed": "success",
    "in_progress": "warning",
    "planned": "neutral",
}
