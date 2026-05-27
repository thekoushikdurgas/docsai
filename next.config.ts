import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  compress: true,
  poweredByHeader: false,
  devIndicators: false,

  async rewrites() {
    if (process.env.NODE_ENV !== "development") {
      return [];
    }
    let upstream = (
      process.env.GRAPHQL_UPSTREAM_URL ||
      process.env.NEXT_PUBLIC_API_URL ||
      "https://api.contact360.io"
    ).replace(/\/$/, "");
    try {
      const u = new URL(upstream);
      const port = u.port || (u.protocol === "https:" ? "443" : "80");
      const loopback =
        u.hostname === "localhost" ||
        u.hostname === "127.0.0.1" ||
        u.hostname === "::1";
      if (loopback && port === "3001") {
        upstream = "http://127.0.0.1:8000";
      }
    } catch {
      /* keep upstream */
    }
    return [{ source: "/graphql", destination: `${upstream}/graphql` }];
  },

  experimental: {
    /** Dev rewrites proxy `/graphql` → upstream. Default proxy timeout is ~30s. */
    proxyTimeout: 300_000,
  },

  compiler: {
    removeConsole: process.env.NODE_ENV === "production",
  },

  modularizeImports: {
    "lucide-react": {
      transform: "lucide-react/dist/esm/icons/{{kebabCase member}}",
    },
  },
};

export default nextConfig;
