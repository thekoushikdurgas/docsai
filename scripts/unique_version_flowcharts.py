"""
Per-file unique Flowchart content for docs/versions/version_*.md.
Each (major, minor) gets a distinct delivery stage label and runtime mermaid body.
Mermaid: avoid double-quotes inside node labels; use camelCase IDs.

Apply to the repo:  python scripts/apply_unique_flowcharts.py
"""
from __future__ import annotations

import re
from typing import Callable


def _td(label: str) -> str:
    """Escape for mermaid node label in double quotes."""
    return label.replace('"', "'")


def delivery_section(stage_label: str, runtime_mermaid: str) -> str:
    sl = _td(stage_label)
    return f"""## Flowchart

Delivery work for this minor follows the five-track model (contract, service, surface, data, ops) through a release gate.

```mermaid
flowchart TD
    stageNode["{sl}"]
    contract["Contract"]
    service["Service"]
    surface["Surface"]
    data["Data"]
    ops["Ops"]
    releaseGate["Release gate"]

    stageNode --> contract
    stageNode --> service
    stageNode --> surface
    stageNode --> data
    stageNode --> ops
    contract --> releaseGate
    service --> releaseGate
    surface --> releaseGate
    data --> releaseGate
    ops --> releaseGate
```

### Runtime focus (unique to this minor)

```mermaid
{runtime_mermaid.strip()}
```

See also: [`docs/flowchart.md`](../flowchart.md) for system-wide and master views.

"""


# --- Runtime bodies (no outer fences) ---

def r_0_0() -> str:
    return """
flowchart LR
    pre["Pre-repo concepts"]
    contracts["Data contracts undefined"]
    pre --> contracts
"""


def r_0_1() -> str:
    return """
flowchart LR
    repo["Monorepo root"]
    api["Appointment360"]
    sync["Connectra"]
    jobs["TKD Job"]
    s3["s3storage"]
    repo --> api
    repo --> sync
    repo --> jobs
    repo --> s3
"""


def r_0_2() -> str:
    return """
flowchart TB
    apiDb["appointment360 Postgres"]
    jobDb["tkdjob Postgres"]
    alembic["Alembic migrations"]
    ci["Migration CI gates"]
    alembic --> apiDb
    alembic --> jobDb
    alembic --> ci
"""


def r_0_3() -> str:
    return """
flowchart LR
    gw["Gateway"]
    lambdas["Downstream Lambdas"]
    apiKey["X-API-Key rotation"]
    errors["Unified error shapes"]
    gw --> lambdas
    apiKey --> gw
    errors --> gw
"""


def r_0_4() -> str:
    return """
flowchart LR
    jwt["JWT access / refresh"]
    roles["Five-level roles"]
    credits["Credit metering hooks"]
    authMod["01_AUTH_MODULE"]
    jwt --> roles --> credits --> authMod
"""


def r_0_5() -> str:
    return """
flowchart TB
    s3mod["07_S3_MODULE"]
    upl["10_UPLOAD_MODULE"]
    mp["Multipart completion"]
    buckets["Logical buckets"]
    s3mod --> buckets
    upl --> mp --> buckets
"""


def r_0_6() -> str:
    return """
flowchart LR
    dag["job_node plus edges"]
    kafka["Kafka JOBS_TOPIC"]
    sched["Scheduler"]
    consumer["Consumer pool"]
    dag --> sched --> kafka --> consumer
"""


def r_0_7() -> str:
    return """
flowchart LR
    vql["VQL baseline"]
    es["Elasticsearch indexes"]
    pg["Postgres source of truth"]
    syncSvc["Connectra service"]
    vql --> syncSvc --> es
    pg --> syncSvc
"""


def r_0_8() -> str:
    return """
flowchart TB
    next["Next.js App Router"]
    docsai["DocsAI Django"]
    syncDoc["docsai-sync constants"]
    next --> syncDoc
    docsai --> syncDoc
"""


def r_0_9() -> str:
    return """
flowchart LR
    ext["Chrome extension"]
    sn["salesnavigator Lambda"]
    client["lambda_sales_navigator_client"]
    conn["Connectra upsert"]
    ext --> sn --> client --> conn
"""


def r_0_10() -> str:
    return """
flowchart LR
    compose["Docker Compose"]
    sam["SAM templates"]
    health["Health probes"]
    secrets["Secret baseline"]
    compose --> health
    sam --> health
    secrets --> compose
"""


def r_1_0() -> str:
    return """
flowchart LR
    user["User"]
    dash["Dashboard"]
    gw["Appointment360"]
    find["Finder"]
    verify["Verifier"]
    results["Results UI"]
    user --> dash --> gw --> find --> results
    gw --> verify --> results
"""


def r_1_1() -> str:
    return """
flowchart TB
    user["User"]
    dash["Dashboard"]
    gw["Appointment360"]
    jobs["Jobs mutations"]
    tkd["TKD Job"]
    bill["Billing"]
    s3["CSV on S3"]
    user --> dash --> gw
    gw --> jobs --> tkd --> s3
    gw --> bill
"""


def r_1_2() -> str:
    return """
flowchart LR
    user["User"]
    dash["Dashboard"]
    gw["Appointment360"]
    analytics["Analytics module"]
    notify["Notifications"]
    admin["Admin routes"]
    logs["logs.api"]
    user --> dash --> gw --> analytics
    gw --> notify
    gw --> admin --> logs
"""


