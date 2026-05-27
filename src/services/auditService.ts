import { graphqlQuery } from "@/lib/graphqlClient";
import { ADMIN_AUDIT_EVENTS_QUERY } from "@/graphql/adminOperations";

export const auditService = {
  events: (limit = 50, offset = 0) =>
    graphqlQuery(ADMIN_AUDIT_EVENTS_QUERY, { limit, offset }),
};
