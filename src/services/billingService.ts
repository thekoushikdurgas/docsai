import { graphqlMutation, graphqlQuery } from "@/lib/graphqlClient";
import {
  ADMIN_SUBSCRIPTION_SWEEP,
  BILLING_ADDONS_QUERY,
  BILLING_APPROVE_PAYMENT,
  BILLING_CREATE_ADDON,
  BILLING_DECLINE_PAYMENT,
  BILLING_DELETE_ADDON,
  BILLING_PAYMENT_INSTRUCTIONS_QUERY,
  BILLING_PAYMENTS_QUERY,
  BILLING_PLANS_QUERY,
  BILLING_UPDATE_ADDON,
  BILLING_UPDATE_PAYMENT_INSTRUCTIONS,
} from "@/graphql/adminOperations";

export type AddonPackageRow = {
  id: string;
  name: string;
  credits: number;
  ratePerCredit: number;
  price: number;
};

export const billingService = {
  plans: () => graphqlQuery(BILLING_PLANS_QUERY),

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