def r_1_3() -> str:
    return """
flowchart LR
    reserved["Reserved stage 1.3"]
    note["Historical numbering gap"]
    future["Future mapping TBD"]
    reserved --> note --> future
"""


def r_1_4() -> str:
    return """
flowchart LR
    dash["Dashboard"]
    gw["Appointment360"]
    emailapis["emailapis"]
    patterns["Pattern generation"]
    finder["Finder candidates"]
    dash --> gw --> emailapis --> patterns --> finder
"""


def r_1_5() -> str:
    return """
flowchart LR
    gw["Appointment360"]
    email["15_EMAIL_MODULE"]
    mailvetter["mailvetter"]
    status["Deliverability status"]
    gw --> email --> mailvetter --> status
"""


def r_1_6() -> str:
    return """
flowchart LR
    ui["EmailFinderSingle"]
    history["Activity history"]
    bulk["Verifier bulk results"]
    confidence["Confidence display"]
    ui --> history
    ui --> bulk --> confidence
"""


def r_1_7() -> str:
    return """
flowchart LR
    dash["Dashboard"]
    gw["Appointment360"]
    usage["Usage ledger"]
    block["Zero-credit block"]
    dash --> gw --> usage --> block
"""


def r_1_8() -> str:
    return """
flowchart TB
    csv["CSV upload"]
    tkd["TKD Job stream"]
    resume["Resume checkpoints"]
    out["Export download"]
    csv --> tkd --> resume --> out
"""


def r_1_9() -> str:
    return """
flowchart LR
    dash["Dashboard"]
    profile["Profile settings"]
    twofa["2FA hooks"]
    dash --> profile --> twofa
"""


def r_1_10() -> str:
    return """
flowchart LR
    dash["Dashboard"]
    billing["Billing GraphQL"]
    upi["UPI or packs"]
    ledger["Credits ledger"]
    dash --> billing --> upi --> ledger
"""


def r_2_0() -> str:
    return """
flowchart LR
    user["User"]
    vql["VQL builder"]
    gw["Appointment360"]
    conn["Connectra"]
    es["Elasticsearch"]
    user --> vql --> gw --> conn --> es
"""


def r_2_1() -> str:
    return """
flowchart TB
    ast["VQL AST"]
    compiler["Compiler"]
    esQuery["ES query"]
    ast --> compiler --> esQuery
"""


def r_2_2() -> str:
    return """
flowchart LR
    saved["Saved searches"]
    gw["Appointment360"]
    conn["Connectra"]
    pg["Postgres"]
    saved --> gw --> conn
    pg --> saved
"""


def r_2_3() -> str:
    return """
flowchart LR
    conn["Connectra"]
    rate["Rate middleware"]
    es["Elasticsearch cluster"]
    health["Cluster health"]
    conn --> rate --> es
    es --> health
"""


def r_2_4() -> str:
    return """
flowchart TB
    contacts["Contacts index"]
    companies["Companies index"]
    dedup["Dedup keys"]
    merge["Merge policy"]
    contacts --> dedup
    companies --> dedup --> merge
"""


def r_2_5() -> str:
    return """
flowchart LR
    gw["Appointment360"]
    conn["Connectra"]
    cache["Query cache layer"]
    es["Elasticsearch"]
    gw --> conn --> cache --> es
"""


def r_2_6() -> str:
    return """
flowchart LR
    ui["Contacts table"]
    facets["Facet filters"]
    vql["VQL string"]
    ui --> facets --> vql
"""


def r_2_7() -> str:
    return """
flowchart TB
    enrich["Enrichment workers"]
    conn["Connectra"]
    es["Elasticsearch"]
    enrich --> conn --> es
"""


def r_2_8() -> str:
    return """
flowchart LR
    company["Company entity"]
    contact["Contact entity"]
    link["Association graph"]
    company --> link
    contact --> link
"""


def r_2_9() -> str:
    return """
flowchart LR
    user["User"]
    limit["Per-tenant limits"]
    conn["Connectra"]
    throttle["Throttle decisions"]
    user --> limit --> throttle --> conn
"""


def r_2_10() -> str:
    return """
flowchart LR
    roadmap["2.x roadmap buffer"]
    conn["Connectra"]
    nextEra["Handoff to 3.x"]
    roadmap --> conn --> nextEra
"""


def r_3_0() -> str:
    return """
flowchart LR
    ext["Extension"]
    sn["salesnavigator"]
    gw["Appointment360"]
    conn["Connectra"]
    ext --> gw
    ext --> sn --> conn
"""


def r_3_1() -> str:
    return """
flowchart LR
    ext["Extension"]
    token["Session token"]
    gw["Appointment360"]
    ext --> token --> gw
"""


def r_3_2() -> str:
    return """
flowchart TB
    scrape["SN scrape"]
    save["save_service"]
    bulk["Bulk upsert"]
    scrape --> save --> bulk
"""


def r_3_3() -> str:
    return """
flowchart LR
    gw["Appointment360"]
    sn["salesnavigator"]
    conn["Connectra"]
    profile["profile_url key"]
    gw --> sn --> conn --> profile
"""


def r_3_4() -> str:
    return """
flowchart LR
    ext["Extension"]
    refresh["Session refresh"]
    gw["Appointment360"]
    ext --> refresh --> gw
"""


