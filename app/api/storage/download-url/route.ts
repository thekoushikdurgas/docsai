import { NextResponse } from "next/server";
import { assertAdminOrSuperAdmin } from "@/lib/serverGraphql";
import { getStorageDownloadUrl, isS3StorageConfigured } from "@/lib/s3storageServer";

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

  const key = new URL(request.url).searchParams.get("key")?.trim() ?? "";
  if (!key) {
    return NextResponse.json({ error: "key is required" }, { status: 400 });
  }

  const downloadUrl = await getStorageDownloadUrl(key);
  if (!downloadUrl) {
    return NextResponse.json(
      { error: "Could not generate download URL" },
      { status: 400 },
    );
  }

  return NextResponse.json({ url: downloadUrl });
}
