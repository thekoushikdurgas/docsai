/** Helpers for Postman Collection v2.1 JSON (Durgasman runner). */

export type PostmanTreeNode = {
  id: string;
  name: string;
  type: "folder" | "request";
  depth: number;
  request?: PostmanRequestDraft;
  children?: PostmanTreeNode[];
};

export type PostmanRequestDraft = {
  name: string;
  method: string;
  url: string;
  headers: Record<string, string>;
  body: string;
  bodyType: "none" | "raw" | "form";
  queryParams: Record<string, string>;
};

type PostmanItem = {
  name?: string;
  item?: PostmanItem[];
  request?: {
    method?: string;
    url?: string | { raw?: string };
    header?: Array<{ key?: string; value?: string; disabled?: boolean }>;
    body?: {
      mode?: string;
      raw?: string;
      urlencoded?: Array<{ key?: string; value?: string; disabled?: boolean }>;
    };
  };
};

function resolveUrlField(
  url: string | { raw?: string } | undefined,
): string {
  if (typeof url === "string") return url;
  if (url && typeof url === "object" && url.raw) return url.raw;
  return "";
}

export function itemToDraft(item: PostmanItem): PostmanRequestDraft {
  const req = item.request ?? {};
  const headers: Record<string, string> = {};
  for (const h of req.header ?? []) {
    if (h.disabled) continue;
    if (h.key) headers[h.key] = h.value ?? "";
  }
  let body = "";
  let bodyType: PostmanRequestDraft["bodyType"] = "none";
  const mode = req.body?.mode;
  if (mode === "raw" && req.body?.raw) {
    body = req.body.raw;
    bodyType = "raw";
  } else if (mode === "urlencoded" && req.body?.urlencoded?.length) {
    bodyType = "form";
  }
  return {
    name: item.name ?? "Request",
    method: (req.method ?? "GET").toUpperCase(),
    url: resolveUrlField(req.url),
    headers,
    body,
    bodyType,
    queryParams: {},
  };
}

export function buildRequestTree(items: PostmanItem[], depth = 0, prefix = ""): PostmanTreeNode[] {
  const out: PostmanTreeNode[] = [];
  items.forEach((item, idx) => {
    const id = `${prefix}${idx}`;
    if (item.request) {
      out.push({
        id,
        name: item.name ?? "Request",
        type: "request",
        depth,
        request: itemToDraft(item),
      });
    } else if (item.item?.length) {
      out.push({
        id,
        name: item.name ?? "Folder",
        type: "folder",
        depth,
        children: buildRequestTree(item.item, depth + 1, `${id}-`),
      });
    }
  });
  return out;
}

export function flattenRequestNodes(nodes: PostmanTreeNode[]): PostmanTreeNode[] {
  const flat: PostmanTreeNode[] = [];
  for (const n of nodes) {
    if (n.type === "request") flat.push(n);
    if (n.children) flat.push(...flattenRequestNodes(n.children));
  }
  return flat;
}

export function substituteVariables(
  text: string,
  variables: Record<string, string>,
): string {
  return text.replace(/\{\{([^}]+)\}\}/g, (_, key: string) => {
    const k = key.trim();
    return variables[k] ?? `{{${k}}}`;
  });
}

export function environmentVariables(
  env: { values?: Array<{ key?: string; value?: string; enabled?: boolean }> } | null,
): Record<string, string> {
  const out: Record<string, string> = {};
  for (const v of env?.values ?? []) {
    if (v.enabled === false || !v.key) continue;
    out[v.key] = v.value ?? "";
  }
  return out;
}