def r_3_5() -> str:
    return """
flowchart LR
    ext["Extension"]
    logs["logs.api"]
    telemetry["Telemetry events"]
    ext --> telemetry --> logs
"""


def r_3_6() -> str:
    return """
flowchart TB
    dup["Duplicate profiles"]
    merge["Merge rules"]
    conn["Connectra index"]
    dup --> merge --> conn
"""


def r_3_7() -> str:
    return """
flowchart LR
    li["LinkedIn module"]
    gw["Appointment360"]
    sn["Sales Navigator"]
    li --> gw --> sn
"""


def r_3_8() -> str:
    return """
flowchart LR
    pkg["Extension package"]
    manifest["Manifest v3"]
    store["Chrome Web Store"]
    pkg --> manifest --> store
"""


def r_3_9() -> str:
    return """
flowchart LR
    ingest["Ingest request"]
    idem["Idempotency key"]
    upsert["Upsert to Connectra"]
    ingest --> idem --> upsert
"""


def r_3_10() -> str:
    return """
flowchart LR
    ext["Extension"]
    e2e["SN to search E2E"]
    integrity["Sync integrity checks"]
    ext --> e2e --> integrity
"""


def r_4_0() -> str:
    return """
flowchart LR
    user["User"]
    dash["ai-chat"]
    gw["Appointment360"]
    ai["contact.ai"]
    llm["Model provider"]
    user --> dash --> gw --> ai --> llm
"""


def r_4_1() -> str:
    return """
flowchart TB
    chat["AI_CHATS_MODULE"]
    rest["contact.ai REST"]
    stream["SSE stream"]
    chat --> rest --> stream
"""


def r_4_2() -> str:
    return """
flowchart LR
    prompt["Prompt template"]
    guard["Safety guardrails"]
    ai["contact.ai"]
    prompt --> guard --> ai
"""


def r_4_3() -> str:
    return """
flowchart LR
    primary["Primary model"]
    fallback["Fallback model"]
    ai["contact.ai router"]
    primary --> ai
    fallback --> ai
"""


def r_4_4() -> str:
    return """
flowchart TB
    score["Confidence score"]
    explain["Explainability text"]
    ui["EmailAssistantPanel"]
    score --> explain --> ui
"""


def r_4_5() -> str:
    return """
flowchart LR
    audit["Prompt audit log"]
    logs["logs.api"]
    admin["DocsAI review"]
    audit --> logs --> admin
"""


def r_4_6() -> str:
    return """
flowchart LR
    tool["Tool calls"]
    ai["contact.ai"]
    gw["Appointment360"]
    tool --> ai --> gw
"""


def r_4_7() -> str:
    return """
flowchart TB
    token["Token budget"]
    throttle["Throttle AI calls"]
    user["User session"]
    token --> throttle --> user
"""


def r_4_8() -> str:
    return """
flowchart LR
    ctx["Conversation context"]
    pg["ai_chats Postgres"]
    retrieve["History retrieve"]
    ctx --> retrieve --> pg
"""


def r_4_9() -> str:
    return """
flowchart LR
    eval["Offline eval set"]
    quality["Quality metrics"]
    release["Model promotion gate"]
    eval --> quality --> release
"""


def r_4_10() -> str:
    return """
flowchart LR
    fourx["4.x buffer"]
    ai["contact.ai"]
    five["Handoff to 5.x reliability"]
    fourx --> ai --> five
"""


def r_5_0() -> str:
    return """
flowchart TB
    gw["Appointment360"]
    tkd["TKD Job"]
    kafka["Kafka"]
    s3["s3storage"]
    logs["logs.api"]
    gw --> tkd --> kafka
    tkd --> s3
    gw --> logs
    tkd --> logs
"""


def r_5_1() -> str:
    return """
flowchart LR
    slo["SLO definitions"]
    budget["Error budgets"]
    report["Reliability report"]
    slo --> budget --> report
"""


def r_5_2() -> str:
    return """
flowchart LR
    write["Write path"]
    idem["Idempotency key"]
    recon["Reconciliation job"]
    write --> idem --> recon
"""


def r_5_3() -> str:
    return """
flowchart TB
    kafka["Kafka topic"]
    dlq["DLQ"]
    replay["Replay tooling"]
    worker["Workers"]
    kafka --> worker
    worker --> dlq --> replay --> worker
"""


def r_5_4() -> str:
    return """
flowchart LR
    trace["Distributed trace"]
    corr["Correlation IDs"]
    logs["logs.api"]
    alert["Alerts"]
    trace --> corr --> logs --> alert
"""


def r_5_5() -> str:
    return """
flowchart LR
    api["API latency"]
    search["Search latency"]
    bulk["Bulk throughput"]
    tune["Tuning loop"]
    api --> tune
    search --> tune
    bulk --> tune
"""


def r_5_6() -> str:
    return """
flowchart TB
    s3["S3 objects"]
    lifecycle["Lifecycle rules"]
    retention["Retention policy"]
    s3 --> lifecycle --> retention
"""


def r_5_7() -> str:
    return """
flowchart LR
    cost["Cost signals"]
    budget["Budget guard"]
    throttle["Throttle"]
    cost --> budget --> throttle
"""


