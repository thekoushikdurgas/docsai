import { NextResponse } from "next/server";
import { assertAdminOrSuperAdmin } from "@/lib/serverGraphql";
import { isS3StorageConfigured, listStorageArtifacts } from "@/lib/s3storageServer";

function bearerToken(request: Request): string | null {
  const auth = request.headers.get("authorization") ?? "";
  if (auth.toLowerCase().startsWith("bearer ")) {
    return auth.slice(7).trim() || null;
  }
  return null;
}

export async function GET(request: Request) {
  const token = bearerToken(request);
  if (!token) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  if (!isS3StorageConfigured()) {
    return NextResponse.json(
      { error: "S3Storage is not configured" },
      { status: 503 },
    );
  }

  try {
    await assertAdminOrSuperAdmin(token);
  } catch (e) {
    const message = e instanceof Error ? e.message : "Forbidden";
    return NextResponse.json({ error: message }, { status: 403 });
  }

  const url = new URL(request.url);
  const prefix = url.searchParams.get("prefix") ?? "";
  const limit = Math.min(
    200,
    Math.max(1, parseInt(url.searchParams.get("limit") ?? "50", 10) || 50),
  );
  const offset = Math.max(0, parseInt(url.searchParams.get("offset") ?? "0", 10) || 0);

  try {
    const result = await listStorageArtifacts({ prefix, limit, offset });
    return NextResponse.json({
      items: result.items,
      total: result.total,
      limit,
      offset,
      hasNext: offset + limit < result.total,
      hasPrevious: offset > 0,
    });
  } catch (e) {
    return NextResponse.json(
      { error: e instanceof Error ? e.message : "List failed" },
      { status: 500 },
    );
  }
}
