import { readFile } from "node:fs/promises";
import path from "node:path";

export async function GET() {
  try {
    const file = path.join(
      process.cwd(),
      "..",
      "..",
      "docs",
      "frontend",
      "pages",
      "admin-parity-matrix.json",
    );
    const raw = await readFile(file, "utf8");
    const json = JSON.parse(raw) as {
      generated_at?: string;
      counts?: Record<string, number>;
    };
    return Response.json({
      generated_at: json.generated_at,
      counts: json.counts,
    });
  } catch {
    return Response.json(
      { error: "Parity matrix not found. Run npm run parity:matrix." },
      { status: 404 },
    );
  }
}