def r_5_8() -> str:
    return """
flowchart LR
    edge["Edge requests"]
    waf["Rate limits"]
    abuse["Abuse signals"]
    edge --> waf --> abuse
"""


def r_5_9() -> str:
    return """
flowchart TB
    rc["Release candidate"]
    checks["Validation suite"]
    signoff["Go to 6.x"]
    rc --> checks --> signoff
"""


def r_5_10() -> str:
    return """
flowchart LR
    five["5.x era"]
    buffer["Minor 5.10 buffer"]
    six["Enterprise 6.x prep"]
    five --> buffer --> six
"""


def r_6_0() -> str:
    return """
flowchart TB
    gw["Appointment360"]
    rbac["RBAC enforcement"]
    audit["Audit events"]
    logs["logs.api"]
    gw --> rbac --> audit --> logs
"""


def r_6_1() -> str:
    return """
flowchart LR
    matrix["Permission matrix"]
    ctx["GraphQL context"]
    resolver["Resolvers"]
    matrix --> ctx --> resolver
"""


def r_6_2() -> str:
    return """
flowchart LR
    svcA["Service A"]
    svcB["Service B"]
    mTLS["Service authz"]
    svcA --> mTLS --> svcB
"""


def r_6_3() -> str:
    return """
flowchart TB
    admin["Admin mutation"]
    approval["Approval flow"]
    audit["Audit trail"]
    admin --> approval --> audit
"""


def r_6_4() -> str:
    return """
flowchart LR
    event["Immutable audit event"]
    store["Event store"]
    report["Compliance report"]
    event --> store --> report
"""


def r_6_5() -> str:
    return """
flowchart TB
    classify["Data classification"]
    retention["Retention rules"]
    delete["Deletion workflow"]
    classify --> retention --> delete
"""


def r_6_6() -> str:
    return """
flowchart LR
    tenantA["Tenant A"]
    tenantB["Tenant B"]
    policy["Policy boundary"]
    tenantA --> policy
    tenantB --> policy
"""


def r_6_7() -> str:
    return """
flowchart LR
    secrets["Secret store"]
    rotation["Rotation job"]
    priv["Privileged ops"]
    secrets --> rotation --> priv
"""


def r_6_8() -> str:
    return """
flowchart LR
    tenant["Tenant scope"]
    report["Governance report"]
    ops["Operational KPIs"]
    tenant --> report --> ops
"""


def r_6_9() -> str:
    return """
flowchart LR
    rc["Enterprise RC"]
    validate["Control validation"]
    seven["Analytics 7.x gate"]
    rc --> validate --> seven
"""


def r_6_10() -> str:
    return """
flowchart LR
    six["6.x era"]
    buffer["Minor 6.10 buffer"]
    seven["7.x analytics prep"]
    six --> buffer --> seven
"""


def r_7_0() -> str:
    return """
flowchart TB
    events["Product events"]
    pipe["Analytics pipeline"]
    dash["Analytics UI"]
    events --> pipe --> dash
"""


def r_7_1() -> str:
    return """
flowchart LR
    dict["Metric dictionary"]
    validate["Schema validate"]
    emit["Emit events"]
    dict --> validate --> emit
"""


def r_7_2() -> str:
    return """
flowchart LR
    dash["Dashboard"]
    ext["Extension"]
    gw["Appointment360"]
    sink["Analytics sink"]
    dash --> gw --> sink
    ext --> sink
"""


def r_7_3() -> str:
    return """
flowchart TB
    ingest["Ingestion"]
    dedupe["Dedupe"]
    dlq["Analytics DLQ"]
    ingest --> dedupe --> dlq
"""


def r_7_4() -> str:
    return """
flowchart LR
    lineage["Lineage graph"]
    quality["Quality checks"]
    fresh["Freshness SLO"]
    lineage --> quality --> fresh
"""


def r_7_5() -> str:
    return """
flowchart LR
    user["User"]
    analytics["User analytics page"]
    charts["Charts"]
    user --> analytics --> charts
"""


def r_7_6() -> str:
    return """
flowchart LR
    docsai["DocsAI"]
    admin["Analytics admin"]
    controls["Control views"]
    docsai --> admin --> controls
"""


def r_7_7() -> str:
    return """
flowchart TB
    sched["TKD Job schedule"]
    export["Report export"]
    deliver["Delivery channel"]
    sched --> export --> deliver
"""


def r_7_8() -> str:
    return """
flowchart LR
    query["Heavy query"]
    optimize["Query plan"]
    cost["Cost cap"]
    query --> optimize --> cost
"""


def r_7_9() -> str:
    return """
flowchart LR
    rc["Analytics RC"]
    signoff["Data platform signoff"]
    eight["Integrations 8.x gate"]
    rc --> signoff --> eight
"""


def r_7_10() -> str:
    return """
flowchart LR
    seven["7.x era"]
    buffer["Minor 7.10 buffer"]
    eight["8.x integrations prep"]
    seven --> buffer --> eight
"""


def r_8_0() -> str:
    return """
flowchart LR
    partner["Partner"]
    api["Public API"]
    webhooks["Webhooks"]
    gw["Appointment360"]
    partner --> api --> gw
    partner --> webhooks
"""


def r_8_1() -> str:
    return """
flowchart LR
    ver["API version"]
    deprecate["Deprecation window"]
    compat["Compatibility tests"]
    ver --> deprecate --> compat
"""


