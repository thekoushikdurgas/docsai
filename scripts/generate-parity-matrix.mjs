#!/usr/bin/env node
/**
 * Generates admin parity matrix: Django DocsAI (contact360.io/1) vs Next admin routes.
 * Run from repo root: node contact360.io/admin/scripts/generate-parity-matrix.mjs
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "../../..");
const DJANGO_ROOT = path.join(REPO_ROOT, "contact360.io/1");
const ADMIN_ROOT = path.join(REPO_ROOT, "contact360.io/admin");
const OUT_JSON = path.join(REPO_ROOT, "docs/frontend/pages/admin-parity-matrix.json");
const OUT_MD = path.join(REPO_ROOT, "docs/frontend/pages/admin-parity-matrix.md");

/** Mount prefixes from docsai/urls.py includes */
const ROOT_MOUNTS = {
  "apps.core.urls": "",
  "apps.core.legal_urls": "legal/",
  "apps.documentation.urls": "docs/",
  "apps.analytics.urls": "analytics/",
  "apps.ai_agent.urls": "ai/",
  "apps.codebase.urls": "codebase/",
  "apps.graph.urls": "graph/",
  "apps.roadmap.urls": "roadmap/",
  "apps.architecture.urls": "architecture/",
  "apps.templates_app.urls": "templates/",
  "apps.json_store.urls": "json-store/",
  "apps.operations.urls": "operations/",
  "apps.page_builder.urls": "page-builder/",
  "apps.knowledge.urls": "knowledge/",
  "apps.admin_ops.admin_urls": "admin/",
  "apps.durgasflow.urls": "durgasflow/",
  "apps.durgasman.urls": "durgasman/",
  "apps.documentation.api.v1.urls": "api/v1/",
};

const NEXT_ROUTE_MAP = {
  "/": { status: "implemented", next: "/" },
  "/login/": { status: "implemented", next: "/login" },
  "/logout/": { status: "implemented", next: "/settings" },
  "/legal/terms/": { status: "partial", next: "/legal/terms", note: "Phase 2" },
  "/legal/privacy/": { status: "partial", next: "/legal/privacy", note: "Phase 2" },
  "/legal/refund/": { status: "partial", next: "/legal/refund", note: "Phase 2" },
  "/admin/": { status: "implemented", next: "/users" },
  "/admin/users/": { status: "implemented", next: "/users" },
  "/admin/users/<id>/": { status: "implemented", next: "/users/[id]", note: "" },
  "/admin/users/<id>/history/": {
    status: "implemented",
    next: "/users/[id]",
    note: "history via ?tab=history",
  },
  "/admin/jobs/": { status: "implemented", next: "/jobs" },
  "/admin/jobs/<id>/": { status: "partial", next: "/jobs/[id]", note: "Phase 1" },
  "/admin/jobs/<id>/retry/": { status: "partial", next: "/jobs/[id]", note: "Phase 1" },
  "/admin/job-tickets/": { status: "implemented", next: "/jobs/tickets" },
  "/admin/job-tickets/<id>/": { status: "partial", next: "/jobs/tickets/[id]", note: "Phase 1" },
  "/admin/logs/": { status: "implemented", next: "/logs" },
  "/admin/billing/payments/": { status: "implemented", next: "/billing" },
  "/admin/billing/plans/": { status: "partial", next: "/billing/plans", note: "CRUD Phase 1" },
  "/admin/billing/addons/": { status: "partial", next: "/billing/addons", note: "Phase 1" },
  "/admin/billing/settings/": { status: "partial", next: "/billing/settings", note: "Phase 1" },
  "/admin/storage/": { status: "implemented", next: "/storage" },
  "/admin/system-status/": { status: "implemented", next: "/health" },
  "/admin/statistics/": { status: "implemented", next: "/analytics" },
  "/admin/settings/": { status: "implemented", next: "/settings" },
  "/admin/ops/contacts-explorer/": { status: "partial", next: "/ops/contacts", note: "Phase 1" },
  "/admin/ops/campaign-cql/": { status: "partial", next: "/ops/campaign-cql", note: "Phase 1" },
  "/admin/ops/email-jobs/": { status: "partial", next: "/ops/email-jobs", note: "Phase 1" },
  "/admin/ops/phone-jobs/": { status: "partial", next: "/ops/phone-jobs", note: "Phase 1" },
  "/admin/ops/connectra-jobs/": { status: "partial", next: "/ops/connectra-jobs", note: "Phase 1" },
  "/admin/ops/durgasflow-audit/": { status: "partial", next: "/ops/durgasflow-audit", note: "Phase 1" },
  "/admin/ops/leads/": { status: "proxy", next: "/ops/leads", note: "placeholder" },
  "/analytics/": { status: "implemented", next: "/analytics" },
  "/ai/chat/": { status: "partial", next: "/ai/chat", note: "Phase 2" },
  "/ai/sessions/": { status: "partial", next: "/ai/sessions", note: "Phase 2" },
  "/knowledge/": { status: "partial", next: "/knowledge", note: "CRUD Phase 2" },
  "/docs/": { status: "proxy", next: "/docs", note: "BFF Phase 4" },
  "/api/v1/": { status: "proxy", next: "/api/docsai/v1", note: "BFF Phase 4" },
  "/durgasflow/": { status: "proxy", next: "/durgasflow", note: "Phase 5" },
  "/durgasman/": { status: "proxy", next: "/durgasman", note: "Phase 5" },
  "/page-builder/": { status: "proxy", next: "/page-builder", note: "Phase 5" },
  "/json-store/": { status: "proxy", next: "/json-store", note: "Phase 5" },
  "/codebase/": { status: "proxy", next: "/codebase", note: "Phase 5" },
  "/graph/": { status: "proxy", next: "/graph", note: "Phase 5" },
  "/roadmap/": { status: "proxy", next: "/roadmap", note: "Phase 5" },
  "/architecture/": { status: "proxy", next: "/architecture", note: "Phase 5" },
  "/templates/": { status: "proxy", next: "/templates", note: "Phase 5" },
  "/operations/": { status: "proxy", next: "/operations", note: "Phase 5" },
};

