import { graphqlMutation, graphqlQuery } from "@/lib/graphqlClient";
import type { BillingPlan } from "@/lib/billingPlanConstants";
import {
  ADMIN_SUBSCRIPTION_SWEEP,
  BILLING_ADDONS_QUERY,
  BILLING_APPROVE_PAYMENT,
  BILLING_CREATE_ADDON,
  BILLING_CREATE_PLAN,
  BILLING_CREATE_PLAN_FEATURE,
  BILLING_CREATE_PLAN_PERIOD,
  BILLING_DECLINE_PAYMENT,
  BILLING_DELETE_ADDON,
  BILLING_DELETE_PLAN,
  BILLING_DELETE_PLAN_FEATURE,
  BILLING_DELETE_PLAN_PERIOD,
  BILLING_PAYMENT_INSTRUCTIONS_QUERY,
  BILLING_PAYMENTS_QUERY,
  BILLING_PLANS_QUERY,
  BILLING_UPDATE_ADDON,
  BILLING_UPDATE_PAYMENT_INSTRUCTIONS,
  BILLING_UPDATE_PLAN,
  BILLING_UPDATE_PLAN_FEATURE,
  BILLING_UPDATE_PLAN_PERIOD,
} from "@/graphql/adminOperations";

export type AddonPackageRow = {
  id: string;
  name: string;
  credits: number;
  ratePerCredit: number;
  price: number;
};

export type PlansQueryResult = {
  billing?: { plans?: BillingPlan[] };
};

export type PlanPeriodMutationInput = {
  period: string;
  credits: number;
  dailyCreditsLimit: number;
  ratePerCredit: number;
  price: number;
  savingsAmount?: number;
  savingsPercentage?: number;
};

export const billingService = {
  plans: () => graphqlQuery<PlansQueryResult>(BILLING_PLANS_QUERY),

  addons: () => graphqlQuery(BILLING_ADDONS_QUERY),

  payments: (limit = 50, offset = 0, status?: string) =>
    graphqlQuery(BILLING_PAYMENTS_QUERY, { limit, offset, status }),

  approve: (submissionId: string) =>
    graphqlMutation(BILLING_APPROVE_PAYMENT, { submissionId }),

  decline: (submissionId: string, reason: string) =>
    graphqlMutation(BILLING_DECLINE_PAYMENT, {
      input: { submissionId, reason },
    }),

  createAddon: (input: {
    id: string;
    name: string;
    credits: number;
    ratePerCredit: number;
    price: number;
    isActive?: boolean;
  }) => graphqlMutation(BILLING_CREATE_ADDON, { input }),

  updateAddon: (
    packageId: string,
    input: {
      name?: string;
      credits?: number;
      ratePerCredit?: number;
      price?: number;
      isActive?: boolean;
    },
  ) => graphqlMutation(BILLING_UPDATE_ADDON, { packageId, input }),

  deleteAddon: (packageId: string) =>
    graphqlMutation(BILLING_DELETE_ADDON, { packageId }),

  createPlan: (input: {
    category: string;
    name: string;
    periods: PlanPeriodMutationInput[];
    isActive?: boolean;
  }) => graphqlMutation(BILLING_CREATE_PLAN, { input }),

  updatePlan: (
    category: string,
    input: { name?: string; isActive?: boolean },
  ) => graphqlMutation(BILLING_UPDATE_PLAN, { category, input }),

  deletePlan: (category: string) =>
    graphqlMutation(BILLING_DELETE_PLAN, { category }),

  createPlanPeriod: (category: string, input: PlanPeriodMutationInput) =>
    graphqlMutation(BILLING_CREATE_PLAN_PERIOD, { category, input }),

  updatePlanPeriod: (
    category: string,
    period: string,
    input: {
      credits?: number;
      dailyCreditsLimit?: number;
      ratePerCredit?: number;
      price?: number;
      savingsAmount?: number;
      savingsPercentage?: number;
    },
  ) => graphqlMutation(BILLING_UPDATE_PLAN_PERIOD, { category, period, input }),

  deletePlanPeriod: (category: string, period: string) =>
    graphqlMutation(BILLING_DELETE_PLAN_PERIOD, { category, period }),

  createPlanFeature: (
    category: string,
    input: { label: string; sortOrder?: number },
  ) =>
    graphqlMutation(BILLING_CREATE_PLAN_FEATURE, {
      category,
      input: {
        label: input.label,
        sortOrder: input.sortOrder ?? 0,
      },
    }),

  updatePlanFeature: (
    category: string,
    featureId: number,
    input: { label?: string; sortOrder?: number },
  ) =>
    graphqlMutation(BILLING_UPDATE_PLAN_FEATURE, { category, featureId, input }),

  deletePlanFeature: (category: string, featureId: number) =>
    graphqlMutation(BILLING_DELETE_PLAN_FEATURE, { category, featureId }),

  paymentInstructions: () =>
    graphqlQuery(BILLING_PAYMENT_INSTRUCTIONS_QUERY),

  updatePaymentInstructions: (input: {
    upiId: string;
    phoneNumber: string;
    email: string;
    qrCodeS3Key?: string | null;
    qrCodeBucketId?: string | null;
  }) => graphqlMutation(BILLING_UPDATE_PAYMENT_INSTRUCTIONS, { input }),

  sweep: () =>
    graphqlMutation(ADMIN_SUBSCRIPTION_SWEEP, { limit: 500, maxBatches: 50 }),
};