def r_8_2() -> str:
    return """
flowchart LR
    partner["Partner identity"]
    scope["Scoped roles"]
    tenant["Tenant boundary"]
    partner --> scope --> tenant
"""


def r_8_3() -> str:
    return """
flowchart TB
    read["External read"]
    write["External write"]
    stable["Stable surface"]
    read --> stable
    write --> stable
"""


def r_8_4() -> str:
    return """
flowchart LR
    event["Signed event"]
    deliver["Webhook delivery"]
    retry["Retry policy"]
    event --> deliver --> retry
"""


def r_8_5() -> str:
    return """
flowchart LR
    partner["Partner"]
    replay["Replay API"]
    recon["Reconciliation"]
    partner --> replay --> recon
"""


def r_8_6() -> str:
    return """
flowchart TB
    sdk["Connector SDK"]
    lifecycle["Lifecycle hooks"]
    registry["Connector registry"]
    sdk --> lifecycle --> registry
"""


def r_8_7() -> str:
    return """
flowchart LR
    health["Integration health"]
    triage["Triage tools"]
    support["Support actions"]
    health --> triage --> support
"""


def r_8_8() -> str:
    return """
flowchart LR
    plan["Plan entitlements"]
    quota["Quota enforcement"]
    partner["Partner usage"]
    plan --> quota --> partner
"""


def r_8_9() -> str:
    return """
flowchart LR
    rc["Integration RC"]
    checks["Partner soak tests"]
    nine["Productization 9.x gate"]
    rc --> checks --> nine
"""


def r_8_10() -> str:
    return """
flowchart LR
    eight["8.x era"]
    buffer["Minor 8.10 buffer"]
    nine["9.x productization prep"]
    eight --> buffer --> nine
"""


def r_9_0() -> str:
    return """
flowchart TB
    tenant["Tenant"]
    gw["Appointment360"]
    ent["Entitlements"]
    admin["Self-serve admin"]
    tenant --> gw --> ent
    admin --> ent
"""


def r_9_1() -> str:
    return """
flowchart LR
    tid["Tenant ID format"]
    claims["JWT claims"]
    propagate["Downstream propagation"]
    tid --> claims --> propagate
"""


def r_9_2() -> str:
    return """
flowchart LR
    admin["Workspace admin"]
    users["User invites"]
    settings["Workspace settings"]
    admin --> users --> settings
"""


def r_9_3() -> str:
    return """
flowchart LR
    plan["Plan engine"]
    runtime["Runtime enforcement"]
    surface["All surfaces"]
    plan --> runtime --> surface
"""


def r_9_4() -> str:
    return """
flowchart LR
    sla["SLA definitions"]
    monitor["SLA monitor"]
    report["Ops report"]
    sla --> monitor --> report
"""


def r_9_5() -> str:
    return """
flowchart TB
    incident["Incident"]
    playbook["Playbook"]
    diag["Tenant diagnostics"]
    incident --> playbook --> diag
"""


def r_9_6() -> str:
    return """
flowchart LR
    region["Region policy"]
    data["Data residency"]
    tenant["Tenant binding"]
    region --> data --> tenant
"""


def r_9_7() -> str:
    return """
flowchart LR
    cost["Cost attribution"]
    forecast["Capacity forecast"]
    finance["Finance guardrails"]
    cost --> forecast --> finance
"""


def r_9_8() -> str:
    return """
flowchart LR
    mig["Tenant migration"]
    automate["Automation"]
    verify["Verification"]
    mig --> automate --> verify
"""


def r_9_9() -> str:
    return """
flowchart LR
    rc["Productization RC"]
    gate["Unified platform gate"]
    ten["10.x milestone"]
    rc --> gate --> ten
"""


def r_9_10() -> str:
    return """
flowchart LR
    nine["9.x era"]
    buffer["Minor 9.10 buffer"]
    ten["10.x unification prep"]
    nine --> buffer --> ten
"""


def r_10_0() -> str:
    return """
flowchart TB
    dash["Dashboard"]
    ext["Extension"]
    docsai["DocsAI"]
    gw["Appointment360"]
    entity["Canonical entities"]
    dash --> gw
    ext --> gw
    docsai --> gw
    gw --> entity
"""


def r_10_1() -> str:
    return """
flowchart LR
    contracts["Unified contracts"]
    dash["Dashboard"]
    ext["Extension"]
    contracts --> dash
    contracts --> ext
"""


def r_10_2() -> str:
    return """
flowchart TB
    identity["Identity"]
    policy["Policy engine"]
    decision["Single decision"]
    identity --> policy --> decision
"""


def r_10_3() -> str:
    return """
flowchart LR
    wfA["Workflow A"]
    wfB["Workflow B"]
    sem["Shared semantics"]
    wfA --> sem
    wfB --> sem
"""


def r_10_4() -> str:
    return """
flowchart LR
    lineage["Entity lineage"]
    model["Canonical model"]
    completeness["Coverage checks"]
    lineage --> model --> completeness
"""


def r_10_5() -> str:
    return """
flowchart LR
    uxA["Dashboard UX"]
    uxB["Extension UX"]
    tokens["Design tokens"]
    uxA --> tokens
    uxB --> tokens
"""


