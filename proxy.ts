import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { resolvePlanCategory } from "@/lib/planCategory";

const STATIC_PLAN_SEGMENTS = new Set(["create", "manage"]);

/** Legacy tier slugs and non-canonical category casing → `/billing/plans/[category]/…`. */
function redirectLegacyBillingPlanRoute(
  request: NextRequest,
): NextResponse | null {
  const match = request.nextUrl.pathname.match(
    /^\/billing\/plans\/([^/]+)(\/.*)?$/,
  );
  if (!match) return null;

  const slug = decodeURIComponent(match[1]);
  if (STATIC_PLAN_SEGMENTS.has(slug.toLowerCase())) return null;

  const rest = match[2] ?? "";
  const category = resolvePlanCategory(slug);
  const canonicalSlug = category.toUpperCase();
  const normalizedRest =
    rest === "/features" || rest.startsWith("/period") ? "/edit" : rest;

  if (slug.toUpperCase() !== canonicalSlug || slug !== category) {
    const target = `/billing/plans/${encodeURIComponent(category)}${normalizedRest || "/edit"}`;
    return NextResponse.redirect(new URL(target, request.url));
  }

  if (normalizedRest !== rest) {
    const target = `/billing/plans/${encodeURIComponent(category)}${normalizedRest}`;
    return NextResponse.redirect(new URL(target, request.url));
  }

  return null;
}

/** Fast redirect for `/` before the RSC tree runs. */
export function proxy(request: NextRequest) {
  if (request.nextUrl.pathname === "/") {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  const legacyPlan = redirectLegacyBillingPlanRoute(request);
  if (legacyPlan) return legacyPlan;

  return NextResponse.next();
}

export const config = {
  matcher: ["/", "/billing/plans/:path*"],
};
