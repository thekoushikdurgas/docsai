import { USERS_PROFILE_FIELDS } from "@/graphql/profileSelections";

const USER_LIST_FIELDS = `
  uuid
  email
  name
  isActive
  lastSignInAt
  createdAt
  profile {
    ${USERS_PROFILE_FIELDS}
  }
`;

export const ADMIN_USERS_QUERY = `
  query AdminUsers($filters: UserFilterInput) {
    admin {
      users(filters: $filters) {
        items { ${USER_LIST_FIELDS} }
        pageInfo {
          total
          limit
          offset
          hasNext
          hasPrevious
        }
      }
    }
  }
`;

export const ADMIN_USERS_WITH_BUCKETS_QUERY = `
  query AdminUsersWithBuckets($filters: UserFilterInput) {
    admin {
      usersWithBuckets(filters: $filters) {
        items {
          uuid
          email
          bucket
        }
        pageInfo {
          total
          limit
          offset
          hasNext
          hasPrevious
        }
      }
    }
  }
`;

export const ADMIN_USER_STATS_QUERY = `
  query AdminUserStats {
    admin {
      userStats {
        totalUsers
        activeUsers
        usersByRole
        usersByPlan
      }
    }
  }
`;

export const ADMIN_UPDATE_USER_ROLE = `
  mutation AdminUpdateUserRole($input: UpdateUserRoleInput!) {
    admin {
      updateUserRole(input: $input) {
        uuid
        profile { role }
      }
    }
  }
`;

export const ADMIN_UPDATE_USER_CREDITS = `
  mutation AdminUpdateUserCredits($input: UpdateUserCreditsInput!) {
    admin {
      updateUserCredits(input: $input) {
        uuid
        profile { credits }
      }
    }
  }
`;

export const ADMIN_DELETE_USER = `
  mutation AdminDeleteUser($input: DeleteUserInput!) {
    admin {
      deleteUser(input: $input)
    }
  }
`;

export const ADMIN_SCHEDULER_JOBS_QUERY = `
  query AdminSchedulerJobs(
    $limit: Int
    $offset: Int
    $status: String
    $sourceService: String
    $userId: ID
    $jobFamily: String
  ) {
    admin {
      schedulerJobs(
        limit: $limit
        offset: $offset
        status: $status
        sourceService: $sourceService
        userId: $userId
        jobFamily: $jobFamily
      ) {
        jobs {
          id
          jobId
          userId
          jobType
          status
          sourceService
          jobFamily
          createdAt
          updatedAt
        }
        pageInfo {
          total
          limit
          offset
          hasNext
          hasPrevious
        }
      }
    }
  }
`;

export const JOBS_JOB_DETAIL_QUERY = `
  query AdminSchedulerJobDetail($jobId: ID!) {
    jobs {
      job(jobId: $jobId) {
        id
        jobId
        userId
        jobType
        status
        sourceService
        jobFamily
        jobSubtype
        requestPayload
        responsePayload
        statusPayload
        createdAt
        updatedAt
      }
    }
  }
`;

export const ADMIN_JOB_TICKETS_QUERY = `
  query AdminJobTickets(
    $limit: Int
    $offset: Int
    $status: String
    $userId: ID
    $externalJobId: String
  ) {
    admin {
      jobTickets(
        limit: $limit
        offset: $offset
        status: $status
        userId: $userId
        externalJobId: $externalJobId
      ) {
        tickets {
          id
          userId
          jobSource
          externalJobId
          jobType
          jobStatusSnapshot
          title
          description
          severity
          status
          adminNotes
          createdAt
          updatedAt
        }
        pageInfo {
          total
          limit
          offset
          hasNext
          hasPrevious
        }
      }
    }
  }
`;

export const ADMIN_JOB_TICKET_DETAIL_QUERY = `
  query AdminJobTicketDetail($ticketId: ID!) {
    admin {
      jobTicket(ticketId: $ticketId) {
        id
        userId
        jobSource
        externalJobId
        jobType
        jobStatusSnapshot
        title
        description
        severity
        status
        adminNotes
        resolvedByUserId
        resolvedAt
        createdAt
        updatedAt
      }
    }
  }
`;

export const ADMIN_UPDATE_JOB_TICKET = `
  mutation AdminUpdateJobTicket($input: UpdateJobTicketStatusInput!) {
    admin {
      updateJobTicketStatus(input: $input) {
        id
        status
        adminNotes
        severity
        title
        externalJobId
        userId
        updatedAt
      }
    }
  }
`;

