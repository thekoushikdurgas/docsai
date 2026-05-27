import { graphqlMutation, graphqlQuery } from "@/lib/graphqlClient";
import {
  ADMIN_JOB_TICKET_DETAIL_QUERY,
  ADMIN_JOB_TICKETS_QUERY,
  ADMIN_SCHEDULER_JOBS_QUERY,
  ADMIN_UPDATE_JOB_TICKET,
  JOBS_JOB_DETAIL_QUERY,
  JOBS_RETRY_JOB,
} from "@/graphql/adminOperations";

export type SchedulerJobsListParams = {
  limit?: number;
  offset?: number;
  status?: string | null;
  sourceService?: string | null;
  userId?: string | null;
  jobFamily?: string | null;
};

export type JobTicketsListParams = {
  limit?: number;
  offset?: number;
  status?: string | null;
  userId?: string | null;
  externalJobId?: string | null;
};

export const jobsService = {
  list: ({
    limit = 25,
    offset = 0,
    status,
    sourceService,
    userId,
    jobFamily,
  }: SchedulerJobsListParams = {}) =>
    graphqlQuery(ADMIN_SCHEDULER_JOBS_QUERY, {
      limit,
      offset,
      status: status || null,
      sourceService: sourceService || null,
      userId: userId || null,
      jobFamily: jobFamily || null,
    }),

  job: (jobId: string) =>
    graphqlQuery(JOBS_JOB_DETAIL_QUERY, { jobId }),

  tickets: ({
    limit = 25,
    offset = 0,
    status,
    userId,
    externalJobId,
  }: JobTicketsListParams = {}) =>
    graphqlQuery(ADMIN_JOB_TICKETS_QUERY, {
      limit,
      offset,
      status: status || null,
      userId: userId || null,
      externalJobId: externalJobId || null,
    }),

  ticket: (ticketId: string) =>
    graphqlQuery(ADMIN_JOB_TICKET_DETAIL_QUERY, { ticketId }),

  updateTicket: (
    ticketId: string,
    status: string,
    adminNotes?: string | null,
  ) =>
    graphqlMutation(ADMIN_UPDATE_JOB_TICKET, {
      input: {
        ticketId,
        status,
        ...(adminNotes !== undefined ? { adminNotes } : {}),
      },
    }),

  retry: (jobId: string) =>
    graphqlMutation(JOBS_RETRY_JOB, { input: { jobId } }),
};
