"use client";

import {
  jobsService,
  type JobTicketsListParams,
  type SchedulerJobsListParams,
} from "@/services/jobsService";
import { useAdminResource } from "./useAdminResource";

export function useAdminJobs(params: SchedulerJobsListParams) {
  return useAdminResource(
    () => jobsService.list(params),
    [
      params.limit,
      params.offset,
      params.status,
      params.sourceService,
      params.userId,
      params.jobFamily,
    ],
  );
}

export function useAdminJobDetail(jobId: string) {
  return useAdminResource(() => jobsService.job(jobId), [jobId]);
}

export function useAdminJobTickets(params: JobTicketsListParams) {
  return useAdminResource(
    () => jobsService.tickets(params),
    [
      params.limit,
      params.offset,
      params.status,
      params.userId,
      params.externalJobId,
    ],
  );
}

export function useAdminJobTicketDetail(ticketId: string) {
  return useAdminResource(() => jobsService.ticket(ticketId), [ticketId]);
}
