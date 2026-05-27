"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { DurgasmanSubNav } from "@/components/feature/durgasman/DurgasmanSubNav";
import Button from "@/components/ui/Button";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import {
  buildRequestTree,
  environmentVariables,
  substituteVariables,
  type PostmanRequestDraft,
  type PostmanTreeNode,
} from "@/lib/durgasmanPostman";
import {
  durgasmanService,
  type DurgasmanCollectionRow,
  type DurgasmanEnvironmentRow,
  type SendRequestResult,
} from "@/services/durgasmanService";

const METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"];

export function DurgasmanRunnerClient() {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const [collections, setCollections] = useState<DurgasmanCollectionRow[]>([]);
  const [environments, setEnvironments] = useState<DurgasmanEnvironmentRow[]>([]);
  const [selectedColId, setSelectedColId] = useState<number | "">("");
  const [selectedEnvId, setSelectedEnvId] = useState<number | "">("");
  const [tree, setTree] = useState<PostmanTreeNode[]>([]);
  const [search, setSearch] = useState("");
  const [draft, setDraft] = useState<PostmanRequestDraft>(emptyDraft());
  const [headersText, setHeadersText] = useState("{}");
  const [sending, setSending] = useState(false);
  const [response, setResponse] = useState<SendRequestResult | null>(null);
  const [envVars, setEnvVars] = useState<Record<string, string>>({});

  const loadLists = useCallback(async () => {
    try {
      const [cols, envs] = await Promise.all([
        durgasmanService.collections(),
        durgasmanService.environments(),
      ]);
      setCollections(cols.collections);
      setEnvironments(envs.environments);
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to load lists");
    }
  }, []);

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
      return;
    }
    void loadLists();
  }, [isSuperAdmin, loadLists, router]);

  const loadCollection = async (colId: number) => {
    setSelectedColId(colId);
    setTree([]);
    try {
      const res = await durgasmanService.collectionJson(colId);
      const items = (res.collection?.item ?? []) as Parameters<
        typeof buildRequestTree
      >[0];
      setTree(buildRequestTree(items));
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to load collection");
    }
  };

  const loadEnvironment = async (envId: number | "") => {
    setSelectedEnvId(envId);
    if (!envId) {
      setEnvVars({});
      return;
    }
    try {
      const res = await durgasmanService.environmentJson(envId);
      setEnvVars(environmentVariables(res.environment));
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to load environment");
    }
  };

  const selectRequest = (node: PostmanTreeNode) => {
    if (!node.request) return;
    setDraft(node.request);
    setHeadersText(JSON.stringify(node.request.headers, null, 2));
    setResponse(null);
  };

  const send = async () => {
    setSending(true);
    setResponse(null);
    try {
      let headers: Record<string, string> = {};
      try {
        headers = JSON.parse(headersText) as Record<string, string>;
      } catch {
        toast.error("Headers must be valid JSON");
        setSending(false);
        return;
      }
      const variables = envVars;
      const result = await durgasmanService.send({
        method: draft.method,
        url: substituteVariables(draft.url, variables),
        headers: Object.fromEntries(
          Object.entries(headers).map(([k, v]) => [
            k,
            substituteVariables(String(v), variables),
          ]),
        ),
        body:
          draft.bodyType === "raw"
            ? substituteVariables(draft.body, variables)
            : "",
        body_type: draft.bodyType === "raw" ? "raw" : "none",
        variables,
        timeout: 60,
      });
      setResponse(result);
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Send failed");
    } finally {
      setSending(false);
    }
  };

  const filteredTree = useMemo(() => {
    const q = search.trim().toLowerCase();
    if (!q) return tree;
    return filterTree(tree, q);
  }, [tree, search]);

  if (!isSuperAdmin) return null;

  return (
    <AdminPageLayout
      title="API runner"
      subtitle="Browse collections, send requests, inspect responses"
      actions={
        <Link href={ADMIN_ROUTES.DURGASMAN_UPLOAD}>
          <Button size="sm" variant="outline">
            Upload
          </Button>
        </Link>
      }
      tabs={<DurgasmanSubNav />}
    >
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "minmax(220px, 280px) 1fr minmax(240px, 1fr)",
          gap: 12,
          minHeight: "calc(100vh - 260px)",
          alignItems: "stretch",
        }}
      >
        <aside className="c360-card" style={{ padding: 12, overflow: "auto" }}>
          <label className="c360-text-muted" style={{ fontSize: "0.75rem" }}>
            Environment
          </label>
          <select
            className="c360-input"
            style={{ width: "100%", marginBottom: 12 }}
            value={selectedEnvId}
            onChange={(e) => {
              const v = e.target.value;
              void loadEnvironment(v ? parseInt(v, 10) : "");
            }}
          >
            <option value="">No environment</option>
            {environments.map((env) => (
              <option key={env.id} value={env.id}>
                {env.name} ({env.variable_count})
              </option>
            ))}
          </select>

          <label className="c360-text-muted" style={{ fontSize: "0.75rem" }}>
            Collection
          </label>
          <select
            className="c360-input"
            style={{ width: "100%", marginBottom: 12 }}
            value={selectedColId}
            onChange={(e) => {
              const v = parseInt(e.target.value, 10);
              if (v) void loadCollection(v);
            }}
          >
            <option value="">Select collection…</option>
            {collections.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name} ({c.request_count})
              </option>
            ))}
          </select>

          <input
            className="c360-input"
            placeholder="Search requests…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ width: "100%", marginBottom: 8 }}
          />

          <TreeList nodes={filteredTree} onSelect={selectRequest} />
        </aside>

        <section className="c360-card" style={{ padding: 12, display: "flex", flexDirection: "column" }}>
          <div className="c360-flex c360-flex--gap-2" style={{ marginBottom: 12 }}>
            <select
              className="c360-input"
              value={draft.method}
              onChange={(e) => setDraft((d) => ({ ...d, method: e.target.value }))}
              style={{ width: 110 }}
            >
              {METHODS.map((m) => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))}
            </select>
            <input
              className="c360-input"
              style={{ flex: 1 }}
              value={draft.url}
              onChange={(e) => setDraft((d) => ({ ...d, url: e.target.value }))}
              placeholder="https://api.example.com/..."
            />
            <Button size="sm" disabled={sending} onClick={() => void send()}>
              {sending ? "Sending…" : "Send"}
            </Button>
          </div>

          <label className="c360-text-muted" style={{ fontSize: "0.75rem" }}>
            Headers (JSON)
          </label>
          <textarea
            className="c360-input"
            rows={4}
            value={headersText}
            onChange={(e) => setHeadersText(e.target.value)}
            style={{ width: "100%", fontFamily: "monospace", marginBottom: 12 }}
          />

          <label className="c360-text-muted" style={{ fontSize: "0.75rem" }}>
            Body (raw JSON / text)
          </label>
          <textarea
            className="c360-input"
            rows={10}
            value={draft.body}
            onChange={(e) =>
              setDraft((d) => ({ ...d, body: e.target.value, bodyType: "raw" }))
            }
            style={{ width: "100%", fontFamily: "monospace", flex: 1 }}
          />
        </section>

        <section className="c360-card" style={{ padding: 12, overflow: "auto" }}>
          <ResponsePanel result={response} />
        </section>
      </div>
    </AdminPageLayout>
  );
}