export const ADMIN_LOG_STATISTICS_QUERY = `
  query AdminLogStatistics($timeRange: String) {
    admin {
      logStatistics(timeRange: $timeRange) {
        totalLogs
        errorRate
        byLevel
        timeRange
      }
    }
  }
`;

export const ADMIN_LOGS_QUERY = `
  query AdminLogs($filters: LogQueryFilterInput) {
    admin {
      logs(filters: $filters) {
        items {
          id
          level
          message
          logger
          timestamp
        }
        pageInfo {
          total
          limit
          offset
          hasNext
          hasPrevious
        }
      }
    }
  }
`;

export const ADMIN_SEARCH_LOGS_QUERY = `
  query AdminSearchLogs($input: LogSearchInput!) {
    admin {
      searchLogs(input: $input) {
        items {
          id
          level
          message
          logger
          timestamp
        }
        pageInfo {
          total
          limit
          offset
          hasNext
          hasPrevious
        }
        query
      }
    }
  }
`;

export const ADMIN_AUDIT_EVENTS_QUERY = `
  query AdminAuditEvents($limit: Int!, $offset: Int!) {
    admin {
      graphqlAuditEvents(limit: $limit, offset: $offset) {
        id
        operationName
        actorUserId
        targetUserId
        createdAt
      }
    }
  }
`;

export const ADMIN_SUBSCRIPTION_SWEEP = `
  mutation AdminSubscriptionSweep($limit: Int, $maxBatches: Int) {
    admin {
      runSubscriptionExpirySweep(limit: $limit, maxBatches: $maxBatches)
    }
  }
`;

const BILLING_PLAN_PERIOD_FIELDS = `
  period
  credits
  dailyCreditsLimit
  ratePerCredit
  price
  savings {
    amount
    percentage
  }
`;

export const BILLING_PLANS_QUERY = `
  query AdminBillingPlans($includeInactive: Boolean = false) {
    billing {
      plans(includeInactive: $includeInactive) {
        category
        name
        isActive
        periods {
          monthly { ${BILLING_PLAN_PERIOD_FIELDS} }
          quarterly { ${BILLING_PLAN_PERIOD_FIELDS} }
          yearly { ${BILLING_PLAN_PERIOD_FIELDS} }
        }
        features {
          id
          label
          sortOrder
        }
      }
    }
  }
`;

export const BILLING_CREATE_PLAN_FEATURE = `
  mutation AdminBillingCreatePlanFeature($category: String!, $input: CreatePlanFeatureInput!) {
    billing {
      createPlanFeature(category: $category, input: $input) {
        message
        id
        category
      }
    }
  }
`;

export const BILLING_UPDATE_PLAN_FEATURE = `
  mutation AdminBillingUpdatePlanFeature(
    $category: String!
    $featureId: Int!
    $input: UpdatePlanFeatureInput!
  ) {
    billing {
      updatePlanFeature(category: $category, featureId: $featureId, input: $input) {
        message
        id
        category
      }
    }
  }
`;

export const BILLING_DELETE_PLAN_FEATURE = `
  mutation AdminBillingDeletePlanFeature($category: String!, $featureId: Int!) {
    billing {
      deletePlanFeature(category: $category, featureId: $featureId) {
        message
        id
        category
      }
    }
  }
`;

export const BILLING_CREATE_PLAN = `
  mutation AdminBillingCreatePlan($input: CreatePlanInput!) {
    billing {
      createPlan(input: $input) {
        message
        category
      }
    }
  }
`;

export const BILLING_UPDATE_PLAN = `
  mutation AdminBillingUpdatePlan($category: String!, $input: UpdatePlanInput!) {
    billing {
      updatePlan(category: $category, input: $input) {
        message
        category
      }
    }
  }
`;

export const BILLING_DELETE_PLAN = `
  mutation AdminBillingDeletePlan($category: String!) {
    billing {
      deletePlan(category: $category) {
        message
        category
      }
    }
  }
`;

export const BILLING_CREATE_PLAN_PERIOD = `
  mutation AdminBillingCreatePlanPeriod($category: String!, $input: CreatePlanPeriodInput!) {
    billing {
      createPlanPeriod(category: $category, input: $input) {
        message
        category
        period
      }
    }
  }
`;

export const BILLING_UPDATE_PLAN_PERIOD = `
  mutation AdminBillingUpdatePlanPeriod($category: String!, $period: String!, $input: UpdatePlanPeriodInput!) {
    billing {
      updatePlanPeriod(category: $category, period: $period, input: $input) {
        message
        category
        period
      }
    }
  }
`;