def r_10_6() -> str:
    return """
flowchart LR
    deploy["Deploy pipeline"]
    rollback["Rollback"]
    recover["Recovery"]
    deploy --> rollback --> recover
"""


def r_10_7() -> str:
    return """
flowchart TB
    controls["Security controls"]
    audit["Audit readiness"]
    compliance["Compliance signoff"]
    controls --> audit --> compliance
"""


def r_10_8() -> str:
    return """
flowchart LR
    latency["Latency"]
    unit["Unit economics"]
    joint["Joint optimization"]
    latency --> joint
    unit --> joint
"""


def r_10_9() -> str:
    return """
flowchart LR
    freeze["Contract freeze"]
    gov["Governance baseline"]
    longterm["Long-term process"]
    freeze --> gov --> longterm
"""


def r_10_10() -> str:
    return """
flowchart LR
    ten["10.x era"]
    buffer["Minor 10.10 buffer"]
    beyond["Post-10.x planning"]
    ten --> buffer --> beyond
"""


RUNTIME_FUNCS: dict[tuple[int, int], Callable[[], str]] = {
    (0, 0): r_0_0,
    (0, 1): r_0_1,
    (0, 2): r_0_2,
    (0, 3): r_0_3,
    (0, 4): r_0_4,
    (0, 5): r_0_5,
    (0, 6): r_0_6,
    (0, 7): r_0_7,
    (0, 8): r_0_8,
    (0, 9): r_0_9,
    (0, 10): r_0_10,
    (1, 0): r_1_0,
    (1, 1): r_1_1,
    (1, 2): r_1_2,
    (1, 3): r_1_3,
    (1, 4): r_1_4,
    (1, 5): r_1_5,
    (1, 6): r_1_6,
    (1, 7): r_1_7,
    (1, 8): r_1_8,
    (1, 9): r_1_9,
    (1, 10): r_1_10,
    (2, 0): r_2_0,
    (2, 1): r_2_1,
    (2, 2): r_2_2,
    (2, 3): r_2_3,
    (2, 4): r_2_4,
    (2, 5): r_2_5,
    (2, 6): r_2_6,
    (2, 7): r_2_7,
    (2, 8): r_2_8,
    (2, 9): r_2_9,
    (2, 10): r_2_10,
    (3, 0): r_3_0,
    (3, 1): r_3_1,
    (3, 2): r_3_2,
    (3, 3): r_3_3,
    (3, 4): r_3_4,
    (3, 5): r_3_5,
    (3, 6): r_3_6,
    (3, 7): r_3_7,
    (3, 8): r_3_8,
    (3, 9): r_3_9,
    (3, 10): r_3_10,
    (4, 0): r_4_0,
    (4, 1): r_4_1,
    (4, 2): r_4_2,
    (4, 3): r_4_3,
    (4, 4): r_4_4,
    (4, 5): r_4_5,
    (4, 6): r_4_6,
    (4, 7): r_4_7,
    (4, 8): r_4_8,
    (4, 9): r_4_9,
    (4, 10): r_4_10,
    (5, 0): r_5_0,
    (5, 1): r_5_1,
    (5, 2): r_5_2,
    (5, 3): r_5_3,
    (5, 4): r_5_4,
    (5, 5): r_5_5,
    (5, 6): r_5_6,
    (5, 7): r_5_7,
    (5, 8): r_5_8,
    (5, 9): r_5_9,
    (5, 10): r_5_10,
    (6, 0): r_6_0,
    (6, 1): r_6_1,
    (6, 2): r_6_2,
    (6, 3): r_6_3,
    (6, 4): r_6_4,
    (6, 5): r_6_5,
    (6, 6): r_6_6,
    (6, 7): r_6_7,
    (6, 8): r_6_8,
    (6, 9): r_6_9,
    (6, 10): r_6_10,
    (7, 0): r_7_0,
    (7, 1): r_7_1,
    (7, 2): r_7_2,
    (7, 3): r_7_3,
    (7, 4): r_7_4,
    (7, 5): r_7_5,
    (7, 6): r_7_6,
    (7, 7): r_7_7,
    (7, 8): r_7_8,
    (7, 9): r_7_9,
    (7, 10): r_7_10,
    (8, 0): r_8_0,
    (8, 1): r_8_1,
    (8, 2): r_8_2,
    (8, 3): r_8_3,
    (8, 4): r_8_4,
    (8, 5): r_8_5,
    (8, 6): r_8_6,
    (8, 7): r_8_7,
    (8, 8): r_8_8,
    (8, 9): r_8_9,
    (8, 10): r_8_10,
    (9, 0): r_9_0,
    (9, 1): r_9_1,
    (9, 2): r_9_2,
    (9, 3): r_9_3,
    (9, 4): r_9_4,
    (9, 5): r_9_5,
    (9, 6): r_9_6,
    (9, 7): r_9_7,
    (9, 8): r_9_8,
    (9, 9): r_9_9,
    (9, 10): r_9_10,
    (10, 0): r_10_0,
    (10, 1): r_10_1,
    (10, 2): r_10_2,
    (10, 3): r_10_3,
    (10, 4): r_10_4,
    (10, 5): r_10_5,
    (10, 6): r_10_6,
    (10, 7): r_10_7,
    (10, 8): r_10_8,
    (10, 9): r_10_9,
    (10, 10): r_10_10,
}


