/**
 * Server-only S3Storage HTTP client (parity with Django `admin_ops` direct s3storage calls).
 */

export type StorageArtifact = {
  key: string;
  filename: string;
  size: number;
  lastModified: string;
  contentType: string;
};

function apiV1Base(baseUrl: string): string {
  const b = baseUrl.replace(/\/$/, "");
  if (b.endsWith("/api/v1")) return b;
  return `${b}/api/v1`;
}

export function s3ApiRoot(): string {
  const base = process.env.S3STORAGE_API_URL?.trim();
  if (!base) return "";
  return apiV1Base(base);
}

function s3Headers(): Record<string, string> {
  const headers: Record<string, string> = {
    "X-Request-ID": crypto.randomUUID(),
  };
  const apiKey = process.env.S3STORAGE_API_KEY?.trim();
  if (apiKey) headers["X-API-Key"] = apiKey;
  return headers;
}

export function isS3StorageConfigured(): boolean {
  return Boolean(s3ApiRoot());
}

function normalizeArtifact(obj: Record<string, unknown>): StorageArtifact {
  const key = String(obj.key ?? obj.Key ?? "");
  const size = Number(obj.size ?? obj.Size ?? obj.ContentLength ?? 0);
  const lastModified = String(
    obj.last_modified ?? obj.lastModified ?? obj.LastModified ?? "",
  );
  const contentType = String(
    obj.content_type ?? obj.contentType ?? obj.ContentType ?? "",
  );
  const filename =
    String(obj.filename ?? obj.Filename ?? "") || key.split("/").pop() || key;
  return {
    key,
    filename,
    size: Number.isFinite(size) ? size : 0,
    lastModified,
    contentType,
  };
}

export async function listStorageArtifacts(params: {
  prefix: string;
  limit?: number;
  offset?: number;
}): Promise<{ items: StorageArtifact[]; total: number }> {
  const root = s3ApiRoot();
  if (!root) {
    throw new Error("S3Storage is not configured (S3STORAGE_API_URL)");
  }
  const limit = params.limit ?? 50;
  const offset = params.offset ?? 0;
  const url = new URL(`${root}/files`);
  url.searchParams.set("prefix", params.prefix);
  url.searchParams.set("limit", String(limit));
  url.searchParams.set("offset", String(offset));

  const resp = await fetch(url.toString(), {
    headers: s3Headers(),
    cache: "no-store",
  });
  const body = (await resp.json().catch(() => ({}))) as Record<string, unknown>;
  if (!resp.ok) {
    const detail =
      (typeof body.detail === "string" && body.detail) ||
      (typeof body.error === "string" && body.error) ||
      resp.statusText;
    throw new Error(detail || "Failed to list storage");
  }
  const raw = (body.objects ?? body.files ?? []) as unknown[];
  const items = Array.isArray(raw)
    ? raw
        .filter((o): o is Record<string, unknown> => !!o && typeof o === "object")
        .map((o) => normalizeArtifact(o))
    : [];
  const total = Number(body.total ?? items.length);
  return { items, total: Number.isFinite(total) ? total : items.length };
}

export async function getStorageDownloadUrl(key: string): Promise<string | null> {
  const root = s3ApiRoot();
  if (!root || !key.trim()) return null;
  const url = new URL(`${root}/objects/presign-download`);
  url.searchParams.set("key", key.trim());
  const resp = await fetch(url.toString(), {
    headers: s3Headers(),
    cache: "no-store",
  });
  if (!resp.ok) return null;
  const body = (await resp.json().catch(() => ({}))) as Record<string, unknown>;
  const downloadUrl = body.downloadUrl ?? body.download_url ?? body.url;
  return typeof downloadUrl === "string" ? downloadUrl : null;
}

export async function deleteStorageArtifact(key: string): Promise<boolean> {
  const root = s3ApiRoot();
  if (!root || !key.trim()) return false;
  const url = new URL(`${root}/objects`);
  url.searchParams.set("key", key.trim());
  const resp = await fetch(url.toString(), {
    method: "DELETE",
    headers: s3Headers(),
  });
  return resp.status < 300;
}

export async function uploadPhotoToS3Storage(params: {
  bucketId: string;
  file: Blob;
  filename: string;
  contentType: string;
  requestId?: string;
}): Promise<{ fileKey: string; bucketId: string }> {
  const baseUrl = process.env.S3STORAGE_API_URL?.trim();
  if (!baseUrl) {
    throw new Error("S3Storage is not configured (S3STORAGE_API_URL)");
  }

  const url = new URL(`${apiV1Base(baseUrl)}/uploads/photo`);
  url.searchParams.set("bucket_id", params.bucketId);

  const form = new FormData();
  form.append("file", params.file, params.filename);

  const headers: Record<string, string> = {
    "X-Request-ID": params.requestId ?? crypto.randomUUID(),
  };
  const apiKey = process.env.S3STORAGE_API_KEY?.trim();
  if (apiKey) headers["X-API-Key"] = apiKey;

  const timeoutMs = Number(process.env.S3STORAGE_API_TIMEOUT ?? "30000");
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const resp = await fetch(url.toString(), {
      method: "POST",
      headers,
      body: form,
      signal: controller.signal,
    });
    const data = (await resp.json().catch(() => ({}))) as Record<string, unknown>;
    if (!resp.ok) {
      const detail =
        (typeof data.detail === "string" && data.detail) ||
        (typeof data.error === "string" && data.error) ||
        resp.statusText ||
        "Upload failed";
      throw new Error(detail);
    }
    const fileKey = String(
      data.fileKey ?? data.file_key ?? data.key ?? "",
    ).trim();
    if (!fileKey) {
      throw new Error("Storage did not return a file key");
    }
    return {
      fileKey,
      bucketId: String(data.bucketId ?? data.bucket_id ?? params.bucketId),
    };
  } finally {
    clearTimeout(timer);
  }
}
