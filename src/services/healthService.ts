import { graphqlQuery } from "@/lib/graphqlClient";
import {
  HEALTH_API_METADATA_QUERY,
  HEALTH_SATELLITE_QUERY,
} from "@/graphql/adminOperations";

export const healthService = {
  satellites: () => graphqlQuery(HEALTH_SATELLITE_QUERY),

  apiMetadata: () =>
    graphqlQuery(HEALTH_API_METADATA_QUERY, {}, { showToastOnError: false }),
};