# Stage labels from docs/versions.md release entries (semver X.Y.0)
STAGE_LABEL_RICH: dict[tuple[int, int], str] = {
    (0, 1): "0.1.0 — Initial monorepo and service skeletons",
    (1, 0): "1.0.0 — MVP signup through finder, verifier, and results",
    (1, 1): "1.1.0 — Bulk CSV jobs and billing readiness (stages 1.8, 1.10)",
    (1, 2): "1.2.0 — Analytics, notifications, admin controls, security baseline",
    (2, 0): "2.0.0 — Connectra intelligence (VQL, enrichment, dedup, search UX)",
    (3, 0): "3.0.0 — Extension and Sales Navigator maturity",
    (4, 0): "4.0.0 — contact.ai workflows and governance",
    (5, 0): "5.0.0 — Reliability and scale era (idempotency, queues, observability)",
    (5, 1): "5.1.0 — SLOs, error budgets, reliability reporting",
    (5, 2): "5.2.0 — Idempotent writes and reconciliation",
    (5, 3): "5.3.0 — Queue resilience, DLQ, replay",
    (5, 4): "5.4.0 — Traces, correlated logs, alerts",
    (5, 5): "5.5.0 — API, search, and bulk performance tuning",
    (5, 6): "5.6.0 — S3 integrity and lifecycle",
    (5, 7): "5.7.0 — Cost budgets and throttling",
    (5, 8): "5.8.0 — Abuse detection and advanced rate limits",
    (5, 9): "5.9.0 — Reliability RC before enterprise era",
    (6, 0): "6.0.0 — Enterprise readiness (RBAC, audit, policy)",
    (6, 1): "6.1.0 — RBAC model and permission matrix",
    (6, 2): "6.2.0 — Service-level authorization standardization",
    (6, 3): "6.3.0 — Admin governance and approvals",
    (6, 4): "6.4.0 — Immutable audit event model",
    (6, 5): "6.5.0 — Data classification and retention",
    (6, 6): "6.6.0 — Tenant and policy isolation",
    (6, 7): "6.7.0 — Secrets rotation and privileged controls",
    (6, 8): "6.8.0 — Tenant governance reporting",
    (6, 9): "6.9.0 — Enterprise RC before analytics era",
    (7, 0): "7.0.0 — Analytics platform growth",
    (7, 1): "7.1.0 — Unified analytics taxonomy",
    (7, 2): "7.2.0 — Instrumentation across surfaces",
    (7, 3): "7.3.0 — Analytics ingestion hardening",
    (7, 4): "7.4.0 — Quality and lineage controls",
    (7, 5): "7.5.0 — User analytics experience v1",
    (7, 6): "7.6.0 — DocsAI analytics center v1",
    (7, 7): "7.7.0 — Scheduled reports and exports",
    (7, 8): "7.8.0 — Analytics performance and cost optimization",
    (7, 9): "7.9.0 — Analytics RC before integrations era",
    (8, 0): "8.0.0 — Integration ecosystem expansion",
    (8, 1): "8.1.0 — External contract governance",
    (8, 2): "8.2.0 — Partner identity and scoped access",
    (8, 3): "8.3.0 — Public API minimum surface",
    (8, 4): "8.4.0 — Webhook delivery platform v1",
    (8, 5): "8.5.0 — Replay and reconciliation APIs",
    (8, 6): "8.6.0 — Connector framework and SDK lifecycle",
    (8, 7): "8.7.0 — Integration health and support tooling",
    (8, 8): "8.8.0 — Integration quotas and entitlements",
    (8, 9): "8.9.0 — Integration RC before productization era",
    (9, 0): "9.0.0 — Platform productization and multi-tenant ops",
    (9, 1): "9.1.0 — Canonical tenant model propagation",
    (9, 2): "9.2.0 — Self-serve workspace administration",
    (9, 3): "9.3.0 — Entitlement and packaging engine",
    (9, 4): "9.4.0 — SLA and SLO operations",
    (9, 5): "9.5.0 — Support and incident operations",
    (9, 6): "9.6.0 — Data residency and policy overlays",
    (9, 7): "9.7.0 — Cost governance and forecasting",
    (9, 8): "9.8.0 — Tenant migration automation",
    (9, 9): "9.9.0 — Productization RC before unified platform",
    (10, 0): "10.0.0 — Unified Contact360 platform milestone",
    (10, 1): "10.1.0 — Cross-surface contract unification",
    (10, 2): "10.2.0 — Unified identity and policy engine",
    (10, 3): "10.3.0 — Workflow orchestration standardization",
    (10, 4): "10.4.0 — Canonical entity model and lineage",
    (10, 5): "10.5.0 — Cross-surface UX consistency",
    (10, 6): "10.6.0 — Release and recovery automation",
    (10, 7): "10.7.0 — Security and compliance hardening",
    (10, 8): "10.8.0 — Performance and unit economics convergence",
    (10, 9): "10.9.0 — Contract freeze and governance baseline",
}


