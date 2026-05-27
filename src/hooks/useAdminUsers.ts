"use client";

import { usersService, type UsersListParams } from "@/services/usersService";
import { useAdminResource } from "./useAdminResource";

export function useAdminUsers(params: UsersListParams) {
  return useAdminResource(
    () => usersService.list(params),
    [params.limit, params.offset],
  );
}