function emptyDraft(): PostmanRequestDraft {
  return {
    name: "Request",
    method: "GET",
    url: "",
    headers: {},
    body: "",
    bodyType: "none",
    queryParams: {},
  };
}

function TreeList({
  nodes,
  onSelect,
  depth = 0,
}: {
  nodes: PostmanTreeNode[];
  onSelect: (n: PostmanTreeNode) => void;
  depth?: number;
}) {
  return (
    <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
      {nodes.map((node) => (
        <li key={node.id}>
          {node.type === "request" ? (
            <button
              type="button"
              onClick={() => onSelect(node)}
              style={{
                display: "block",
                width: "100%",
                textAlign: "left",
                padding: "4px 8px",
                paddingLeft: 8 + depth * 12,
                background: "none",
                border: "none",
                cursor: "pointer",
                fontSize: "0.875rem",
              }}
            >
              {node.name}
            </button>
          ) : (
            <>
              <div
                style={{
                  fontWeight: 600,
                  fontSize: "0.8rem",
                  paddingLeft: 8 + depth * 12,
                  marginTop: 6,
                }}
              >
                {node.name}
              </div>
              {node.children ? (
                <TreeList nodes={node.children} onSelect={onSelect} depth={depth + 1} />
              ) : null}
            </>
          )}
        </li>
      ))}
    </ul>
  );
}

function filterTree(nodes: PostmanTreeNode[], q: string): PostmanTreeNode[] {
  const out: PostmanTreeNode[] = [];
  for (const n of nodes) {
    if (n.type === "request" && n.name.toLowerCase().includes(q)) {
      out.push(n);
    } else if (n.children) {
      const kids = filterTree(n.children, q);
      if (kids.length) out.push({ ...n, children: kids });
    }
  }
  return out;
}

function ResponsePanel({ result }: { result: SendRequestResult | null }) {
  if (!result) {
    return (
      <p className="c360-text-muted" style={{ fontSize: "0.875rem" }}>
        Hit Send to receive a response.
      </p>
    );
  }
  if (result.error) {
    return <p style={{ color: "var(--c360-danger, #b91c1c)" }}>{result.error}</p>;
  }
  return (
    <>
      <div className="c360-flex c360-flex--gap-3" style={{ marginBottom: 12, flexWrap: "wrap" }}>
        <span>
          Status: <strong>{result.status}</strong> {result.status_text}
        </span>
        <span>Time: {result.elapsed_ms} ms</span>
        <span>Size: {result.size_bytes} B</span>
      </div>
      <pre
        style={{
          fontSize: "0.8rem",
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
          margin: 0,
          maxHeight: "calc(100vh - 320px)",
          overflow: "auto",
        }}
      >
        {formatBody(result.body ?? "")}
      </pre>
      {result.body_truncated ? (
        <p className="c360-text-muted" style={{ fontSize: "0.75rem", marginTop: 8 }}>
          Response truncated.
        </p>
      ) : null}
    </>
  );
}

function formatBody(body: string): string {
  try {
    return JSON.stringify(JSON.parse(body), null, 2);
  } catch {
    return body;
  }
}
