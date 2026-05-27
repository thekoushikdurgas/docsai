import { graphqlMutation, graphqlQuery } from "@/lib/graphqlClient";
import {
  ADMIN_DELETE_USER,
  ADMIN_PROMOTE_TO_ADMIN,
  ADMIN_PROMOTE_TO_SUPER_ADMIN,
  ADMIN_REQUEST_DANGEROUS_APPROVAL,
  ADMIN_UPDATE_USER_CREDITS,
  ADMIN_UPDATE_USER_ROLE,
  ADMIN_USER_HISTORY_QUERY,
  ADMIN_USER_STATS_QUERY,
  ADMIN_USERS_QUERY,
} from "@/graphql/adminOperations";
import {
  USERS_FIND_BY_ID_MAX_SCAN,
  USERS_FIND_BY_ID_PAGE_SIZE,
} from "@/lib/usersConstants";

export type AdminUserRow = {
  uuid: string;
  email?: string;
  name?: string | null;
  isActive?: boolean;
  lastSignInAt?: string | null;
  createdAt?: string;
  profile?: {
    role?: string;
    credits?: number;
    subscriptionPlan?: string;
    subscriptionStatus?: string;
    subscriptionEndsAt?: string | null;
    subscriptionPeriod?: string | null;
  } | null;
};

export type UsersListParams = {
  limit?: number;
  offset?: number;
};

export type UsersListResult = {
  admin: {
    users: {
      items: AdminUserRow[];
      pageInfo?: {
        total?: number;
        limit?: number;
        offset?: number;
        hasNext?: boolean;
        hasPrevious?: boolean;
      };
    };
  };
};

export type UserHistoryItemRow = {
  id: string;
  userId?: string;
  userEmail?: string | null;
  userName?: string | null;
  eventType?: string;
  ip?: string | null;
  country?: string | null;
  city?: string | null;
  createdAt?: string;
};

export type UserHistoryParams = {
  userId: string;
  limit?: number;
  offset?: number;
  eventType?: string | null;
};

export const usersService = {
  list: (params?: UsersListParams) =>
    graphqlQuery<UsersListResult>(ADMIN_USERS_QUERY, {
      filters: {
        limit: params?.limit ?? 100,
        offset: params?.offset ?? 0,
      },
    }),

  stats: () =>
    graphqlQuery<{ admin: { userStats: unknown } }>(ADMIN_USER_STATS_QUERY),

  async getById(userId: string): Promise<AdminUserRow | null> {
    const uid = userId.trim();
    if (!uid) return null;

    let offset = 0;
    let scanned = 0;
    const limit = USERS_FIND_BY_ID_PAGE_SIZE;

    while (scanned < USERS_FIND_BY_ID_MAX_SCAN) {
      const res = await usersService.list({ limit, offset });
      const items = res?.admin?.users?.items ?? [];
      const match = items.find((u) => u.uuid === uid);
      if (match) return match;

      const pageInfo = res?.admin?.users?.pageInfo;
      if (!pageInfo?.hasNext) break;

      offset += limit;
      scanned += items.length;
    }
    return null;
  },

  history: (params: UserHistoryParams) => {
    const filters: Record<string, unknown> = {
      userId: params.userId,
      limit: params.limit ?? 50,
      offset: params.offset ?? 0,
    };
    const et = (params.eventType ?? "").trim();
    if (et && et !== "all") {
      filters.eventType = et;
    }
    return graphqlQuery<{
      admin: {
        userHistory: {
          items: UserHistoryItemRow[];
          pageInfo?: {
            total?: number;
            limit?: number;
            offset?: number;
            hasNext?: boolean;
            hasPrevious?: boolean;
          };
        };
      };
    }>(ADMIN_USER_HISTORY_QUERY, { filters });
  },

  async adjustCredits(
    userId: string,
    delta: number,
    _reason: string,
  ): Promise<{ credits: number }> {
    const row = await usersService.getById(userId);
    if (!row) {
      throw new Error(
        "User not found in admin directory (scan limit reached).",
      );
    }
    const current = Number(row.profile?.credits ?? 0);
    const newCredits = Math.max(0, current + delta);
    await graphqlMutation(ADMIN_UPDATE_USER_CREDITS, {
      input: { userId, credits: newCredits },
    });
    return { credits: newCredits };
  },

  updateRole: (userId: string, role: string) =>
    graphqlMutation(ADMIN_UPDATE_USER_ROLE, {
      input: { userId, role },
    }),

  updateCredits: (userId: string, credits: number) =>
    graphqlMutation(ADMIN_UPDATE_USER_CREDITS, {
      input: { userId, credits },
    }),

  remove: (userId: string, approvalId?: string) =>
    graphqlMutation(ADMIN_DELETE_USER, {
      input: { userId, ...(approvalId ? { approvalId } : {}) },
    }),

  promoteToAdmin: (userId: string) =>
    graphqlMutation(ADMIN_PROMOTE_TO_ADMIN, { input: { userId } }),

  promoteToSuperAdmin: (userId: string, approvalId?: string) =>
    graphqlMutation(ADMIN_PROMOTE_TO_SUPER_ADMIN, {
      input: { userId, ...(approvalId ? { approvalId } : {}) },
    }),

  requestDangerousApproval: (operation: string, targetUserId: string) =>
    graphqlMutation(ADMIN_REQUEST_DANGEROUS_APPROVAL, {
      input: { operation, targetUserId },
    }),
};
