"use client";

import { storageService } from "@/services/storageService";
import { STORAGE_USERS_PAGE_SIZE } from "@/lib/storageConstants";
import { useAdminResource } from "./useAdminResource";

export function useStorageUsersWithBuckets() {
  return useAdminResource(
    () => storageService.usersWithBuckets(STORAGE_USERS_PAGE_SIZE, 0),
    [],
  );
}

export function useStorageArtifacts(params: {
  bucket: string;
  prefix: string;
  offset: number;
  limit: number;
}) {
  return useAdminResource(
    () =>
      storageService.listArtifacts({
        bucket: params.bucket,
        prefix: params.prefix,
        limit: params.limit,
        offset: params.offset,
      }),
    [params.bucket, params.prefix, params.offset, params.limit],
  );
}
