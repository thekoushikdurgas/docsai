"use client";

import { analyticsService } from "@/services/analyticsService";
import { healthService } from "@/services/healthService";
import { aiService } from "@/services/aiService";
import { knowledgeService } from "@/services/knowledgeService";
import { auditService } from "@/services/auditService";
import { useAdminResource } from "./useAdminResource";

type UserStatsResponse = Awaited<ReturnType<typeof analyticsService.userStats>>;

export function useAdminUserStats() {
  return useAdminResource<UserStatsResponse>(
    () => analyticsService.userStats(),
    [],
  );
}

type HealthResponse = Awaited<ReturnType<typeof healthService.satellites>>;

export function useAdminHealth() {
  return useAdminResource<HealthResponse>(() => healthService.satellites(), []);
}

export function useAdminAiChats() {
  return useAdminResource(() => aiService.chats(50, 0), []);
}

export function useAdminKnowledge() {
  return useAdminResource(() => knowledgeService.list(50, 0), []);
}

export function useAdminAudit() {
  return useAdminResource(() => auditService.events(50, 0), []);
}