function walkUrls(dir, base = "") {
  const results = [];
  if (!fs.existsSync(dir)) return results;
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, ent.name);
    if (ent.isDirectory()) {
      results.push(...walkUrls(full, base));
      continue;
    }
    if (!ent.name.endsWith("urls.py") && !ent.name.endsWith("legal_urls.py")) continue;
    const rel = path.relative(DJANGO_ROOT, full).replace(/\\/g, "/");
    const content = fs.readFileSync(full, "utf8");
    const appMatch = rel.match(/^apps\/([^/]+)/);
    const app = appMatch ? appMatch[1] : "docsai";
    const includeKey = rel.includes("legal_urls")
      ? "apps.core.legal_urls"
      : rel === "docsai/urls.py"
        ? null
        : `apps.${app}.${ent.name === "urls.py" && rel.includes("/api/") ? path.dirname(rel).split("/").slice(-2).join(".") : app}.urls`;

    let prefix = "";
    if (rel === "docsai/urls.py") {
      prefix = "";
    } else if (rel.includes("documentation/api/v1/pages_urls")) {
      prefix = "api/v1/pages/";
    } else if (rel.includes("documentation/api/v1/endpoints_urls")) {
      prefix = "api/v1/endpoints/";
    } else if (rel.includes("documentation/api/v1/relationships_urls")) {
      prefix = "api/v1/relationships/";
    } else if (rel.includes("documentation/api/v1/postman_urls")) {
      prefix = "api/v1/postman/";
    } else if (rel.includes("documentation/api/v1/")) {
      prefix = "api/v1/";
    } else {
      for (const [key, p] of Object.entries(ROOT_MOUNTS)) {
        if (rel.includes(key.replace(/\./g, "/").replace("apps/", "apps/"))) {
          prefix = p;
          break;
        }
        if (rel === `apps/${app}/urls.py` && ROOT_MOUNTS[`apps.${app}.urls`]) {
          prefix = ROOT_MOUNTS[`apps.${app}.urls`];
        }
      }
      if (rel === "apps/core/legal_urls.py") prefix = "legal/";
      if (rel === "apps/admin_ops/urls.py") prefix = "admin/";
      if (rel === "apps/documentation/urls.py") prefix = "docs/";
    }

    const pathRegex = /path\s*\(\s*["']([^"']*)["']/g;
    let m;
    while ((m = pathRegex.exec(content)) !== null) {
      const pattern = m[1];
      if (pattern.includes("include(")) continue;
      const fullPath = "/" + prefix + pattern;
      const normalized = fullPath.replace(/\/+/g, "/").replace(/\/$/, "") || "/";
      results.push({
        app,
        file: rel,
        pattern,
        path: normalized + (pattern.endsWith("/") || !pattern ? "/" : ""),
        prefix,
      });
    }
  }
  return results;
}

