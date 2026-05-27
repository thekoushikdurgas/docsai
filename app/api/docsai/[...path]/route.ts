import { docsaiBffTarget, forwardAuthHeaders } from "@/lib/docsaiBff";

type RouteContext = { params: Promise<{ path: string[] }> };

async function proxy(request: Request, ctx: RouteContext) {
  const { path } = await ctx.params;
  const url = new URL(request.url);
  const target = docsaiBffTarget(path, url.search);

  const init: RequestInit = {
    method: request.method,
    headers: forwardAuthHeaders(request),
    cache: "no-store",
  };

  if (request.method !== "GET" && request.method !== "HEAD") {
    init.body = await request.arrayBuffer();
    const ct = request.headers.get("content-type");
    if (ct) {
      (init.headers as Record<string, string>)["Content-Type"] = ct;
    }
  }

  const upstream = await fetch(target, init);
  const body = await upstream.arrayBuffer();
  return new Response(body, {
    status: upstream.status,
    headers: {
      "Content-Type":
        upstream.headers.get("content-type") || "application/json",
    },
  });
}

export async function GET(request: Request, ctx: RouteContext) {
  return proxy(request, ctx);
}

export async function POST(request: Request, ctx: RouteContext) {
  return proxy(request, ctx);
}

export async function PUT(request: Request, ctx: RouteContext) {
  return proxy(request, ctx);
}

export async function PATCH(request: Request, ctx: RouteContext) {
  return proxy(request, ctx);
}

export async function DELETE(request: Request, ctx: RouteContext) {
  return proxy(request, ctx);
}