# Placeholder delivery labels — unique slice per minor
STAGE_LABEL_PLACEHOLDER: dict[tuple[int, int], str] = {
    (0, 0): "0.0.x placeholder — pre-monorepo baseline (no shipped scope)",
    (0, 2): "0.2.x placeholder — DB schema and Alembic separation focus",
    (0, 3): "0.3.x placeholder — service-to-service contracts focus",
    (0, 4): "0.4.x placeholder — auth primitives and RBAC freeze focus",
    (0, 5): "0.5.x placeholder — S3 and upload module focus",
    (0, 6): "0.6.x placeholder — async job and Kafka topology focus",
    (0, 7): "0.7.x placeholder — Connectra and Elasticsearch baseline focus",
    (0, 8): "0.8.x placeholder — dashboard scaffolding and DocsAI sync focus",
    (0, 9): "0.9.x placeholder — extension and Sales Navigator skeleton focus",
    (0, 10): "0.10.x placeholder — CI/CD and health-check hardening focus",
    (1, 3): "1.3.x placeholder — reserved stage number (historical gap)",
    (1, 4): "1.4.x placeholder — finder engine slice (pre-ship)",
    (1, 5): "1.5.x placeholder — verifier engine slice (pre-ship)",
    (1, 6): "1.6.x placeholder — results experience slice (pre-ship)",
    (1, 7): "1.7.x placeholder — credits and usage edge cases (pre-ship)",
    (1, 8): "1.8.x placeholder — bulk validation MVP slice (pre-ship)",
    (1, 9): "1.9.x placeholder — profile and account polish (pre-ship)",
    (1, 10): "1.10.x placeholder — billing and packs slice (pre-ship)",
    (2, 1): "2.1.x placeholder — VQL compiler and query planning slice",
    (2, 2): "2.2.x placeholder — saved searches and persistence slice",
    (2, 3): "2.3.x placeholder — rate limits and Connectra health slice",
    (2, 4): "2.4.x placeholder — deduplication and merge policy slice",
    (2, 5): "2.5.x placeholder — search latency and caching slice",
    (2, 6): "2.6.x placeholder — contacts UI and facet filters slice",
    (2, 7): "2.7.x placeholder — enrichment pipeline slice",
    (2, 8): "2.8.x placeholder — company and contact graph slice",
    (2, 9): "2.9.x placeholder — per-tenant quotas slice",
    (2, 10): "2.10.x placeholder — Connectra era buffer before 3.x",
    (3, 1): "3.1.x placeholder — extension session handshake slice",
    (3, 2): "3.2.x placeholder — SN scrape and save path slice",
    (3, 3): "3.3.x placeholder — profile URL dedup slice",
    (3, 4): "3.4.x placeholder — token refresh slice",
    (3, 5): "3.5.x placeholder — extension telemetry slice",
    (3, 6): "3.6.x placeholder — merge conflicts slice",
    (3, 7): "3.7.x placeholder — LinkedIn module wiring slice",
    (3, 8): "3.8.x placeholder — extension packaging slice",
    (3, 9): "3.9.x placeholder — ingest idempotency slice",
    (3, 10): "3.10.x placeholder — SN E2E integrity slice",
    (4, 1): "4.1.x placeholder — AI chats REST and streaming slice",
    (4, 2): "4.2.x placeholder — prompt safety and policy slice",
    (4, 3): "4.3.x placeholder — model fallback routing slice",
    (4, 4): "4.4.x placeholder — confidence and explainability slice",
    (4, 5): "4.5.x placeholder — prompt audit and review slice",
    (4, 6): "4.6.x placeholder — tool-use and gateway integration slice",
    (4, 7): "4.7.x placeholder — token budgets slice",
    (4, 8): "4.8.x placeholder — conversation history storage slice",
    (4, 9): "4.9.x placeholder — offline eval and promotion gate slice",
    (4, 10): "4.10.x placeholder — AI era buffer before 5.x",
    (5, 10): "5.10.x placeholder — reliability era buffer before 6.x",
    (6, 10): "6.10.x placeholder — enterprise era buffer before 7.x",
    (7, 10): "7.10.x placeholder — analytics era buffer before 8.x",
    (8, 10): "8.10.x placeholder — integrations era buffer before 9.x",
    (9, 10): "9.10.x placeholder — productization era buffer before 10.x",
    (10, 10): "10.10.x placeholder — post-10.0 planning buffer",
}


def _placeholder_label(major: int, minor: int) -> str:
    if (major, minor) in STAGE_LABEL_PLACEHOLDER:
        return STAGE_LABEL_PLACEHOLDER[(major, minor)]
    return f"{major}.{minor}.x placeholder — roadmap slice pending approval"


def stage_label_for(major: int, minor: int) -> str:
    key = (major, minor)
    if key in STAGE_LABEL_RICH:
        return STAGE_LABEL_RICH[key]
    return _placeholder_label(major, minor)


def runtime_body_for(major: int, minor: int) -> str:
    return RUNTIME_FUNCS[(major, minor)]()


def build_flowchart_section(major: int, minor: int, _file_text: str = "") -> str:
    key = (major, minor)
    if key in STAGE_LABEL_RICH:
        label = STAGE_LABEL_RICH[key]
    else:
        label = _placeholder_label(major, minor)
    label = _td(label[:220])
    body = runtime_body_for(major, minor)
    return delivery_section(label, body)


FLOWCHART_BLOCK_PATTERN = re.compile(
    r"## Flowchart\n.*?^See also: \[`docs/flowchart\.md`\]\(\.\./flowchart\.md\) for system-wide and master views\.\n",
    re.MULTILINE | re.DOTALL,
)