export const BILLING_DELETE_PLAN_PERIOD = `
  mutation AdminBillingDeletePlanPeriod($category: String!, $period: String!) {
    billing {
      deletePlanPeriod(category: $category, period: $period) {
        message
        category
        period
      }
    }
  }
`;

export const BILLING_ADDONS_QUERY = `
  query AdminBillingAddons {
    billing {
      addons {
        id
        name
        credits
        ratePerCredit
        price
      }
    }
  }
`;

export const BILLING_CREATE_ADDON = `
  mutation AdminBillingCreateAddon($input: CreateAddonInput!) {
    billing {
      createAddon(input: $input) {
        id
        message
      }
    }
  }
`;

export const BILLING_UPDATE_ADDON = `
  mutation AdminBillingUpdateAddon($packageId: String!, $input: UpdateAddonInput!) {
    billing {
      updateAddon(packageId: $packageId, input: $input) {
        id
        message
      }
    }
  }
`;

export const BILLING_DELETE_ADDON = `
  mutation AdminBillingDeleteAddon($packageId: String!) {
    billing {
      deleteAddon(packageId: $packageId) {
        id
        message
      }
    }
  }
`;

export const BILLING_PAYMENT_INSTRUCTIONS_QUERY = `
  query AdminBillingPaymentInstructions {
    billing {
      paymentInstructions {
        upiId
        phoneNumber
        email
        qrCodeS3Key
        qrCodeBucketId
        qrCodeDownloadUrl
      }
    }
  }
`;

export const BILLING_UPDATE_PAYMENT_INSTRUCTIONS = `
  mutation AdminBillingUpdatePaymentInstructions($input: UpdatePaymentInstructionsInput!) {
    billing {
      updatePaymentInstructions(input: $input) {
        upiId
        phoneNumber
        email
        qrCodeS3Key
        qrCodeBucketId
        qrCodeDownloadUrl
      }
    }
  }
`;

export const BILLING_PAYMENTS_QUERY = `
  query AdminPaymentSubmissions($status: String, $limit: Int, $offset: Int) {
    billing {
      paymentSubmissions(status: $status, limit: $limit, offset: $offset) {
        items {
          id
          userId
          userEmail
          amount
          status
          createdAt
        }
        total
        limit
        offset
        hasNext
        hasPrevious
      }
    }
  }
`;

export const HEALTH_SATELLITE_QUERY = `
  query AdminSatelliteHealth {
    health {
      satelliteHealth {
        name
        status
        configured
        detail
      }
    }
  }
`;

export const AI_CHATS_QUERY = `
  query AdminAIChats($filters: AIChatFilterInput) {
    aiChats {
      aiChats(filters: $filters) {
        items {
          uuid
          title
          createdAt
          updatedAt
        }
        pageInfo { hasNext hasPrevious }
      }
    }
  }
`;

export const KNOWLEDGE_ARTICLES_QUERY = `
  query AdminKnowledgeArticles($limit: Int!, $offset: Int!) {
    knowledge {
      articles(limit: $limit, offset: $offset) {
        id
        title
        createdAt
        updatedAt
      }
    }
  }
`;

export const S3_FILES_QUERY = `
  query AdminS3Files($prefix: String) {
    s3 {
      s3Files(prefix: $prefix) {
        files {
          key
          size
          lastModified
        }
      }
    }
  }
`;

export const ADMIN_USER_HISTORY_QUERY = `
  query AdminUserHistory($filters: UserHistoryFilterInput) {
    admin {
      userHistory(filters: $filters) {
        items {
          id
          userId
          userEmail
          userName
          eventType
          ip
          country
          city
          createdAt
        }
        pageInfo {
          total
          limit
          offset
          hasNext
          hasPrevious
        }
      }
    }
  }
`;

export const ADMIN_DELETE_LOG = `
  mutation AdminDeleteLog($input: DeleteLogInput!) {
    admin { deleteLog(input: $input) }
  }
`;

export const ADMIN_UPDATE_LOG = `
  mutation AdminUpdateLog($input: UpdateLogInput!) {
    admin {
      updateLog(input: $input) {
        id
        level
        message
        logger
        timestamp
      }
    }
  }
`;

export const ADMIN_DELETE_LOGS_BULK = `
  mutation AdminDeleteLogsBulk($input: DeleteLogsBulkInput!) {
    admin {
      deleteLogsBulk(input: $input) {
        deletedCount
      }
    }
  }
`;

