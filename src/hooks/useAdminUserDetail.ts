"use client";

import { usersService } from "@/services/usersService";
import { useAdminResource } from "./useAdminResource";

export function useAdminUserDetail(userId: string) {
  return useAdminResource(() => usersService.getById(userId), [userId]);
}
