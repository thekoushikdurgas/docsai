import { NextResponse } from "next/server";
import { assertSuperAdmin } from "@/lib/serverGraphql";
import { deleteStorageArtifact, isS3StorageConfigured } from "@/lib/s3storageServer";

function bearerToken(request: Request): string | null {
  const auth = request.headers.get("authorization") ?? "";
  if (auth.toLowerCase().startsWith("bearer ")) {
    return auth.slice(7).trim() || null;
  }
  return null;
}

export async function DELETE(request: Request) {
  const token = bearerToken(request);
  if (!token) {
    return NextResponse.json({ success: false, error: "Unauthorized" }, { status: 401 });
  }

  if (!isS3StorageConfigured()) {
    return NextResponse.json(
      { success: false, error: "S3Storage is not configured" },
      { status: 503 },
    );
  }

  try {
    await assertSuperAdmin(token);
  } catch (e) {
    const message = e instanceof Error ? e.message : "Forbidden";
    return NextResponse.json({ success: false, error: message }, { status: 403 });
  }

  const key = new URL(request.url).searchParams.get("key")?.trim() ?? "";
  if (!key) {
    return NextResponse.json(
      { success: false, error: "key is required" },
      { status: 400 },
    );
  }

  const ok = await deleteStorageArtifact(key);
  if (!ok) {
    return NextResponse.json(
      { success: false, error: "Delete failed" },
      { status: 500 },
    );
  }

  return NextResponse.json({ success: true });
}
