"""Script to append specific links to relevant markdown files in the documentation."""
import os

links_to_add = {
    "architecture.md": [
        "\n\n## Operations & Runbooks",
        "- [Appointment360 Runbook](ops/runbooks/appointment360.md)",
        "- [Connectra Runbook](ops/runbooks/connectra.md)",
        "- [Contact AI Runbook](ops/runbooks/contact-ai.md)",
        "- [Email API (Go) Runbook](ops/runbooks/emailapigo.md)",
        "- [Email APIs Runbook](ops/runbooks/emailapis.md)",
        "- [Jobs Runbook](ops/runbooks/jobs.md)",
        "- [Logs API Runbook](ops/runbooks/logs-api.md)",
        "- [Resume AI Runbook](ops/runbooks/resumeai.md)",
        "- [S3 Storage Runbook](ops/runbooks/s3storage.md)",
    ],
    "backend.md": [
        "\n\n## System & API Contracts",
        "- [Service Mesh Contracts](backend/apis/00_SERVICE_MESH_CONTRACTS.md)",
        "- [SalesNavigator UUID5 Contract](backend/apis/17_SALESNAVIGATOR_UUID5_CONTRACT.md)",
        "- [Foundation Exit Gate Signoff](backend/apis/21_FOUNDATION_EXIT_GATE_SIGNOFF.md)",
    ],
    "governance.md": [
        "\n\n## Quality Gates & Checklists",
        "- [Era Subchecklist Template](promsts/checklists/era-subchecklist-template.md)",
        "- [Prompt Quality Gate](promsts/checklists/prompt-quality-gate.md)",
    ],
    "docsai-sync.md": [
        "\n\n## AI Workspace Logs & Sync Activity",
        "- [Cursor Documentation File Ex](analysis/cursor_contact360_documentation_file_ex.md)",
        "- [Cursor Directory Exploration](analysis/cursor_directory_exploration_and_file_c.md)",
        "- [Cursor Content Retrieval 1](analysis/cursor_documentation_content_retrieval1.md)",
        "- [Cursor Content Retrieval](analysis/cursor_documentation_file_content_retri.md)",
        "- [Cursor Folder Exploration](analysis/cursor_documentation_folder_exploration.md)",
        "- [Cursor Structure Exploration](analysis/cursor_documentation_structure_explorat.md)",
        "- [Cursor File Content & Label](analysis/cursor_file_content_retrieval_and_label.md)",
    ],
    "codebase.md": [
        "\n\n## Attached Analysis & Task Packs",
        "- [Appointment360 Foundation Task Pack]"
        "(analysis/appointment360-foundation-task-pack (1).md)",
        "- [Appointment360 User Billing Task Pack]"
        "(analysis/appointment360-user-billing-task-pack (1).md)",
        "- [Connectra Foundation Task Pack]"
        "(analysis/connectra-foundation-task-pack (1).md)",
        "- [Contact AI Foundation Task Pack]"
        "(analysis/contact-ai-foundation-task-pack (1).md)",
        "- [Contact360 E2E Architecture Flow]"
        "(analysis/Contact360 End-to-End Architecture and Flow.md)",
        "- [Email APIs Foundation Task Pack]"
        "(analysis/emailapis-foundation-task-pack (1).md)",
        "- [Sync Codebase Analysis](codebases/sync-codebase-analysis.md)",
    ],
    "frontend.md": [
        "\n\n## Assets & Exports",
        "- [Pages Export Excel](frontend/excel/pages_export_2026-03-16.xlsx)",
    ],
    "roadmap.md": [
        "\n\n## Historical Refactor Plans",
        "- [Contact360 Docs Overhaul Plan 1](plans/contact360_docs_overhaul_1a3fa187.plan.md)",
        "- [Contact360 Docs Overhaul Plan 2](plans/contact360_docs_overhaul_9f8e9039.plan.md)",
    ]
}

for parent_file, lines in links_to_add.items():
    if not os.path.exists(parent_file):
        print(f"Warning: {parent_file} does not exist.")
        continue

    with open(parent_file, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Appended links to {parent_file}")
