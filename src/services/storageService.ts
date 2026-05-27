import { graphqlQuery } from "@/lib/graphqlClient";
import { getAccessToken } from "@/lib/tokenManager";
import { ADMIN_USERS_WITH_BUCKETS_QUERY } from "@/graphql/adminOperations";
import type { StorageArtifact } from "@/lib/s3storageServer";

export type StorageUserBucket = {
  uuid: string;
  email: string;
  bucket: string;
};

export type StorageListResult = {
  items: StorageArtifact[];
  total: number;
  limit: number;
  offset: number;
  hasNext: boolean;
  hasPrevious: boolean;
};

function authHeaders(): HeadersInit {
  const token = getAccessToken();
  if (!token) throw new Error("Not signed in");
  return { Authorization: `Bearer ${token}` };
}

export const storageService = {
  usersWithBuckets: (limit = 200, offset = 0) =>
    graphqlQuery(ADMIN_USERS_WITH_BUCKETS_QUERY, {
      filters: { limit, offset },
    }),

  listArtifacts: async (params: {
    bucket: string;
    prefix?: string;
    limit?: number;
    offset?: number;
  }): Promise<StorageListResult> => {
    const bucket = params.bucket.trim();
    if (!bucket) {
      return {
        items: [],
        total: 0,
        limit: params.limit ?? 50,
        offset: 0,
        hasNext: false,
        hasPrevious: false,
      };
    }
    const sub = (params.prefix ?? "").trim().replace(/^\/+/, "");
    const fullPrefix = sub ? `${bucket}/${sub}` : bucket;
    const url = new URL("/api/storage/files", window.location.origin);
    url.searchParams.set("prefix", fullPrefix);
    url.searchParams.set("limit", String(params.limit ?? 50));
    url.searchParams.set("offset", String(params.offset ?? 0));

    const resp = await fetch(url.toString(), {
      headers: authHeaders(),
      cache: "no-store",
    });
    const json = (await resp.json()) as StorageListResult & { error?: string };
    if (!resp.ok) {
      throw new Error(json.error ?? "Failed to load storage");
    }
    return json;
  },

  downloadUrl: async (key: string): Promise<string> => {
    const url = new URL("/api/storage/download-url", window.location.origin);
    url.searchParams.set("key", key);
    const resp = await fetch(url.toString(), {
      headers: authHeaders(),
      cache: "no-store",
    });
    const json = (await resp.json()) as { url?: string; error?: string };
    if (!resp.ok || !json.url) {
      throw new Error(json.error ?? "Could not generate download URL");
    }
    return json.url;
  },

  delete: async (key: string): Promise<void> => {
    const url = new URL("/api/storage/delete", window.location.origin);
    url.searchParams.set("key", key);
    const resp = await fetch(url.toString(), {
      method: "DELETE",
      headers: authHeaders(),
    });
    const json = (await resp.json()) as { success?: boolean; error?: string };
    if (!resp.ok || !json.success) {
      throw new Error(json.error ?? "Delete failed");
    }
  },
};