function listNextPages(dir, base = "") {
  const routes = [];
  if (!fs.existsSync(dir)) return routes;
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const rel = path.join(base, ent.name);
    if (ent.isDirectory()) {
      routes.push(...listNextPages(path.join(dir, ent.name), rel));
    } else if (ent.name === "page.tsx") {
      const route =
        "/" +
        rel
          .replace(/\\/g, "/")
          .replace(/\/page\.tsx$/, "")
          .replace(/^\//, "");
      routes.push(route === "/" ? "/" : route);
    }
  }
  return routes;
}

function inferStatus(djangoPath) {
  const norm = djangoPath.replace(/<[^>]+>/g, "<id>").replace(/\/+/g, "/");
  const entries = Object.entries(NEXT_ROUTE_MAP).sort(
    (a, b) => b[0].length - a[0].length,
  );
  for (const [key, val] of entries) {
    const k = key.replace(/<[^>]+>/g, "<id>");
    const prefix = k.replace(/\/$/, "");
    if (!prefix) continue;
    if (norm === k || norm.startsWith(`${prefix}/`) || norm === prefix) {
      return val;
    }
  }
  if (djangoPath.startsWith("/docs/") || djangoPath.startsWith("/api/v1/")) {
    return { status: "proxy", next: "/docs or /api/docsai", note: "Phase 4" };
  }
  if (
    djangoPath.startsWith("/durgasflow/") ||
    djangoPath.startsWith("/durgasman/") ||
    djangoPath.startsWith("/page-builder/") ||
    djangoPath.startsWith("/json-store/") ||
    djangoPath.startsWith("/codebase/")
  ) {
    return { status: "proxy", next: djangoPath.slice(0, -1) || djangoPath, note: "Phase 5" };
  }
  if (djangoPath.startsWith("/admin/")) {
    return { status: "partial", next: "TBD", note: "Phase 1 admin_ops" };
  }
  return { status: "missing", next: null, note: "TBD" };
}

const djangoRoutes = walkUrls(DJANGO_ROOT);
const nextRoutes = listNextPages(path.join(ADMIN_ROOT, "app"));

const matrix = djangoRoutes.map((r) => {
  const inf = inferStatus(r.path);
  return {
    django_path: r.path,
    django_app: r.app,
    django_file: r.file,
    parity_status: inf.status,
    next_route: inf.next,
    notes: inf.note || "",
  };
});

const summary = matrix.reduce((acc, row) => {
  acc[row.parity_status] = (acc[row.parity_status] || 0) + 1;
  return acc;
}, {});

const output = {
  generated_at: new Date().toISOString(),
  django_root: "contact360.io/1",
  next_root: "contact360.io/admin",
  counts: {
    django_url_patterns: djangoRoutes.length,
    next_pages: nextRoutes.length,
    ...summary,
  },
  next_routes: nextRoutes.sort(),
  matrix,
};

fs.mkdirSync(path.dirname(OUT_JSON), { recursive: true });
fs.writeFileSync(OUT_JSON, JSON.stringify(output, null, 2));

let md = `# Admin parity matrix (generated)\n\n`;
md += `Generated: ${output.generated_at}\n\n`;
md += `| Metric | Count |\n|--------|-------|\n`;
md += `| Django \`path()\` patterns | ${djangoRoutes.length} |\n`;
md += `| Next.js pages | ${nextRoutes.length} |\n`;
for (const [k, v] of Object.entries(summary)) {
  md += `| Status: ${k} | ${v} |\n`;
}
md += `\nSee [admin-parity-matrix.json](./admin-parity-matrix.json) for full data.\n`;
md += `\nRegenerate: \`node contact360.io/admin/scripts/generate-parity-matrix.mjs\`\n`;
fs.writeFileSync(OUT_MD, md);

console.log("Wrote", OUT_JSON);
console.log("Wrote", OUT_MD);
console.log("Summary:", summary);
