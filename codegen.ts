import type { CodegenConfig } from "@graphql-codegen/cli";

/**
 * Introspects the Strawberry gateway and emits TypeScript schema types.
 * Local API: CODEGEN_SCHEMA_URL=http://127.0.0.1:8001/graphql npm run codegen
 * Or: npm run codegen:local
 */
const schema =
  process.env.CODEGEN_SCHEMA_URL ||
  process.env.NEXT_PUBLIC_GRAPHQL_URL ||
  "https://api.contact360.io/graphql";

const config: CodegenConfig = {
  schema,
  generates: {
    "src/graphql/generated/types.ts": {
      plugins: ["typescript"],
      config: {
        scalars: {
          BigInt: "string",
          JSON: "Record<string, unknown>",
          namingConvention: "keep",
        },
        enumsAsTypes: true,
        skipTypename: true,
      },
    },
  },
};

export default config;
