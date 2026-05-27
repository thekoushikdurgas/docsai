import { graphqlQuery } from "@/lib/graphqlClient";
import {
  CAMPAIGN_CQL_PARSE,
  CAMPAIGN_CQL_VALIDATE,
  CONTACTS_EXPLORER_QUERY,
} from "@/graphql/adminOperations";

export const opsService = {
  contacts: (limit = 25, offset = 0) =>
    graphqlQuery(CONTACTS_EXPLORER_QUERY, {
      query: { limit, offset },
    }),

  cqlParse: (query: string, target?: string) =>
    graphqlQuery(CAMPAIGN_CQL_PARSE, { query, target: target ?? null }),

  cqlValidate: (cql: Record<string, unknown>) =>
    graphqlQuery(CAMPAIGN_CQL_VALIDATE, { cql }),
};