export const BILLING_APPROVE_PAYMENT = `
  mutation AdminApprovePayment($submissionId: String!) {
    billing {
      approvePayment(submissionId: $submissionId) {
        id
        status
        userEmail
        amount
      }
    }
  }
`;

export const BILLING_DECLINE_PAYMENT = `
  mutation AdminDeclinePayment($input: DeclinePaymentInput!) {
    billing {
      declinePayment(input: $input) {
        id
        status
        declineReason
      }
    }
  }
`;

export const JOBS_RETRY_JOB = `
  mutation AdminRetryJob($input: RetryJobInput!) {
    jobs {
      retryJob(input: $input)
    }
  }
`;

export const ADMIN_PROMOTE_TO_ADMIN = `
  mutation AdminPromoteToAdmin($input: PromoteToAdminInput!) {
    admin {
      promoteToAdmin(input: $input) {
        uuid
        profile { role }
      }
    }
  }
`;

export const ADMIN_PROMOTE_TO_SUPER_ADMIN = `
  mutation AdminPromoteToSuperAdmin($input: PromoteToSuperAdminInput!) {
    admin {
      promoteToSuperAdmin(input: $input) {
        uuid
        profile { role }
      }
    }
  }
`;

export const ADMIN_REQUEST_DANGEROUS_APPROVAL = `
  mutation AdminRequestDangerousApproval($input: RequestDangerousOperationApprovalInput!) {
    admin {
      requestDangerousOperationApproval(input: $input) {
        approvalId
        operation
        status
      }
    }
  }
`;

export const S3_DELETE_FILE = `
  mutation AdminS3DeleteFile($fileKey: String!) {
    s3 {
      deleteFile(fileKey: $fileKey)
    }
  }
`;

export const HEALTH_API_METADATA_QUERY = `
  query AdminApiMetadata {
    health {
      apiMetadata {
        name
        version
        docsUrl
        buildSha
        gitRef
      }
    }
  }
`;

export const CONTACTS_EXPLORER_QUERY = `
  query AdminContactsExplorer($query: VQLQueryInput) {
    contacts {
      contacts(query: $query) {
        items {
          uuid
          email
          firstName
          lastName
          title
          company { name }
        }
        total
        limit
        offset
      }
    }
  }
`;

export const CAMPAIGN_CQL_PARSE = `
  query AdminCqlParse($query: String!, $target: String) {
    campaignSatellite {
      cqlParse(query: $query, target: $target)
    }
  }
`;

export const CAMPAIGN_CQL_VALIDATE = `
  query AdminCqlValidate($cql: JSON!) {
    campaignSatellite {
      cqlValidate(cql: $cql)
    }
  }
`;

export const KNOWLEDGE_ARTICLES_FULL_QUERY = `
  query AdminKnowledgeArticlesFull($limit: Int!, $offset: Int!) {
    knowledge {
      articles(limit: $limit, offset: $offset) {
        id
        title
        body
        tags
        createdAt
        updatedAt
      }
    }
  }
`;

export const KNOWLEDGE_CREATE_ARTICLE = `
  mutation AdminKnowledgeCreate($input: CreateKnowledgeArticleInput!) {
    knowledge {
      createArticle(input: $input) {
        id
        title
      }
    }
  }
`;

export const KNOWLEDGE_UPDATE_ARTICLE = `
  mutation AdminKnowledgeUpdate($input: UpdateKnowledgeArticleInput!) {
    knowledge {
      updateArticle(input: $input) {
        id
        title
      }
    }
  }
`;

export const KNOWLEDGE_DELETE_ARTICLE = `
  mutation AdminKnowledgeDelete($articleId: ID!) {
    knowledge {
      deleteArticle(articleId: $articleId)
    }
  }
`;

export const AI_CHAT_DETAIL_QUERY = `
  query AdminAIChatDetail($chatId: String!) {
    aiChats {
      aiChat(chatId: $chatId) {
        uuid
        title
        messages {
          role
          content
          createdAt
        }
      }
    }
  }
`;

export const AI_CREATE_CHAT = `
  mutation AdminCreateAIChat($input: CreateAIChatInput!) {
    aiChats {
      createAIChat(input: $input) {
        uuid
        title
      }
    }
  }
`;

export const AI_SEND_MESSAGE = `
  mutation AdminSendAIMessage($chatId: String!, $input: SendMessageInput!) {
    aiChats {
      sendMessage(chatId: $chatId, input: $input) {
        uuid
        title
        messages {
          role
          content
          createdAt
        }
      }
    }
  }
`;
