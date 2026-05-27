/**
 * Server-side GraphQL fetch for Next API routes (Bearer token from admin session).
 */

function resolveServerGraphqlUrl(): string {
  const upstream = process.env.GRAPHQL_UPSTREAM_URL?.trim();
  if (upstream) {
    const base = upstream.replace(/\/$/, "");
    return base.endsWith("/graphql") ? base : `${base}/graphql`;
  }
  const api = (
    process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8001"
  ).replace(/\/$/, "");
  return `${api}/graphql`;
}

export async function serverGraphql<T>(
  query: string,
  variables: Record<string, unknown>,
  accessToken: string,
): Promise<T> {
  const resp = await fetch(resolveServerGraphqlUrl(), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify({ query, variables }),
    cache: "no-store",
  });
  const json = (await resp.json()) as {
    data?: T;
    errors?: Array<{ message?: string }>;
  };
  if (json.errors?.length) {
    throw new Error(json.errors[0]?.message ?? "GraphQL error");
  }
  if (!json.data) {
    throw new Error("Empty GraphQL response");
  }
  return json.data;
}

const AUTH_ME_FOR_UPLOAD = `
  query BillingQrUploadMe {
    auth {
      me {
        uuid
        bucket
        profile { role }
      }
    }
  }
`;

export async function resolvePaymentQrBucket(
  accessToken: string,
): Promise<string | null> {
  const envBucket = process.env.PAYMENT_QR_BUCKET_ID?.trim();
  if (envBucket) return envBucket;

  try {
    const data = await serverGraphql<{
      auth?: { me?: { uuid?: string; bucket?: string | null } | null };
    }>(AUTH_ME_FOR_UPLOAD, {}, accessToken);
    const me = data.auth?.me;
    const bucket = me?.bucket?.trim() || me?.uuid?.trim();
    return bucket || null;
  } catch {
    return null;
  }
}

export async function getOperatorRole(
  accessToken: string,
): Promise<string | null> {
  const data = await serverGraphql<{
    auth?: { me?: { profile?: { role?: string | null } | null } | null };
  }>(AUTH_ME_FOR_UPLOAD, {}, accessToken);
  return data.auth?.me?.profile?.role ?? null;
}

export async function assertAdminOrSuperAdmin(
  accessToken: string,
): Promise<string> {
  const role = await getOperatorRole(accessToken);
  if (role !== "Admin" && role !== "SuperAdmin") {
    throw new Error("Admin or SuperAdmin role required");
  }
  return role;
}

export async function assertSuperAdmin(accessToken: string): Promise<void> {
  const role = await getOperatorRole(accessToken);
  if (role !== "SuperAdmin") {
    throw new Error("SuperAdmin role required");
  }
}
