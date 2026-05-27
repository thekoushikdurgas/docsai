"use client";

import { usersService } from "@/services/usersService";
import { useAdminResource } from "./useAdminResource";

export function useAdminUserHistory(
  userId: string,
  params: { limit: number; offset: number; eventType: string },
  enabled: boolean,
) {
  return useAdminResource(
    () =>
      enabled
        ? usersService.history({
          userId,
          limit: params.limit,
          offset: params.offset,
          eventType: params.eventType,
        })
        : Promise.resolve(null),
    [userId, params.limit, params.offset, params.eventType, enabled],
  );
}
