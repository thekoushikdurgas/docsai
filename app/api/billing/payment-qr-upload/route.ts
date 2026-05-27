import { NextResponse } from "next/server";
import {
  assertSuperAdmin,
  resolvePaymentQrBucket,
} from "@/lib/serverGraphql";
import { isS3StorageConfigured, uploadPhotoToS3Storage } from "@/lib/s3storageServer";

const ALLOWED_TYPES = new Set([
  "image/png",
  "image/jpeg",
  "image/jpg",
  "image/webp",
]);

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
  try {
    await assertSuperAdmin(token);
    const paymentQrBucket = await resolvePaymentQrBucket(token);
    return NextResponse.json({
      s3Enabled: isS3StorageConfigured(),
      paymentQrBucket: paymentQrBucket ?? null,
    });
  } catch (e) {
    const message = e instanceof Error ? e.message : "Forbidden";
    const status = message.includes("SuperAdmin") ? 403 : 500;
    return NextResponse.json({ error: message }, { status });
  }
}

export async function POST(request: Request) {
  const token = bearerToken(request);
  if (!token) {
    return NextResponse.json(
      { success: false, error: "Unauthorized" },
      { status: 401 },
    );
  }

  if (!isS3StorageConfigured()) {
    return NextResponse.json(
      { success: false, error: "Storage is not configured" },
      { status: 400 },
    );
  }

  try {
    await assertSuperAdmin(token);
  } catch (e) {
    const message = e instanceof Error ? e.message : "Forbidden";
    return NextResponse.json(
      { success: false, error: message },
      { status: 403 },
    );
  }

  let form: FormData;
  try {
    form = await request.formData();
  } catch {
    return NextResponse.json(
      { success: false, error: "Invalid form data" },
      { status: 400 },
    );
  }

  const file = form.get("file");
  if (!(file instanceof Blob) || file.size === 0) {
    return NextResponse.json(
      { success: false, error: "No file provided" },
      { status: 400 },
    );
  }

  const contentType = (file.type || "image/png").toLowerCase();
  if (!ALLOWED_TYPES.has(contentType)) {
    return NextResponse.json(
      {
        success: false,
        error: `Invalid type. Allowed: ${[...ALLOWED_TYPES].join(", ")}`,
      },
      { status: 400 },
    );
  }

  const manualBucket = String(form.get("qr_code_bucket_id") ?? "").trim();
  const resolved = await resolvePaymentQrBucket(token);
  const bucketId = manualBucket || resolved;
  if (!bucketId) {
    return NextResponse.json(
      {
        success: false,
        error:
          "No bucket available. Set PAYMENT_QR_BUCKET_ID, sign in again, or ensure auth.me returns bucket/uuid.",
      },
      { status: 400 },
    );
  }

  const filename =
    file instanceof File && file.name ? file.name : "qr.png";

  try {
    const result = await uploadPhotoToS3Storage({
      bucketId,
      file,
      filename,
      contentType,
    });
    return NextResponse.json({
      success: true,
      fileKey: result.fileKey,
      bucketId: result.bucketId,
    });
  } catch (e) {
    return NextResponse.json(
      {
        success: false,
        error: e instanceof Error ? e.message : "Upload failed",
      },
      { status: 500 },
    );
  }
}
